# Changelog

All notable changes to this repo are documented here. Format follows [Keep a Changelog](https://keepachangelog.com); this project adheres to [Semantic Versioning](https://semver.org).

## [Unreleased]

### Added

- `docs/quickstart/mcp.md` now covers 11 MCP clients: Claude Desktop, Claude Code, Cursor, Windsurf, Codex CLI, VS Code (Copilot), Cline / Roo Code, Zed, OpenClaw, Goose. Aider's lack of native MCP support is documented with community-bridge alternatives.
- Universal-footguns section in the MCP quickstart (stripped-PATH in desktop apps, schema-key differences across clients).

## [0.0.1] - 2026-05-27

### Added

- Four context endpoints: `/v1/markets/relevant-to`, `/v1/markets/{market_ref}/context`, `/v1/bundles/{bundle_ref}/context`, `/v1/events/{event_id}/related-markets`.
- Curated social watchlist (~5,400 high-signal accounts) gating which posts enter the context index.
- Machine-readable OpenAPI spec at repo root (`openapi.yaml`).
- Quickstart docs for `curl` and MCP setup under `docs/quickstart/`.
- API reference under `docs/api/`.
