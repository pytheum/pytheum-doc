# `GET /v1/events/{event_id}/related-markets`

Given an event_id from the firehose (e.g. one returned by a previous context call), return the markets that paired with it.

## Request

```
GET /v1/events/evt_news_headline_059539a6616e/related-markets?limit=10
```

| Path | |
|---|---|
| `event_id` | Event ID returned by any context endpoint (`evt_<kind>_<random>`) |

| Query | Required | Default | Notes |
|---|---|---|---|
| `limit` | no | 25 | Max 200 |
| `min_similarity` | no | 0.30 | |
| `venue` | no | all | csv |
| `status` | no | `active,resolving` | csv |
| `group_by` | no | `bundle` | `bundle` collapses to one row per bundle_id; `none` returns raw |

## Response

```json
{
  "event_id": "evt_news_headline_6a5f4539dd30",
  "markets": [
    {
      "id": "polymarket:101772",
      "question": "Fed Decision in June?",
      "venue": "polymarket",
      "bundle_id": "polymarket:economic-policy",
      "bundle_label": "Economic Policy",
      "similarity": 0.511,
      "volume_usd": 27092266.7,
      "status": "active",
      "url": "https://polymarket.com/event/fed-decision-in-june-825"
    }
  ],
  "meta": {
    "embedding_model": "openai:text-embedding-3-large",
    "limit": 10,
    "group_by": "bundle",
    "venues": null
  }
}
```

## When to use this

- **News-first workflows**: you saw an article come in and want to trade against the markets it moves.
- **Event chaining**: an agent following a story can hop from event → markets → other events.
- **Auditing pairings**: spot-check what the embedder thinks is related.

## Limits

The event must be within the rolling 24h in-memory window. **PIT replay (events older than 24h)** lands in v1 — at that point the durable `market_event_pairings` log replaces the in-memory lookup. See [ROADMAP.md](../../ROADMAP.md).

## Errors

- `404` — event_id not in the rolling window. Either it's older than 24h or it was never indexed.
