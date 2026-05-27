# API Overview

Base URL: `https://api.pytheum.com`

All endpoints are `GET`. Responses are JSON. No authentication during the v0 free-tier period.

## The four endpoints

| Endpoint | Use it when… |
|---|---|
| [`GET /v1/markets/relevant-to?query=…`](markets-relevant-to.md) | You have a sentence (article body, headline, question) and want to know which markets it relates to. |
| [`GET /v1/markets/{market_ref}/context`](markets-context.md) | You're looking at a specific market and want the news/social posts that paired with it. |
| [`GET /v1/bundles/{bundle_ref}/context`](bundles-context.md) | A market belongs to a multi-outcome bundle (e.g. "Republican 2028 nominee" with 30 candidates) and you want context across the whole thing. |
| [`GET /v1/events/{event_id}/related-markets`](events-related.md) | You saw an event come through the firehose and want to follow it back to the markets it moves. |

## Common parameters

| Param | Default | Notes |
|---|---|---|
| `limit` | endpoint-specific (25 or 50) | Max 200 |
| `min_similarity` | 0.15–0.40 depending on endpoint | Cosine floor |
| `venue` | unset (all) | csv: `kalshi,polymarket,manifold` |
| `status` | `active,resolving` | csv: `active,resolving,resolved` |
| `kinds` | unset (all) | csv: `news_headline,social_post,hn_story,macro_release` (context endpoints only) |
| `group_by` | `bundle` | `bundle` collapses to one row per bundle_id; `none` returns raw matches (market endpoints only) |

## Identifiers

- **Market IDs** are venue-prefixed: `polymarket:31875`, `kalshi:KXFED-24DEC-525`, `manifold:pudqyS5EA9`.
- **Bundle IDs** are venue-prefixed and either a slug (Polymarket: `polymarket:fomc`) or the id prefix before `-` (Kalshi: `kalshi:KXFED`).
- **Event IDs** look like `evt_<kind>_<random>` and are returned by every context endpoint. They're stable inside the rolling 24h window.

## Response shape

Every response has a `meta` block describing how the index was queried:

```json
{
  "meta": {
    "embedding_model": "openai:text-embedding-3-large",
    "limit": 25,
    "window_hours": 24,
    "total_in_window": 8000,
    "min_similarity": 0.15
  }
}
```

`total_in_window` reports how many events are indexed for the rolling 24h window. It's currently capped at **8,000** entries (FIFO drop when exceeded); a value of 8000 means the cap is saturated and there may be more recent events than displayed. `min_similarity` and `window_hours` appear on context endpoints only; `group_by` and `venues` appear on market endpoints only.

## Errors

| HTTP | Meaning |
|---|---|
| 400 | Missing/invalid parameter (`{"detail": "..."}`) |
| 404 | Market/bundle/event not found |
| 422 | Market exists but has no embedding (not in the top-N coverage today) |
| 502 | Upstream embedding provider unavailable |

## Limits and quotas (v0)

- No request quotas yet — we'll add them if the service is abused
- Rolling event window: 24 hours
- Market index: top 10k markets by volume (re-backfilled periodically)
- Event index: every news/social/hn/macro event from the last 24h (filtered against the [Bluesky watchlist](../concepts/architecture.md))
