# Mystilink MCP

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

[![Listed on mcpservers.org](https://mcpservers.org/badge.svg)](https://mcpservers.org/servers/mystilink-ai/mystilink-mcp.git)

## 概述

本地整合套件：把 Mystilink 計算器 CLI 暴露為 **MCP tools**（stdio），供 Cursor 等 Agent 宿主呼叫。可選在 **`127.0.0.1` 上提供本機 FastAPI**，便於本地除錯。

本套件**不排盤**。它只 spawn 已安裝的短命令（`bazi`、`ziwei`、`horoscope`、`lunar`、`tarot`、`liuyao`）並回傳 JSON。計算器支援時，預設帶 `--envelope`（`mystilink.envelope/0.1`）。

**不提供**對外 http/https 遠端服務。FastAPI 入口僅本機迴路。

## 相關位址

- Agent：https://www.mystilink.com
- 理論 Wiki：https://wiki.mystilink.com（API `/api/v1`）

## 交付類型

本倉庫為 **MCP / 本地整合套件**。**不適用**計算器倉庫的 C / C++ / C# / Java / JavaScript / Python 語言矩陣。

## 環境需求

- Python 3.10+
- 計算器 CLI 在 `PATH` 上（安裝對應套件），或設定 `MYSTILINK_*_CLI`

| 體系 | 短 CLI | 環境變數覆蓋 |
|------|--------|--------------|
| lunar | `lunar` | `MYSTILINK_LUNAR_CLI` |
| bazi | `bazi` | `MYSTILINK_BAZI_CLI` |
| ziwei | `ziwei` | `MYSTILINK_ZIWEI_CLI` |
| horoscope | `horoscope` | `MYSTILINK_HOROSCOPE_CLI` |
| tarot | `tarot` | `MYSTILINK_TAROT_CLI` |
| liuyao | `liuyao` | `MYSTILINK_LIUYAO_CLI` |

## 安裝

```bash
cd mystilink-mcp
python3 -m pip install -e .

# 可選本機 FastAPI 依賴
python3 -m pip install -e '.[local-api]'
```

探測 CLI：

```bash
mystilink-mcp status
mystilink-mcp version
```

## MCP（stdio）

預設入口啟動 stdio MCP：

```bash
mystilink-mcp
# 等價：
mystilink-mcp stdio
```

### Cursor MCP 設定範例

見 `examples/cursor-mcp.json`。典型寫法：

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

確保 Cursor 拉起行程時的 `PATH` 能找到各計算器 CLI。

### Tools

| Tool | 計算器 |
|------|--------|
| `lunar_convert` | `lunar convert` |
| `bazi_calculate` | `bazi calculate` |
| `bazi_dayun` | `bazi dayun` |
| `bazi_liunian` | `bazi liunian` |
| `ziwei_chart` | `ziwei chart` |
| `horoscope_natal` | `horoscope natal` |
| `tarot_draw` | `tarot draw` |
| `liuyao_cast` | `liuyao cast` |
| `list_cli_status` | PATH 探測 |
| `version` | 套件版本 |

多數排盤 tool 接受 `envelope`（預設 `true`）與可選 `locale`。

## 本機 FastAPI（僅 127.0.0.1）

```bash
mystilink-mcp local-api
# 監聽 http://127.0.0.1:8765
# 改埠：MYSTILINK_MCP_LOCAL_PORT=8765
```

| 方法 | 路徑 |
|------|------|
| GET | `/health` |
| GET | `/v1/cli-status` |
| POST | `/v1/lunar/convert` |
| POST | `/v1/bazi/calculate` |
| POST | `/v1/bazi/dayun` |
| POST | `/v1/bazi/liunian` |
| POST | `/v1/ziwei/chart` |
| POST | `/v1/horoscope/natal` |
| POST | `/v1/tarot/draw` |
| POST | `/v1/liuyao/cast` |

範例：

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

## 限制

- 需單獨安裝各計算器套件 / CLI
- 不做盤面解讀，不呼叫遠端 Mystilink 產品 API
- 本機 FastAPI 固定綁定 `127.0.0.1`

## 授權

MIT。見 [LICENSE](../../LICENSE)。

## 回饋

回饋時請附：tool 名、對應 CLI 版本（如 `bazi version`）、最小虛構入參。
