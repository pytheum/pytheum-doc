# pytheum

**Prediction-market context, paired with live news + social signal, in a single API call.**

pytheum tails every market tick on Kalshi, Polymarket, and Manifold, embeds them alongside a curated firehose of news and social posts, and exposes the pairings through four HTTP endpoints designed for AI agents. Ask *"what's moving the Fed-cut market right now?"* and get back the markets, the supporting signals, and the timestamps in one round trip.

```bash
curl 'https://api.pytheum.com/v1/markets/relevant-to?query=fed+cut+june&limit=5' | jq
```

[curl examples](docs/quickstart/curl.md) · [MCP setup (11 clients)](docs/quickstart/mcp.md)

## What pytheum does

- **Curated social + news firehose** — ~5,400 hand-vetted and discovered accounts across econ, politics, geopolitics, crypto, and sports, embedded against every tracked market roughly every 20 seconds. RSS articles and HackerNews items go through the same pipeline.
- **Point-in-time discipline** — the underlying archive enforces `published_at ≤ target_ts` contamination filtering. PIT replay (`at=2026-04-15T14:00Z`) lands in v1.
- **Cross-venue, one schema** — Kalshi, Polymarket, and Manifold normalized into a single market vocabulary. One query covers all three.
- **Free and unauthenticated in v0** — no key required while we calibrate. Add it to an agent in a single line.

## Four endpoints

| Method | Path | Use when |
|---|---|---|
| GET | `/v1/markets/relevant-to` | You have a sentence, want the markets it moves |
| GET | `/v1/markets/{market_ref}/context` | You're watching a market, want the latest signals |
| GET | `/v1/bundles/{bundle_ref}/context` | You're watching a multi-outcome event, want context across all legs |
| GET | `/v1/events/{event_id}/related-markets` | You saw an event in our firehose, want to know what else it moves |

The MCP server ([`pytheum-mcp` on PyPI](https://pypi.org/project/pytheum-mcp/), [`@pytheum/mcp` on npm](https://www.npmjs.com/package/@pytheum/mcp)) exposes these four as `t_find_markets`, `t_market_context`, `t_bundle_context`, `t_event_related_markets`.

Full reference: [`docs/api/`](docs/api/overview.md) · Machine-readable spec: [`openapi.yaml`](openapi.yaml)

## Documentation

| | |
|---|---|
| **Quickstart** | [curl](docs/quickstart/curl.md) · [MCP setup (11 clients)](docs/quickstart/mcp.md) |
| **API reference** | [Overview](docs/api/overview.md) · [Errors / rate-limits / auth](docs/reference/errors.md) |
| **Concepts** | [Point-in-time](docs/concepts/pit.md) · [Embedding & pairing](docs/concepts/embedding-pairing.md) · [Bundles](docs/concepts/bundles.md) · [Event kinds](docs/concepts/event-kinds.md) · [Watchlist](docs/concepts/watchlist.md) · [Architecture](docs/concepts/architecture.md) |
| **Examples** | [Python](examples/python-quickstart/) · [Next.js route handler](examples/next-route-handler/) · [Claude Desktop MCP](examples/mcp-claude-desktop/) |
| **SDKs (planned)** | [Index](docs/sdks/index.md) |

## Status

**v0, public, free, no auth.** Calibrating quality before any quota; expect breaking changes. See [ROADMAP.md](ROADMAP.md) · [CHANGELOG.md](CHANGELOG.md).

## Links

- API base: `https://api.pytheum.com`
- Live demo dashboard: [pytheum-stream-site.vercel.app](https://pytheum-stream-site.vercel.app)
- Issues / questions: [open a GitHub issue](https://github.com/pytheum/pytheum-doc/issues)
