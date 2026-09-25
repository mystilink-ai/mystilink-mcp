# Mystilink MCP

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

[![Listed on mcpservers.org](https://mcpservers.org/badge.svg)](https://mcpservers.org/servers/mystilink-ai/mystilink-mcp.git)

## Resumen

Integración local que expone las CLI de calculadoras Mystilink como **herramientas MCP** (stdio) para hosts Agent como Cursor. Opcionalmente sirve la misma orquestación con **FastAPI en bucle local en `127.0.0.1`** para depuración local.

Este paquete **no calcula** cartas. Lanza las CLI cortas instaladas (`bazi`, `ziwei`, `horoscope`, `lunar`, `tarot`, `liuyao`) y devuelve JSON. Las respuestas de herramientas usan por defecto `mystilink.envelope/0.1` cuando la calculadora admite `--envelope`.

**No hay servicio HTTP/HTTPS remoto** que desplegar. La entrada FastAPI es solo localhost.

## Puntos de acceso

- Agent: https://www.mystilink.com
- Wiki teórica: https://wiki.mystilink.com (API `/api/v1`)

## Tipo de entrega

Este repositorio es un **paquete MCP / integración local**. **No** implementa la matriz de lenguajes C / C++ / C# / Java / JavaScript / Python de las bibliotecas calculadoras.

## Requisitos

- Python 3.10+
- CLI de calculadoras en `PATH` (instale los paquetes correspondientes), o defina `MYSTILINK_*_CLI`

| Sistema | CLI corta | Anulación de env |
|--------|-----------|--------------|
| lunar | `lunar` | `MYSTILINK_LUNAR_CLI` |
| bazi | `bazi` | `MYSTILINK_BAZI_CLI` |
| ziwei | `ziwei` | `MYSTILINK_ZIWEI_CLI` |
| horoscope | `horoscope` | `MYSTILINK_HOROSCOPE_CLI` |
| tarot | `tarot` | `MYSTILINK_TAROT_CLI` |
| liuyao | `liuyao` | `MYSTILINK_LIUYAO_CLI` |

## Instalación

```bash
cd mystilink-mcp
python3 -m pip install -e .

# extras opcionales de FastAPI local
python3 -m pip install -e '.[local-api]'
```

Sondeo de CLI:

```bash
mystilink-mcp status
mystilink-mcp version
```

## MCP (stdio)

La entrada por defecto inicia el servidor MCP en stdio:

```bash
mystilink-mcp
# igual que:
mystilink-mcp stdio
```

### Ejemplo de config MCP de Cursor

Vea `examples/cursor-mcp.json`. Forma típica:

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

Asegúrese de que las CLI de calculadoras estén en el mismo `PATH` que el proceso que lanza Cursor.

### Herramientas

| Tool | Calculadora |
|------|------------|
| `lunar_convert` | `lunar convert` |
| `bazi_calculate` | `bazi calculate` |
| `bazi_dayun` | `bazi dayun` |
| `bazi_liunian` | `bazi liunian` |
| `ziwei_chart` | `ziwei chart` |
| `horoscope_natal` | `horoscope natal` |
| `tarot_draw` | `tarot draw` |
| `liuyao_cast` | `liuyao cast` |
| `list_cli_status` | sondeo PATH |
| `version` | versión del paquete |

La mayoría de las herramientas de carta aceptan `envelope` (predeterminado `true`) y `locale` opcional.

## FastAPI local (solo 127.0.0.1)

```bash
mystilink-mcp local-api
# escucha http://127.0.0.1:8765
# puerto: MYSTILINK_MCP_LOCAL_PORT=8765
```

| Método | Ruta |
|--------|------|
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

Ejemplo:

```bash
curl -s http://127.0.0.1:8765/health
curl -s -X POST http://127.0.0.1:8765/v1/tarot/draw \
  -H 'content-type: application/json' \
  -d '{"seed":123}'
```

## API de Python

```python
from mystilink_mcp.tools import bazi_calculate, tarot_draw

chart = bazi_calculate(date="1990-05-15", hour=12, timezone="Asia/Shanghai")
draw = tarot_draw(seed=123)
```

## Límites

- Requiere instalar por separado los paquetes / CLI de calculadoras
- No interpreta cartas ni llama a API de producto Mystilink remotas
- El host FastAPI local está fijado a `127.0.0.1`

## Licencia

MIT. Vea [LICENSE](../../LICENSE).

## Comentarios

Reporte problemas con: nombre de la herramienta, versión de CLI (`bazi version`, …) y una carga útil ficticia mínima.
