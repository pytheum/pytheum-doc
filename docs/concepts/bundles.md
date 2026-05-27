# Bundles

A bundle is a group of markets that share an underlying event but split it into multiple outcomes. The June FOMC meeting is one event with three Polymarket markets attached: cut, hold, hike. That trio is a bundle.

Bundles exist because most interesting questions are multi-outcome. If you only query the cut market, you miss the news that moves the hold market — even though both react to the same FOMC speech.

## How IDs work

Bundle IDs are venue-prefixed strings:

| Venue | Source | Example |
|---|---|---|
| Polymarket | Event slug from the platform | `polymarket:fomc`, `polymarket:elections`, `polymarket:politics` |
| Kalshi | The id prefix before the first `-` | `kalshi:KXFED`, `kalshi:KXPRES` |
| Manifold | (no bundle concept exposed yet) | — |

So `polymarket:fomc` is a bundle. Its children are individual market ids like `polymarket:287395` (the "Fed cuts in June 2026?" market). The bundle ID stays stable as children come and go.

## A concrete example

`polymarket:fomc` currently has 3 children:

- `polymarket:287395` — "Will the Fed cut rates in June 2026?"
- `polymarket:287394` — "Will the Fed hold rates in June 2026?"
- `polymarket:287396` — "Will the Fed hike rates in June 2026?"

Ask the bundle endpoint:

```
GET /v1/bundles/polymarket:fomc/context?limit=10
```

…and you get back the news/social/macro events that paired with **any** of those three markets in the last 24h, deduped by `event_id`, keeping the highest-similarity match. The response tells you `matched_market_id` so you can see which child the event hit hardest.

## Per-market vs bundle queries

Both are useful — pick based on what you know:

| You know… | Use |
|---|---|
| The exact outcome you care about | `/v1/markets/{market_ref}/context` |
| The event but not which outcome | `/v1/bundles/{bundle_ref}/context` |
| Neither — just a sentence | `/v1/markets/relevant-to?query=…` |

The trade-off: bundle queries iterate over child markets, so very large bundles are slower than narrower ones. Performance work for very-large-bundle queries is on the v0.1 roadmap. For now, prefer narrower bundles like `polymarket:fomc` or `polymarket:elections` when latency matters.

## Bundle dedup on `relevant-to`

`/v1/markets/relevant-to` defaults to `group_by=bundle` — it collapses to the highest-similarity market per bundle so you don't get 30 nominee-X rows when only the bundle as a whole was the answer. Pass `group_by=none` to see every child.

## See also

- [Architecture](architecture.md) — where bundles fit in the index
- [Bundles context endpoint](../api/bundles-context.md)
- [Markets relevant-to endpoint](../api/markets-relevant-to.md)
