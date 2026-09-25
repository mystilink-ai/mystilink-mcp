# -*- coding: utf-8 -*-
"""MCP stdio server: exposes Mystilink calculator tools to local hosts."""
from __future__ import annotations

import json
from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP

from . import __version__
from .runner import CliError, structured_error
from . import tools as T

mcp = FastMCP(
    "mystilink-mcp",
    instructions=(
        "Mystilink local MCP. Tools spawn installed calculator CLIs "
        "(bazi/ziwei/horoscope/lunar/tarot/liuyao) and return JSON. "
        "Default envelope=true wraps results as mystilink.envelope/0.1. "
        "This server does not compute charts itself."
    ),
)


def _call(fn, **kwargs: Any) -> str:
    """Run a tool and return JSON text for the MCP host."""
    try:
        # Drop None values so defaults apply in tools layer where needed
        clean = {k: v for k, v in kwargs.items() if v is not None}
        result = fn(**clean)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except CliError as exc:
        return json.dumps(structured_error(exc), ensure_ascii=False, indent=2)
    except Exception as exc:  # noqa: BLE001
        return json.dumps(structured_error(exc), ensure_ascii=False, indent=2)


@mcp.tool()
def lunar_convert(
    timezone: str,
    date: Optional[str] = None,
    lunar: Optional[str] = None,
    leap: bool = False,
    time: Optional[str] = None,
    profile: str = "lunar",
    year_boundary: Optional[str] = None,
    month_boundary: Optional[str] = None,
    day_boundary: Optional[str] = None,
    explain: bool = False,
    envelope: bool = True,
    locale: Optional[str] = None,
) -> str:
    """Convert Gregorian↔lunar and return ganzhi / calendar basis JSON via `lunar` CLI."""
    return _call(
        T.lunar_convert,
        timezone=timezone,
        date=date,
        lunar=lunar,
        leap=leap,
        time=time,
        profile=profile,
        year_boundary=year_boundary,
        month_boundary=month_boundary,
        day_boundary=day_boundary,
        explain=explain,
        envelope=envelope,
        locale=locale,
    )


@mcp.tool()
def bazi_calculate(
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
) -> str:
    """Compute BaZi four pillars via `bazi` CLI. Prefer BirthProfile JSON in birth_json when available."""
    return _call(
        T.bazi_calculate,
        date=date,
        hour=hour,
        minute=minute,
        timezone=timezone,
        longitude=longitude,
        birth_json=birth_json,
        calendar_engine=calendar_engine,
        calendar_basis=calendar_basis,
        envelope=envelope,
        locale=locale,
    )


@mcp.tool()
def bazi_dayun(
    date: str,
    gender: str,
    count: int = 8,
) -> str:
    """Compute BaZi decade fortunes (DaYun) via `bazi dayun`. gender is male|female."""
    return _call(T.bazi_dayun, date=date, gender=gender, count=count)


@mcp.tool()
def bazi_liunian(
    year: int,
    day_stem: Optional[str] = None,
    pillars_json: Optional[str] = None,
) -> str:
    """Compute BaZi annual fortune (LiuNian) via `bazi liunian`."""
    return _call(
        T.bazi_liunian,
        year=year,
        day_stem=day_stem,
        pillars_json=pillars_json,
    )


@mcp.tool()
def ziwei_chart(
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
) -> str:
    """Compute Zi Wei Dou Shu chart via `ziwei` CLI. datetime_str format: YYYY-MM-DD HH:MM."""
    return _call(
        T.ziwei_chart,
        datetime_str=datetime_str,
        timezone=timezone,
        gender=gender,
        midnight_zi=midnight_zi,
        si_hua=si_hua,
        year=year,
        longitude=longitude,
        birth_json=birth_json,
        calendar_engine=calendar_engine,
        calendar_basis=calendar_basis,
        envelope=envelope,
        locale=locale,
    )


@mcp.tool()
def horoscope_natal(
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
) -> str:
    """Compute natal chart via `horoscope` CLI. Requires lat/lon or BirthProfile place."""
    return _call(
        T.horoscope_natal,
        datetime_str=datetime_str,
        timezone=timezone,
        lat=lat,
        lon=lon,
        house_system=house_system,
        zodiac=zodiac,
        sidereal_mode=sidereal_mode,
        true_solar_time=true_solar_time,
        no_aspects=no_aspects,
        birth_json=birth_json,
        envelope=envelope,
        locale=locale,
    )


@mcp.tool()
def tarot_draw(
    spread: str = "three-card",
    count: Optional[int] = None,
    seed: Optional[int] = None,
    envelope: bool = True,
    locale: Optional[str] = None,
) -> str:
    """Draw RWS tarot cards via `tarot` CLI. Pass seed for deterministic draws."""
    return _call(
        T.tarot_draw,
        spread=spread,
        count=count,
        seed=seed,
        envelope=envelope,
        locale=locale,
    )


@mcp.tool()
def liuyao_cast(
    seed: Optional[int] = None,
    throws: Optional[str] = None,
    envelope: bool = True,
    locale: Optional[str] = None,
) -> str:
    """Cast six lines via `liuyao` CLI. throws is six values in {6,7,8,9}, e.g. '9,8,7,6,8,9'."""
    return _call(
        T.liuyao_cast,
        seed=seed,
        throws=throws,
        envelope=envelope,
        locale=locale,
    )


@mcp.tool()
def list_cli_status() -> str:
    """List which Mystilink calculator CLIs are available on PATH."""
    return _call(T.list_cli_status)


@mcp.tool()
def version() -> str:
    """Return mystilink-mcp package version."""
    return json.dumps(
        {"name": "mystilink-mcp", "version": __version__, "transport": "stdio"},
        ensure_ascii=False,
        indent=2,
    )


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
