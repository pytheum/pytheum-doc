# `GET /v1/markets/{market_ref}/context`

Return the events (news, social posts, HN stories, macro releases) from the last 24h that paired with a specific market.

## Request

```
GET /v1/markets/polymarket:101772/context?limit=1
```

| Path | |
|---|---|
| `market_ref` | Venue-prefixed market id (e.g. `polymarket:101772`, `kalshi:KXFED-24DEC-525`, `manifold:pudqyS5EA9`) |

| Query | Required | Default | Notes |
|---|---|---|---|
| `limit` | no | 25 | Max 200 |
| `min_similarity` | no | 0.30 | Lower than `relevant-to` because market-question→event-body sims are naturally lower |
| `kinds` | no | all | csv: `news_headline,social_post,hn_story,macro_release` |
| `sibling_markets` | no | `true` | Set `false` to omit the correlated-market block (below) |

## Response

```json
{
  "market": {
    "id": "polymarket:101772",
    "question": "Fed Decision in June?",
    "venue": "polymarket",
    "bundle_id": "polymarket:economic-policy",
    "bundle_label": "Economic Policy",
    "volume_usd": 27092266.7,
    "status": "active",
    "implied_yes": 0.978,
    "resolution_criteria": "This market will resolve based on the FOMC's June 2026 interest rate decision..."
  },
  "sibling_markets": [
    {
      "market_id": "polymarket:690197",
      "question": "Fed rate hike in 2026?",
      "venue": "polymarket",
      "status": "active",
      "volume_usd": 1235396.5,
      "implied_yes": 0.315
    }
  ],
  "context": [
    {
      "event_id": "evt_news_headline_6a5f4539dd30",
      "kind": "news_headline",
      "ts": "2026-05-27T01:44:21.490701+00:00",
      "snapshot": {
        "title": "Federal Reserve Board - Minutes of the Board's discount rate meeting on April 20 and 29, 2026",
        "body": "May 26, 2026\nMinutes of the Board's discount rate meeting...",
        "domain": "federalreserve.gov",
        "url": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20260526a.htm",
        "author": null,
        "published_at": "2026-05-26T18:00:00Z",
        "fetched_at": "2026-05-27T01:44:21.698832",
        "body_fetch_state": "complete",
        "fetch_error": null,
        "_matched_market_ids": ["polymarket:906973", "polymarket:906975", "..."],
        "_matched_similarities": [0.566, 0.560, "..."]
      },
      "similarity": 0.511,
      "source": "embedding"
    }
  ],
  "meta": {
    "window_hours": 24,
    "embedding_model": "openai:text-embedding-3-large",
    "limit": 1,
    "min_similarity": 0.3,
    "total_in_window": 8000,
    "sibling_markets_count": 1
  }
}
```

## The market block, sibling markets, and context — three layers in one call

A single `/context` call gives an agent everything it needs to reason about a position:

1. **`market.implied_yes`** — the market's own current implied YES probability (0–1), from its live price. `null` for markets without a binary YES price (categorical/multi-outcome markets, or venues that don't expose a price in our listing).
2. **`market.resolution_criteria`** — *how the market actually resolves* (the source, metric, threshold, and tiebreaks), so an agent frames the question correctly instead of guessing. `null` when the market provides no resolution text.
3. **`sibling_markets`** — correlated markets from the same event graph, each with `volume_usd` and (when available) `implied_yes`. Lets an agent read a market against its neighbors (e.g. a rate-cut market next to a rate-hike market) in the same response. Volume-ranked, deduped, filtered to on-topic correlates.
4. **`context`** — the supporting news/social/macro signals (below).

## When to use this

- **Agent looking at a specific market**: "What's been said about this in the last 24 hours?"
- **Building a market briefing**: aggregate recent news + social around a position.
- **Anomaly detection**: an unusual price move; pull context to see if news justifies it.

## Tips

- **`meta.total_in_window`** reports how many events are indexed for the rolling window. Currently capped at **8,000** entries (FIFO when the cap is hit). Numbers below ~100 usually mean the embedding worker just restarted.
- **`snapshot.body`** is the extracted article body for `news_headline` events (500–2,500 chars typical). When `body_fetch_state` is `"failed"`, only `title` will be useful; `fetch_error` carries the reason.
- **`similarity`** at the top level of each context item is the cosine sim between the event's embedding and **this specific market's** embedding, computed at query time. The same event will appear in other markets' context with a different `similarity` score.
- **`snapshot._matched_market_ids`** / **`_matched_similarities`** are separate worker-internal metadata: the top-10 nearest markets the worker found when it first ingested the event. Leading underscore = internal field, shape may change before v1; don't depend on it.
- See [Concepts → Embedding & Pairing](../concepts/embedding-pairing.md) for the full mental model.

## Errors

- `404` — market not found at all
- `422` — market exists but isn't in our top-N coverage (no embedding). Re-backfill with `--ORDER-BY volume DESC` is the highest-leverage way to expand coverage. [Roadmap](../../ROADMAP.md).
