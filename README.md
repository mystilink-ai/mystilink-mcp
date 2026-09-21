# Mystilink MCP

> Languages: [English](README.md) | [简体中文](docs/i18n/README.zh-CN.md) | [繁體中文](docs/i18n/README.zh-TW.md) | [日本語](docs/i18n/README.ja.md) | [한국어](docs/i18n/README.ko.md) | [Français](docs/i18n/README.fr.md) | [Español](docs/i18n/README.es.md)

[![Listed on mcpservers.org](https://mcpservers.org/badge.svg)](https://mcpservers.org/servers/mystilink-ai/mystilink-mcp.git)

## Overview

Local integration that exposes Mystilink calculator CLIs as **MCP tools** (stdio) for Agent hosts such as Cursor. Optionally serves the same orchestration over **loopback FastAPI on `127.0.0.1`** for local debugging.

This package does **not** compute charts. It spawns installed short CLIs (`bazi`, `ziwei`, `horoscope`, `lunar`, `tarot`, `liuyao`) and returns JSON. Default tool responses use `mystilink.envelope/0.1` when the calculator supports `--envelope`.

There is **no remote HTTP/HTTPS service** to deploy. The FastAPI entry is localhost-only.

## Delivery type

This repository is an **MCP / local integration package**. It does **not** implement the C / C++ / C# / Java / JavaScript / Python language matrix used by calculator libraries.

## Requirements

- Python 3.10+
- Calculator CLIs on `PATH` (install the corresponding packages), or set `MYSTILINK_*_CLI` env vars

| System | Short CLI | Env override |
|--------|-----------|--------------|
| lunar | `lunar` | `MYSTILINK_LUNAR_CLI` |
| bazi | `bazi` | `MYSTILINK_BAZI_CLI` |
| ziwei | `ziwei` | `MYSTILINK_ZIWEI_CLI` |
| horoscope | `horoscope` | `MYSTILINK_HOROSCOPE_CLI` |
| tarot | `tarot` | `MYSTILINK_TAROT_CLI` |
| liuyao | `liuyao` | `MYSTILINK_LIUYAO_CLI` |

## Install

```bash
cd mystilink-mcp
python3 -m pip install -e .

# optional local FastAPI extras
python3 -m pip install -e '.[local-api]'
```

Probe CLIs:

```bash
mystilink-mcp status
mystilink-mcp version
```

## MCP (stdio)

Default entry starts the MCP server on stdio:

```bash
mystilink-mcp
# same as:
mystilink-mcp stdio
```

### Cursor MCP config example

See `examples/cursor-mcp.json`. Typical shape:

```json
{
  "mcpServers": {
    "mystilink": {
      "command": "mystilink-mcp",
      "args": ["stdio"]
    }
  }
}
```

Ensure calculator CLIs are on the same `PATH` as the process Cursor launches.

### Tools

| Tool | Calculator |
|------|------------|
| `lunar_convert` | `lunar convert` |
| `bazi_calculate` | `bazi calculate` |
| `ziwei_chart` | `ziwei chart` |
| `horoscope_natal` | `horoscope natal` |
| `tarot_draw` | `tarot draw` |
| `liuyao_cast` | `liuyao cast` |
| `list_cli_status` | PATH probe |
| `version` | package version |

Most chart tools accept `envelope` (default `true`) and optional `locale`.

## Local FastAPI (127.0.0.1 only)

```bash
mystilink-mcp local-api
# listens on http://127.0.0.1:8765
# override port: MYSTILINK_MCP_LOCAL_PORT=8765
```

| Method | Path |
|--------|------|
| GET | `/health` |
| GET | `/v1/cli-status` |
| POST | `/v1/lunar/convert` |
| POST | `/v1/bazi/calculate` |
| POST | `/v1/ziwei/chart` |
| POST | `/v1/horoscope/natal` |
| POST | `/v1/tarot/draw` |
| POST | `/v1/liuyao/cast` |

Example:

```bash
curl -s http://127.0.0.1:8765/health
curl -s -X POST http://127.0.0.1:8765/v1/tarot/draw \
  -H 'content-type: application/json' \
  -d '{"seed":123}'
```

## Python API

```python
from mystilink_mcp.tools import bazi_calculate, tarot_draw

chart = bazi_calculate(date="1990-05-15", hour=12, timezone="Asia/Shanghai")
draw = tarot_draw(seed=123)
```

## Limits

- Requires separately installed calculator packages / CLIs
- Does not interpret charts or call remote Mystilink product APIs
- Local FastAPI host is hardcoded to `127.0.0.1`

## License

MIT. See [LICENSE](LICENSE).

## Feedback

Report issues with: tool name, CLI version (`bazi version`, …), and a minimal fictional payload.
