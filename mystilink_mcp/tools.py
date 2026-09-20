# -*- coding: utf-8 -*-
"""Build CLI argv for each Mystilink calculator tool."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from .runner import CliError, run_cli


def _flag(args: List[str], name: str, value: Any) -> None:
    if value is None:
        return
    if isinstance(value, bool):
        if value:
            args.append(name)
        return
    args.extend([name, str(value)])


def lunar_convert(
    *,
    date: Optional[str] = None,
    lunar: Optional[str] = None,
    leap: bool = False,
    time: Optional[str] = None,
    timezone: str,
    profile: str = "lunar",
    year_boundary: Optional[str] = None,
    month_boundary: Optional[str] = None,
    day_boundary: Optional[str] = None,
    explain: bool = False,
    envelope: bool = True,
    locale: Optional[str] = None,
) -> Dict[str, Any]:
    if not date and not lunar:
        raise CliError("provide date or lunar (YYYY-MM-DD)", code="invalid_args")
    args: List[str] = ["convert", "--timezone", timezone, "--profile", profile]
    _flag(args, "--date", date)
    _flag(args, "--lunar", lunar)
    _flag(args, "--leap", leap)
    _flag(args, "--time", time)
    _flag(args, "--year-boundary", year_boundary)
    _flag(args, "--month-boundary", month_boundary)
    _flag(args, "--day-boundary", day_boundary)
    _flag(args, "--explain", explain)
    if envelope:
        args.append("--envelope")
        _flag(args, "--locale", locale)
    else:
        args.append("--json")
    return run_cli("lunar", args)


def bazi_calculate(
    *,
    date: Optional[str] = None,
    hour: Optional[int] = None,
    minute: int = 0,
    timezone: Optional[str] = None,
    longitude: Optional[float] = None,
    birth_json: Optional[str] = None,
    calendar_engine: str = "builtin",
    calendar_basis: Optional[str] = None,
    envelope: bool = True,
    locale: Optional[str] = None,
) -> Dict[str, Any]:
    args: List[str] = ["calculate", "--calendar-engine", calendar_engine]
    _flag(args, "--date", date)
    if hour is not None:
        args.extend(["--hour", str(hour)])
    args.extend(["--minute", str(minute)])
    _flag(args, "--timezone", timezone)
    _flag(args, "--longitude", longitude)
    _flag(args, "--birth-json", birth_json)
    _flag(args, "--calendar-basis", calendar_basis)
    if envelope:
        args.append("--envelope")
        _flag(args, "--locale", locale)
    return run_cli("bazi", args)


def ziwei_chart(
    *,
    datetime_str: Optional[str] = None,
    timezone: Optional[str] = None,
    gender: Optional[str] = None,
    midnight_zi: str = "same-day",
    si_hua: bool = False,
    year: Optional[int] = None,
    longitude: Optional[float] = None,
    birth_json: Optional[str] = None,
    calendar_engine: str = "builtin",
    calendar_basis: Optional[str] = None,
    envelope: bool = True,
    locale: Optional[str] = None,
) -> Dict[str, Any]:
    args: List[str] = ["chart", "--midnight-zi", midnight_zi, "--calendar-engine", calendar_engine]
    _flag(args, "--datetime", datetime_str)
    _flag(args, "--timezone", timezone)
    _flag(args, "--gender", gender)
    _flag(args, "--si-hua", si_hua)
    _flag(args, "--year", year)
    _flag(args, "--longitude", longitude)
    _flag(args, "--birth-json", birth_json)
    _flag(args, "--calendar-basis", calendar_basis)
    if envelope:
        args.append("--envelope")
        _flag(args, "--locale", locale)
    return run_cli("ziwei", args)


def horoscope_natal(
    *,
    datetime_str: Optional[str] = None,
    timezone: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    house_system: str = "P",
    zodiac: str = "tropical",
    sidereal_mode: str = "lahiri",
    true_solar_time: bool = False,
    no_aspects: bool = False,
    birth_json: Optional[str] = None,
    envelope: bool = True,
    locale: Optional[str] = None,
) -> Dict[str, Any]:
    args: List[str] = [
        "natal",
        "--house-system",
        house_system,
        "--zodiac",
        zodiac,
        "--sidereal-mode",
        sidereal_mode,
    ]
    _flag(args, "--datetime", datetime_str)
    _flag(args, "--timezone", timezone)
    _flag(args, "--lat", lat)
    _flag(args, "--lon", lon)
    _flag(args, "--true-solar-time", true_solar_time)
    _flag(args, "--no-aspects", no_aspects)
    _flag(args, "--birth-json", birth_json)
    if envelope:
        args.append("--envelope")
        _flag(args, "--locale", locale)
    return run_cli("horoscope", args)


def tarot_draw(
    *,
    spread: str = "three-card",
    count: Optional[int] = None,
    seed: Optional[int] = None,
    envelope: bool = True,
    locale: Optional[str] = None,
) -> Dict[str, Any]:
    args: List[str] = ["draw", "--spread", spread]
    _flag(args, "--count", count)
    _flag(args, "--seed", seed)
    if envelope:
        args.append("--envelope")
        _flag(args, "--locale", locale)
    return run_cli("tarot", args)


def liuyao_cast(
    *,
    seed: Optional[int] = None,
    throws: Optional[str] = None,
    envelope: bool = True,
    locale: Optional[str] = None,
) -> Dict[str, Any]:
    args: List[str] = ["cast"]
    _flag(args, "--seed", seed)
    _flag(args, "--throws", throws)
    if envelope:
        args.append("--envelope")
        _flag(args, "--locale", locale)
    return run_cli("liuyao", args)


def list_cli_status() -> Dict[str, Any]:
    """Probe which calculator CLIs are resolvable."""
    from .runner import CLI_CANDIDATES, resolve_cli

    out: Dict[str, Any] = {}
    for system in CLI_CANDIDATES:
        try:
            out[system] = {"ok": True, "path": resolve_cli(system)}
        except CliError as exc:
            out[system] = {"ok": False, "error": str(exc)}
    return out


TOOLS = (
    lunar_convert,
    bazi_calculate,
    ziwei_chart,
    horoscope_natal,
    tarot_draw,
    liuyao_cast,
    list_cli_status,
)

__all__ = [
    "lunar_convert",
    "bazi_calculate",
    "ziwei_chart",
    "horoscope_natal",
    "tarot_draw",
    "liuyao_cast",
    "list_cli_status",
    "TOOLS",
]
