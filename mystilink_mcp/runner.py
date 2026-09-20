# -*- coding: utf-8 -*-
"""Resolve and spawn Mystilink calculator CLIs; parse JSON stdout."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from typing import Any, Dict, List, Optional, Sequence, Tuple

# Short name first, long alias second. Env overrides take precedence.
CLI_CANDIDATES: Dict[str, Tuple[str, ...]] = {
    "lunar": ("lunar", "mystilink-lunar"),
    "bazi": ("bazi", "mystilink-bazi"),
    "ziwei": ("ziwei", "mystilink-ziwei"),
    "horoscope": ("horoscope", "mystilink-horoscope"),
    "tarot": ("tarot", "mystilink-tarot"),
    "liuyao": ("liuyao", "mystilink-liuyao"),
}

CLI_ENV: Dict[str, str] = {
    "lunar": "MYSTILINK_LUNAR_CLI",
    "bazi": "MYSTILINK_BAZI_CLI",
    "ziwei": "MYSTILINK_ZIWEI_CLI",
    "horoscope": "MYSTILINK_HOROSCOPE_CLI",
    "tarot": "MYSTILINK_TAROT_CLI",
    "liuyao": "MYSTILINK_LIUYAO_CLI",
}


class CliError(RuntimeError):
    """CLI missing, non-zero exit, or invalid JSON."""

    def __init__(self, message: str, *, code: str = "cli_error", details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.code = code
        self.details = details or {}


def resolve_cli(system: str) -> str:
    """Return executable path/name for a calculator system."""
    if system not in CLI_CANDIDATES:
        raise CliError(f"unknown system: {system}", code="unknown_system")
    env_key = CLI_ENV[system]
    env = os.environ.get(env_key, "").strip()
    if env:
        return env
    for name in CLI_CANDIDATES[system]:
        found = shutil.which(name)
        if found:
            return found
    short, long = CLI_CANDIDATES[system][0], CLI_CANDIDATES[system][1]
    raise CliError(
        f"{short} CLI not found on PATH (also tried {long}). "
        f"Install the calculator package or set {env_key}.",
        code="cli_not_found",
        details={"system": system, "env": env_key},
    )


def run_cli(system: str, args: Sequence[str], *, timeout: float = 120.0) -> Dict[str, Any]:
    """Spawn CLI with args; return parsed JSON object from stdout."""
    exe = resolve_cli(system)
    cmd: List[str] = [exe, *args]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise CliError(
            f"CLI timed out after {timeout}s: {' '.join(cmd)}",
            code="cli_timeout",
            details={"cmd": cmd},
        ) from exc
    except OSError as exc:
        raise CliError(str(exc), code="cli_spawn_failed", details={"cmd": cmd}) from exc

    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()
    if proc.returncode != 0:
        # Prefer structured stderr JSON when present
        err_payload: Any = None
        if stderr:
            try:
                err_payload = json.loads(stderr)
            except json.JSONDecodeError:
                err_payload = None
        if isinstance(err_payload, dict) and "error" in err_payload:
            raise CliError(
                _error_message(err_payload["error"]),
                code=_error_code(err_payload["error"]),
                details={"cmd": cmd, "stderr": err_payload, "returncode": proc.returncode},
            )
        raise CliError(
            stderr or stdout or f"CLI exited with {proc.returncode}",
            code="cli_failed",
            details={"cmd": cmd, "returncode": proc.returncode, "stdout": stdout, "stderr": stderr},
        )
    if not stdout:
        raise CliError("CLI returned empty stdout", code="cli_empty", details={"cmd": cmd})
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError as exc:
        raise CliError(
            f"CLI stdout is not JSON: {exc}",
            code="cli_invalid_json",
            details={"cmd": cmd, "stdout_head": stdout[:500]},
        ) from exc
    if not isinstance(data, dict):
        raise CliError("CLI JSON root must be an object", code="cli_invalid_json", details={"cmd": cmd})
    return data


def _error_message(error: Any) -> str:
    if isinstance(error, dict):
        return str(error.get("message") or error.get("code") or error)
    return str(error)


def _error_code(error: Any) -> str:
    if isinstance(error, dict) and isinstance(error.get("code"), str):
        return error["code"]
    return "cli_failed"


def structured_error(exc: BaseException) -> Dict[str, Any]:
    if isinstance(exc, CliError):
        err: Dict[str, Any] = {"code": exc.code, "message": str(exc)}
        if exc.details:
            err["details"] = exc.details
        return {"error": err}
    return {"error": {"code": "internal_error", "message": str(exc)}}
