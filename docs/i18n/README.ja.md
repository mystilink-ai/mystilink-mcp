# Mystilink MCP

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

[![Listed on mcpservers.org](https://mcpservers.org/badge.svg)](https://mcpservers.org/servers/mystilink-ai/mystilink-mcp.git)

## 概要

ローカル統合パッケージ：Mystilink 計算機 CLI を **MCP tools**（stdio）として公開し、Cursor などの Agent ホストから呼び出します。任意で **`127.0.0.1` 上のループバック FastAPI** を提供し、ローカルデバッグに使えます。

本パッケージは**排盤しません**。インストール済みの短い CLI（`bazi`、`ziwei`、`horoscope`、`lunar`、`tarot`、`liuyao`）を spawn して JSON を返します。計算機が対応する場合、既定で `--envelope`（`mystilink.envelope/0.1`）を付けます。

外部向け http/https リモートサービスは**提供しません**。FastAPI 入口は localhost のみです。

## デリバリ種別

本リポジトリは **MCP / ローカル統合パッケージ**です。計算機リポジトリの C / C++ / C# / Java / JavaScript / Python 言語マトリクスは**適用しません**。

## 要件

- Python 3.10+
- 計算機 CLI が `PATH` 上にあること（対応パッケージをインストール）、または `MYSTILINK_*_CLI` を設定

| 体系 | 短い CLI | 環境変数上書き |
|------|--------|--------------|
| lunar | `lunar` | `MYSTILINK_LUNAR_CLI` |
| bazi | `bazi` | `MYSTILINK_BAZI_CLI` |
| ziwei | `ziwei` | `MYSTILINK_ZIWEI_CLI` |
| horoscope | `horoscope` | `MYSTILINK_HOROSCOPE_CLI` |
| tarot | `tarot` | `MYSTILINK_TAROT_CLI` |
| liuyao | `liuyao` | `MYSTILINK_LIUYAO_CLI` |

## インストール

```bash
cd mystilink-mcp
python3 -m pip install -e .

# 任意のローカル FastAPI 依存
python3 -m pip install -e '.[local-api]'
```

CLI を確認：

```bash
mystilink-mcp status
mystilink-mcp version
```

## MCP（stdio）

既定エントリは stdio MCP を起動します：

```bash
mystilink-mcp
# 同等：
mystilink-mcp stdio
```

### Cursor MCP 設定例

`examples/cursor-mcp.json` を参照。典型的な形：

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

Cursor が起動するプロセスの `PATH` で各計算機 CLI を見つけられるようにしてください。

### Tools

| Tool | 計算機 |
|------|--------|
| `lunar_convert` | `lunar convert` |
| `bazi_calculate` | `bazi calculate` |
| `ziwei_chart` | `ziwei chart` |
| `horoscope_natal` | `horoscope natal` |
| `tarot_draw` | `tarot draw` |
| `liuyao_cast` | `liuyao cast` |
| `list_cli_status` | PATH 確認 |
| `version` | パッケージ版 |

大半の排盤 tool は `envelope`（既定 `true`）と任意の `locale` を受け付けます。

## ローカル FastAPI（127.0.0.1 のみ）

```bash
mystilink-mcp local-api
# 待受 http://127.0.0.1:8765
# ポート変更：MYSTILINK_MCP_LOCAL_PORT=8765
```

| メソッド | パス |
|------|------|
| GET | `/health` |
| GET | `/v1/cli-status` |
| POST | `/v1/lunar/convert` |
| POST | `/v1/bazi/calculate` |
| POST | `/v1/ziwei/chart` |
| POST | `/v1/horoscope/natal` |
| POST | `/v1/tarot/draw` |
| POST | `/v1/liuyao/cast` |

例：

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

## 制限

- 計算機パッケージ / CLI を別途インストールする必要がある
- 盤面の解釈やリモート Mystilink 製品 API 呼び出しは行わない
- ローカル FastAPI のホストは `127.0.0.1` 固定

## ライセンス

MIT。[LICENSE](../../LICENSE) を参照。

## フィードバック

報告時は：tool 名、対応 CLI 版（例：`bazi version`）、最小の架空ペイロードを添えてください。
