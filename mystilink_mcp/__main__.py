# -*- coding: utf-8 -*-
"""CLI entry: mystilink-mcp [stdio|local-api|version|status]."""
from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .tools import list_cli_status


def cmd_stdio(_: argparse.Namespace) -> int:
    from .server import main as server_main

    server_main()
    return 0


def cmd_local_api(_: argparse.Namespace) -> int:
    from .local_api import main as api_main

    api_main()
    return 0


def cmd_version(_: argparse.Namespace) -> int:
    print(json.dumps({"name": "mystilink-mcp", "version": __version__}, ensure_ascii=False, indent=2))
    return 0


def cmd_status(_: argparse.Namespace) -> int:
    print(json.dumps(list_cli_status(), ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="mystilink-mcp",
        description=(
            "Local Mystilink MCP host integration. "
            "Default command starts stdio MCP. "
            "local-api binds FastAPI to 127.0.0.1 only."
        ),
    )
    sub = p.add_subparsers(dest="command")

    s = sub.add_parser("stdio", help="Run MCP over stdio (default)")
    s.set_defaults(func=cmd_stdio)

    a = sub.add_parser("local-api", help="Run loopback FastAPI on 127.0.0.1")
    a.set_defaults(func=cmd_local_api)

    v = sub.add_parser("version", help="Print package version JSON")
    v.set_defaults(func=cmd_version)

    st = sub.add_parser("status", help="Probe calculator CLIs on PATH")
    st.set_defaults(func=cmd_status)

    return p


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        # Default: stdio MCP
        raise SystemExit(cmd_stdio(argparse.Namespace()))
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
