# Mystilink MCP

> Languages: [English](../../README.md) | [简体中文](README.zh-CN.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md) | [Français](README.fr.md) | [Español](README.es.md)

[![Listed on mcpservers.org](https://mcpservers.org/badge.svg)](https://mcpservers.org/servers/mystilink-ai/mystilink-mcp.git)

## Aperçu

Intégration locale qui expose les CLI calculateurs Mystilink comme **outils MCP** (stdio) pour les hôtes Agent tels que Cursor. Peut aussi servir la même orchestration via **FastAPI en boucle locale sur `127.0.0.1`** pour le débogage local.

Ce paquet **ne calcule pas** de thèmes. Il lance les CLI courts installés (`bazi`, `ziwei`, `horoscope`, `lunar`, `tarot`, `liuyao`) et renvoie du JSON. Les réponses d’outils utilisent par défaut `mystilink.envelope/0.1` lorsque le calculateur prend en charge `--envelope`.

Il n’y a **pas de service HTTP/HTTPS distant** à déployer. L’entrée FastAPI est limitée à localhost.

## Type de livraison

Ce dépôt est un **paquet MCP / intégration locale**. Il n’implémente **pas** la matrice de langages C / C++ / C# / Java / JavaScript / Python des bibliothèques calculateurs.

## Prérequis

- Python 3.10+
- CLI calculateurs sur `PATH` (installer les paquets correspondants), ou définir les variables `MYSTILINK_*_CLI`

| Système | CLI court | Surcharge d’env |
|--------|-----------|--------------|
| lunar | `lunar` | `MYSTILINK_LUNAR_CLI` |
| bazi | `bazi` | `MYSTILINK_BAZI_CLI` |
| ziwei | `ziwei` | `MYSTILINK_ZIWEI_CLI` |
| horoscope | `horoscope` | `MYSTILINK_HOROSCOPE_CLI` |
| tarot | `tarot` | `MYSTILINK_TAROT_CLI` |
| liuyao | `liuyao` | `MYSTILINK_LIUYAO_CLI` |

## Installation

```bash
cd mystilink-mcp
python3 -m pip install -e .

# extras FastAPI locaux optionnels
python3 -m pip install -e '.[local-api]'
```

Sonde des CLI :

```bash
mystilink-mcp status
mystilink-mcp version
```

## MCP (stdio)

L’entrée par défaut démarre le serveur MCP sur stdio :

```bash
mystilink-mcp
# équivalent :
mystilink-mcp stdio
```

### Exemple de config MCP Cursor

Voir `examples/cursor-mcp.json`. Forme typique :

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

Assurez-vous que les CLI calculateurs sont sur le même `PATH` que le processus lancé par Cursor.

### Outils

| Tool | Calculateur |
|------|------------|
| `lunar_convert` | `lunar convert` |
| `bazi_calculate` | `bazi calculate` |
| `ziwei_chart` | `ziwei chart` |
| `horoscope_natal` | `horoscope natal` |
| `tarot_draw` | `tarot draw` |
| `liuyao_cast` | `liuyao cast` |
| `list_cli_status` | sonde PATH |
| `version` | version du paquet |

La plupart des outils de thème acceptent `envelope` (défaut `true`) et `locale` optionnel.

## FastAPI local (127.0.0.1 uniquement)

```bash
mystilink-mcp local-api
# écoute http://127.0.0.1:8765
# port : MYSTILINK_MCP_LOCAL_PORT=8765
```

| Méthode | Chemin |
|--------|------|
| GET | `/health` |
| GET | `/v1/cli-status` |
| POST | `/v1/lunar/convert` |
| POST | `/v1/bazi/calculate` |
| POST | `/v1/ziwei/chart` |
| POST | `/v1/horoscope/natal` |
| POST | `/v1/tarot/draw` |
| POST | `/v1/liuyao/cast` |

Exemple :

```bash
curl -s http://127.0.0.1:8765/health
curl -s -X POST http://127.0.0.1:8765/v1/tarot/draw \
  -H 'content-type: application/json' \
  -d '{"seed":123}'
```

## API Python

```python
from mystilink_mcp.tools import bazi_calculate, tarot_draw

chart = bazi_calculate(date="1990-05-15", hour=12, timezone="Asia/Shanghai")
draw = tarot_draw(seed=123)
```

## Limites

- Nécessite l’installation séparée des paquets / CLI calculateurs
- N’interprète pas les thèmes et n’appelle pas d’API produit Mystilink distantes
- L’hôte FastAPI local est figé sur `127.0.0.1`

## Licence

MIT. Voir [LICENSE](../../LICENSE).

## Retours

Signalez les problèmes avec : nom de l’outil, version CLI (`bazi version`, …), et une charge utile fictive minimale.
