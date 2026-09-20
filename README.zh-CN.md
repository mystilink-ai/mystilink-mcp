# Mystilink MCP

> Languages: [English](README.md) | [简体中文](README.zh-CN.md)

## 概述

本地集成包：把 Mystilink 计算器 CLI 暴露为 **MCP tools**（stdio），供 Cursor 等 Agent 宿主调用。可选在 **`127.0.0.1` 上提供本机 FastAPI**，便于本地调试。

本包**不排盘**。它只 spawn 已安装的短命令（`bazi`、`ziwei`、`horoscope`、`lunar`、`tarot`、`liuyao`）并返回 JSON。计算器支持时，默认带 `--envelope`（`mystilink.envelope/0.1`）。

**不提供**对外 http/https 远程服务。FastAPI 入口仅本机回环。

## 交付类型

本仓库为 **MCP / 本地集成包**。**不适用**计算器仓库的 C / C++ / C# / Java / JavaScript / Python 语言矩阵。

## 环境要求

- Python 3.10+
- 计算器 CLI 在 `PATH` 上（安装对应包），或设置 `MYSTILINK_*_CLI`

| 体系 | 短 CLI | 环境变量覆盖 |
|------|--------|--------------|
| lunar | `lunar` | `MYSTILINK_LUNAR_CLI` |
| bazi | `bazi` | `MYSTILINK_BAZI_CLI` |
| ziwei | `ziwei` | `MYSTILINK_ZIWEI_CLI` |
| horoscope | `horoscope` | `MYSTILINK_HOROSCOPE_CLI` |
| tarot | `tarot` | `MYSTILINK_TAROT_CLI` |
| liuyao | `liuyao` | `MYSTILINK_LIUYAO_CLI` |

## 安装

```bash
cd mystilink-mcp
python3 -m pip install -e .

# 可选本机 FastAPI 依赖
python3 -m pip install -e '.[local-api]'
```

探测 CLI：

```bash
mystilink-mcp status
mystilink-mcp version
```

## MCP（stdio）

默认入口启动 stdio MCP：

```bash
mystilink-mcp
# 等价：
mystilink-mcp stdio
```

### Cursor MCP 配置示例

见 `examples/cursor-mcp.json`。典型写法：

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

确保 Cursor 拉起进程时的 `PATH` 能找到各计算器 CLI。

### Tools

| Tool | 计算器 |
|------|--------|
| `lunar_convert` | `lunar convert` |
| `bazi_calculate` | `bazi calculate` |
| `ziwei_chart` | `ziwei chart` |
| `horoscope_natal` | `horoscope natal` |
| `tarot_draw` | `tarot draw` |
| `liuyao_cast` | `liuyao cast` |
| `list_cli_status` | PATH 探测 |
| `version` | 包版本 |

多数排盘 tool 接受 `envelope`（默认 `true`）与可选 `locale`。

## 本机 FastAPI（仅 127.0.0.1）

```bash
mystilink-mcp local-api
# 监听 http://127.0.0.1:8765
# 改端口：MYSTILINK_MCP_LOCAL_PORT=8765
```

| 方法 | 路径 |
|------|------|
| GET | `/health` |
| GET | `/v1/cli-status` |
| POST | `/v1/lunar/convert` |
| POST | `/v1/bazi/calculate` |
| POST | `/v1/ziwei/chart` |
| POST | `/v1/horoscope/natal` |
| POST | `/v1/tarot/draw` |
| POST | `/v1/liuyao/cast` |

示例：

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

- 需单独安装各计算器包 / CLI
- 不做盘面解读，不调用远程 Mystilink 产品 API
- 本机 FastAPI 固定绑定 `127.0.0.1`

## 许可

MIT。见 [LICENSE](LICENSE)。

## 反馈

反馈时请附：tool 名、对应 CLI 版本（如 `bazi version`）、最小虚构入参。
