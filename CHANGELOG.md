# Changelog

All notable changes to this repo are documented here. Format follows [Keep a Changelog](https://keepachangelog.com); this project adheres to [Semantic Versioning](https://semver.org).

## [Unreleased]

### Added

- **`/v1/markets/{ref}/context` now returns three new fields** (also via the `t_market_context` MCP tool): `market.implied_yes` (the market's own current implied YES probability), `market.resolution_criteria` (how the market resolves — source, metric, threshold), and a top-level `sibling_markets` array (correlated markets with `volume_usd` + `implied_yes`). One call now carries the market's own price + how it resolves + its correlated-market neighbors + the supporting signals. Opt out of siblings with `?sibling_markets=false`. See [`docs/api/markets-context.md`](docs/api/markets-context.md).
- `docs/quickstart/mcp.md` now covers 11 MCP clients: Claude Desktop, Claude Code, Cursor, Windsurf, Codex CLI, VS Code (Copilot), Cline / Roo Code, Zed, OpenClaw, Goose. Aider's lack of native MCP support is documented with community-bridge alternatives.
- Universal-footguns section in the MCP quickstart (stripped-PATH in desktop apps, schema-key differences across clients).

## [0.0.1] - 2026-05-27

### Added

- Four context endpoints: `/v1/markets/relevant-to`, `/v1/markets/{market_ref}/context`, `/v1/bundles/{bundle_ref}/context`, `/v1/events/{event_id}/related-markets`.
- Curated social watchlist (~5,400 high-signal accounts) gating which posts enter the context index.
- Machine-readable OpenAPI spec at repo root (`openapi.yaml`).
- Quickstart docs for `curl` and MCP setup under `docs/quickstart/`.
- API reference under `docs/api/`.
