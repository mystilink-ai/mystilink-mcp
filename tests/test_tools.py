# -*- coding: utf-8 -*-
"""Tests for CLI resolution and tool orchestration."""
from __future__ import annotations

import json
import shutil

import pytest

from mystilink_mcp.runner import CliError, resolve_cli, structured_error
from mystilink_mcp.tools import (
    bazi_calculate,
    list_cli_status,
    liuyao_cast,
    lunar_convert,
    tarot_draw,
    ziwei_chart,
)


def test_resolve_short_cli() -> None:
    if not shutil.which("bazi") and not shutil.which("mystilink-bazi"):
        pytest.skip("bazi CLI not installed")
    path = resolve_cli("bazi")
    assert path


def test_list_cli_status_shape() -> None:
    status = list_cli_status()
    assert "bazi" in status
    assert "ok" in status["bazi"]


@pytest.mark.skipif(not shutil.which("tarot") and not shutil.which("mystilink-tarot"), reason="tarot missing")
def test_tarot_draw_envelope() -> None:
    out = tarot_draw(seed=123, envelope=True)
    assert out["schema_version"] == "mystilink.envelope/0.1"
    assert out["system"] == "tarot"
    assert "chart" in out


@pytest.mark.skipif(not shutil.which("liuyao") and not shutil.which("mystilink-liuyao"), reason="liuyao missing")
def test_liuyao_cast_envelope() -> None:
    out = liuyao_cast(seed=123, envelope=True)
    assert out["schema_version"] == "mystilink.envelope/0.1"
    assert out["system"] == "liuyao"


@pytest.mark.skipif(not shutil.which("bazi") and not shutil.which("mystilink-bazi"), reason="bazi missing")
def test_bazi_calculate_envelope() -> None:
    out = bazi_calculate(date="1990-05-15", hour=12, timezone="Asia/Shanghai", envelope=True)
    assert out["schema_version"] == "mystilink.envelope/0.1"
    assert out["system"] == "bazi"
    assert "chart" in out


@pytest.mark.skipif(not shutil.which("lunar") and not shutil.which("mystilink-lunar"), reason="lunar missing")
def test_lunar_convert_envelope() -> None:
    out = lunar_convert(date="1990-05-15", time="12:00", timezone="Asia/Shanghai", envelope=True)
    assert out["schema_version"] == "mystilink.envelope/0.1"
    assert out["system"] == "lunar"


@pytest.mark.skipif(not shutil.which("ziwei") and not shutil.which("mystilink-ziwei"), reason="ziwei missing")
def test_ziwei_chart_envelope() -> None:
    out = ziwei_chart(
        datetime_str="1990-05-15 14:30",
        timezone="Asia/Shanghai",
        gender="male",
        envelope=True,
    )
    assert out["schema_version"] == "mystilink.envelope/0.1"
    assert out["system"] == "ziwei"


def test_structured_error() -> None:
    err = structured_error(CliError("missing", code="cli_not_found"))
    assert err["error"]["code"] == "cli_not_found"
    assert "missing" in err["error"]["message"]


def test_unknown_system() -> None:
    with pytest.raises(CliError, match="unknown system"):
        resolve_cli("not-a-system")
