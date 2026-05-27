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
| `min_similarity` | no | 0.15 | Lower than `relevant-to` because market-question→event-body sims are naturally lower |
| `kinds` | no | all | csv: `news_headline,social_post,hn_story,macro_release` |

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
    "status": "active"
  },
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
    "min_similarity": 0.15,
    "total_in_window": 8000
  }
}
```

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
