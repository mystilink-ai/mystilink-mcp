# Changelog

## 0.1.1

- MCP tools / local API: `bazi_dayun`, `bazi_liunian` (`bazi dayun` / `bazi liunian`)
- Expect calculator chart `day_master` when using `bazi_calculate` with envelope

## 0.1.0

- stdio MCP tools: lunar / bazi / ziwei / horoscope / tarot / liuyao (+ status / version)
- Spawns short calculator CLIs; env overrides `MYSTILINK_*_CLI`
- Default `envelope=true` when calculators support `--envelope`
- Optional local FastAPI on `127.0.0.1` via `mystilink-mcp local-api` (extra `[local-api]`)
