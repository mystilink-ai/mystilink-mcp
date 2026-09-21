# Mystilink MCP

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

[![Listed on mcpservers.org](https://mcpservers.org/badge.svg)](https://mcpservers.org/servers/mystilink-ai/mystilink-mcp.git)

## 개요

로컬 통합 패키지: Mystilink 계산기 CLI를 **MCP tools**(stdio)로 노출하여 Cursor 등 Agent 호스트에서 호출합니다. 선택적으로 **`127.0.0.1` 루프백 FastAPI**를 제공해 로컬 디버깅에 사용할 수 있습니다.

이 패키지는 **배반하지 않습니다**. 설치된 짧은 CLI(`bazi`, `ziwei`, `horoscope`, `lunar`, `tarot`, `liuyao`)를 spawn하고 JSON을 반환합니다. 계산기가 지원하면 기본으로 `--envelope`(`mystilink.envelope/0.1`)를 붙입니다.

외부 http/https 원격 서비스는 **제공하지 않습니다**. FastAPI 진입점은 localhost만입니다.

## 제공 유형

이 저장소는 **MCP / 로컬 통합 패키지**입니다. 계산기 저장소의 C / C++ / C# / Java / JavaScript / Python 언어 매트릭스는 **적용하지 않습니다**.

## 요구 사항

- Python 3.10+
- 계산기 CLI가 `PATH`에 있어야 함(해당 패키지 설치), 또는 `MYSTILINK_*_CLI` 설정

| 체계 | 짧은 CLI | 환경 변수 덮어쓰기 |
|------|--------|--------------|
| lunar | `lunar` | `MYSTILINK_LUNAR_CLI` |
| bazi | `bazi` | `MYSTILINK_BAZI_CLI` |
| ziwei | `ziwei` | `MYSTILINK_ZIWEI_CLI` |
| horoscope | `horoscope` | `MYSTILINK_HOROSCOPE_CLI` |
| tarot | `tarot` | `MYSTILINK_TAROT_CLI` |
| liuyao | `liuyao` | `MYSTILINK_LIUYAO_CLI` |

## 설치

```bash
cd mystilink-mcp
python3 -m pip install -e .

# 선택적 로컬 FastAPI 의존성
python3 -m pip install -e '.[local-api]'
```

CLI 확인:

```bash
mystilink-mcp status
mystilink-mcp version
```

## MCP(stdio)

기본 진입점은 stdio MCP를 시작합니다:

```bash
mystilink-mcp
# 동일:
mystilink-mcp stdio
```

### Cursor MCP 설정 예

`examples/cursor-mcp.json` 참고. 일반적인 형태:

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

Cursor가 띄운 프로세스의 `PATH`에서 각 계산기 CLI를 찾을 수 있어야 합니다.

### Tools

| Tool | 계산기 |
|------|--------|
| `lunar_convert` | `lunar convert` |
| `bazi_calculate` | `bazi calculate` |
| `ziwei_chart` | `ziwei chart` |
| `horoscope_natal` | `horoscope natal` |
| `tarot_draw` | `tarot draw` |
| `liuyao_cast` | `liuyao cast` |
| `list_cli_status` | PATH 확인 |
| `version` | 패키지 버전 |

대부분의 배반 tool은 `envelope`(기본 `true`)와 선택적 `locale`을 받습니다.

## 로컬 FastAPI(127.0.0.1만)

```bash
mystilink-mcp local-api
# 수신 http://127.0.0.1:8765
# 포트 변경: MYSTILINK_MCP_LOCAL_PORT=8765
```

| 메서드 | 경로 |
|------|------|
| GET | `/health` |
| GET | `/v1/cli-status` |
| POST | `/v1/lunar/convert` |
| POST | `/v1/bazi/calculate` |
| POST | `/v1/ziwei/chart` |
| POST | `/v1/horoscope/natal` |
| POST | `/v1/tarot/draw` |
| POST | `/v1/liuyao/cast` |

예:

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

## 제한

- 계산기 패키지 / CLI를 별도로 설치해야 함
- 차트 해석이나 원격 Mystilink 제품 API 호출은 하지 않음
- 로컬 FastAPI 호스트는 `127.0.0.1` 고정

## 라이선스

MIT. [LICENSE](../../LICENSE) 참고.

## 피드백

보고 시: tool 이름, 해당 CLI 버전(예: `bazi version`), 최소 가상의 페이로드를 첨부하세요.
