# -*- coding: utf-8 -*-
"""Optional local-only FastAPI surface (bind 127.0.0.1). Not a remote API service."""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from . import __version__
from .runner import CliError, structured_error
from . import tools as T

app = FastAPI(
    title="mystilink-mcp local API",
    description=(
        "Local loopback helper for debugging Mystilink calculator orchestration. "
        "Intended bind: 127.0.0.1 only. Not a public HTTP/HTTPS service."
    ),
    version=__version__,
)


class LunarBody(BaseModel):
    timezone: str
    date: Optional[str] = None
    lunar: Optional[str] = None
    leap: bool = False
    time: Optional[str] = None
    profile: str = "lunar"
    year_boundary: Optional[str] = None
    month_boundary: Optional[str] = None
    day_boundary: Optional[str] = None
    explain: bool = False
    envelope: bool = True
    locale: Optional[str] = None


class BaziBody(BaseModel):
    date: Optional[str] = None
    hour: Optional[int] = None
    minute: int = 0
    timezone: Optional[str] = None
    longitude: Optional[float] = None
    birth_json: Optional[str] = None
    calendar_engine: str = "builtin"
    calendar_basis: Optional[str] = None
    envelope: bool = True
    locale: Optional[str] = None


class BaziDayunBody(BaseModel):
    date: str
    gender: str
    count: int = 8


class BaziLiunianBody(BaseModel):
    year: int
    day_stem: Optional[str] = None
    pillars_json: Optional[str] = None


class ZiweiBody(BaseModel):
    datetime_str: Optional[str] = Field(default=None, description="YYYY-MM-DD HH:MM")
    timezone: Optional[str] = None
    gender: Optional[str] = None
    midnight_zi: str = "same-day"
    si_hua: bool = False
    year: Optional[int] = None
    longitude: Optional[float] = None
    birth_json: Optional[str] = None
    calendar_engine: str = "builtin"
    calendar_basis: Optional[str] = None
    envelope: bool = True
    locale: Optional[str] = None


class HoroscopeBody(BaseModel):
    datetime_str: Optional[str] = None
    timezone: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    house_system: str = "P"
    zodiac: str = "tropical"
    sidereal_mode: str = "lahiri"
    true_solar_time: bool = False
    no_aspects: bool = False
    birth_json: Optional[str] = None
    envelope: bool = True
    locale: Optional[str] = None


class TarotBody(BaseModel):
    spread: str = "three-card"
    count: Optional[int] = None
    seed: Optional[int] = None
    envelope: bool = True
    locale: Optional[str] = None


class LiuyaoBody(BaseModel):
    seed: Optional[int] = None
    throws: Optional[str] = None
    envelope: bool = True
    locale: Optional[str] = None


def _invoke(fn, **kwargs: Any) -> Dict[str, Any]:
    try:
        clean = {k: v for k, v in kwargs.items() if v is not None}
        return fn(**clean)
    except CliError as exc:
        raise HTTPException(status_code=400, detail=structured_error(exc)["error"]) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=structured_error(exc)["error"]) from exc


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"ok": True, "name": "mystilink-mcp", "version": __version__, "bind": "127.0.0.1"}


@app.get("/v1/cli-status")
def cli_status() -> Dict[str, Any]:
    return _invoke(T.list_cli_status)


@app.post("/v1/lunar/convert")
def lunar_convert(body: LunarBody) -> Dict[str, Any]:
    return _invoke(T.lunar_convert, **body.model_dump())


@app.post("/v1/bazi/calculate")
def bazi_calculate(body: BaziBody) -> Dict[str, Any]:
    return _invoke(T.bazi_calculate, **body.model_dump())


@app.post("/v1/bazi/dayun")
def bazi_dayun(body: BaziDayunBody) -> Dict[str, Any]:
    return _invoke(T.bazi_dayun, **body.model_dump())


@app.post("/v1/bazi/liunian")
def bazi_liunian(body: BaziLiunianBody) -> Dict[str, Any]:
    return _invoke(T.bazi_liunian, **body.model_dump())


@app.post("/v1/ziwei/chart")
def ziwei_chart(body: ZiweiBody) -> Dict[str, Any]:
    return _invoke(T.ziwei_chart, **body.model_dump())


@app.post("/v1/horoscope/natal")
def horoscope_natal(body: HoroscopeBody) -> Dict[str, Any]:
    return _invoke(T.horoscope_natal, **body.model_dump())


@app.post("/v1/tarot/draw")
def tarot_draw(body: TarotBody) -> Dict[str, Any]:
    return _invoke(T.tarot_draw, **body.model_dump())


@app.post("/v1/liuyao/cast")
def liuyao_cast(body: LiuyaoBody) -> Dict[str, Any]:
    return _invoke(T.liuyao_cast, **body.model_dump())


def main() -> None:
    """Run local loopback API. Host is fixed to 127.0.0.1."""
    import os

    import uvicorn

    port = int(os.environ.get("MYSTILINK_MCP_LOCAL_PORT", "8765"))
    uvicorn.run(
        "mystilink_mcp.local_api:app",
        host="127.0.0.1",
        port=port,
        log_level="info",
    )


if __name__ == "__main__":
    main()
