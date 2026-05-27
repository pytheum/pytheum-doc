# Roadmap

What's shipped, what's next.

## Shipped (2026-05)

- Four context endpoints (`/v1/markets/relevant-to`, `/v1/markets/{ref}/context`, `/v1/bundles/{ref}/context`, `/v1/events/{id}/related-markets`)
- Top-10k market embedding index (volume-weighted)
- Curated Bluesky watchlist (~5,400 high-signal accounts across politics, econ, geopolitics, crypto, sports, entertainment)
- Durable pairings log (every `(event, market, similarity)` tuple persisted for PIT replay)
- `pytheum-mcp` MCP server on PyPI and npm — `uvx pytheum-mcp` for any MCP client
- Public docs (this repo)

## Coming next

### v0.1 — quality and coverage

- **Expanded Kalshi coverage** — broaden the embedded market index so Kalshi questions surface in `relevant-to` results as strongly as Polymarket questions across politics, sports, crypto, and weather.
- **Bundle endpoint performance** — scale the per-bundle context fetch so very large bundles (hundreds of children) stay snappy.
- **Daily refresh** of the social watchlist so newly active high-signal accounts get embedded automatically.

### v0.2 — delivery convenience

- **`pytheum` Python SDK** — pip-installable typed client. Async + sync both supported.
- **`@pytheum/client` TypeScript SDK** — for Node and browser.

Both are thin wrappers over the same HTTP endpoints. The OpenAPI spec ([`openapi.yaml`](openapi.yaml)) drives codegen.

### v1.0 — point-in-time replay

- **PIT replay endpoint** — `/v1/replay?market_id=&at=` to fetch the market + paired context as it stood at any historical timestamp. Backed by the persistent pairings log and the S3 cold tier.
- **Backtest API** — drop a strategy, get scored against the historical pairings.

### Beyond

- More embeddable sources (Reddit, court filings, polls, on-chain events).
- Cross-venue market matching — the same question listed on Kalshi + Polymarket linked back to a single canonical id.
- Hosted MCP (remote) at `api.pytheum.com/mcp` — zero-install for clients that support it.

## What we explicitly aren't building

- Authentication / quotas / billing — v0 is free, public, no auth. We'll add when usage forces it.
- Streaming endpoints over HTTP — use the existing WebSocket firehose at `wss://api.pytheum.com/v1/stream` for low-latency event streams. The REST API is for context lookups.
- A web UI on this domain — see [pytheum-stream-site.vercel.app](https://pytheum-stream-site.vercel.app) for the demo dashboard.

---

Have a request? Open an issue. The roadmap is reactive to actual usage.
