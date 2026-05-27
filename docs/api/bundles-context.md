# `GET /v1/bundles/{bundle_ref}/context`

Return events paired with **any** market in a bundle, deduplicated by event_id (keeping the highest-similarity match).

## Request

```
GET /v1/bundles/polymarket:fomc/context?limit=10
```

| Path | |
|---|---|
| `bundle_ref` | Venue-prefixed bundle id (e.g. `polymarket:fomc`, `polymarket:politics`, `kalshi:KXFED`) |

| Query | Required | Default | Notes |
|---|---|---|---|
| `limit` | no | 50 | Max 200 |
| `min_similarity` | no | 0.15 | Same rationale as markets/context |
| `kinds` | no | all | csv |

## What is a bundle?

A bundle groups multiple markets that share an event ("FOMC meeting" with separate markets for hike/hold/cut, or "2028 nominee" with 30 candidates). Bundles are useful when you don't know which specific child market is the right query.

Polymarket bundles come from the event slug. Kalshi bundles are the id prefix before `-`.

## Response

```json
{
  "bundle": {
    "id": "polymarket:fomc",
    "label": "fomc",
    "venue": "polymarket",
    "market_count": 3
  },
  "context": [
    {
      "event_id": "evt_news_headline_29a94200de6c",
      "kind": "news_headline",
      "ts": "2026-05-27T01:33:58.883402+00:00",
      "snapshot": {
        "title": "Federal Reserve Board - Minutes of the Board's discount rate meeting...",
        "body": "...",
        "domain": "federalreserve.gov",
        "url": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20260526a.htm",
        "author": null,
        "published_at": "2026-05-26T18:00:00Z",
        "fetched_at": "2026-05-27T01:33:59.122510",
        "body_fetch_state": "complete",
        "fetch_error": null,
        "_matched_market_ids": ["polymarket:906973", "..."],
        "_matched_similarities": [0.566, "..."]
      },
      "similarity": 0.491,
      "source": "embedding",
      "matched_market_id": "polymarket:287395"
    }
  ],
  "meta": {
    "window_hours": 24,
    "embedding_model": "openai:text-embedding-3-large",
    "limit": 1,
    "min_similarity": 0.15,
    "total_in_window": 8000
  }
}
```

The `matched_market_id` field tells you which child market in the bundle the event paired with most strongly. The dedup logic keeps the best match across all children.

## When to use this

- **You don't know which outcome**: a Fed-cut bundle has 6 outcomes; ask the bundle, get news that applies to any of them.
- **Multi-candidate events**: presidential nominees, sports tournaments, awards.
- **Aggregated market briefing**: "what's moving the politics complex right now?"

## Performance

Bundles iterate over their child markets and query each. **For bundles with > ~50 children the request can time out.** Known issue: `polymarket:politics` has 577 children and currently returns HTTP 000 after 30s. Fix in the v0.1 roadmap.

For now, prefer narrow bundles (the politics complex is split into ~20 sub-bundles like `polymarket:fomc`, `polymarket:elections`, etc.) or use [`/v1/markets/relevant-to`](markets-relevant-to.md) instead.
