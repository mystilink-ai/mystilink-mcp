# -*- coding: utf-8 -*-
"""Local FastAPI loopback tests."""
from __future__ import annotations

import shutil

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient

from mystilink_mcp.local_api import app


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


def test_health(client: TestClient) -> None:
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["bind"] == "127.0.0.1"


@pytest.mark.skipif(not shutil.which("tarot") and not shutil.which("mystilink-tarot"), reason="tarot missing")
def test_tarot_endpoint(client: TestClient) -> None:
    r = client.post("/v1/tarot/draw", json={"seed": 123})
    assert r.status_code == 200
    data = r.json()
    assert data["system"] == "tarot"
