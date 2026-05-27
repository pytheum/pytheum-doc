# `GET /v1/markets/relevant-to`

Embed a free-text query and return the most similar prediction markets.

## Request

```
GET /v1/markets/relevant-to?query=fed+cut+june&limit=5
```

| Param | Required | Default | Notes |
|---|---|---|---|
| `query` | yes | — | The text to embed. Max 4000 chars. |
| `limit` | no | 50 | Max 200 |
| `min_similarity` | no | 0.40 | Cosine floor. Lower returns more, noisier results. |
| `venue` | no | all | csv: `kalshi,polymarket,manifold` |
| `status` | no | `active,resolving` | csv |
| `group_by` | no | `bundle` | `bundle` collapses to the highest-similarity market per bundle. `none` returns raw matches. |

## Response

```json
{
  "query": "fed cut june",
  "markets": [
    {
      "id": "polymarket:101772",
      "question": "Fed Decision in June?",
      "venue": "polymarket",
      "bundle_id": "polymarket:economic-policy",
      "bundle_label": "Economic Policy",
      "similarity": 0.760,
      "volume_usd": 27092266.7,
      "status": "active",
      "url": "https://polymarket.com/event/fed-decision-in-june-825"
    }
  ],
  "meta": {
    "embedding_model": "openai:text-embedding-3-large",
    "limit": 5,
    "group_by": "bundle",
    "venues": null
  }
}
```

## When to use this

- **Article-to-market routing**: pass an article body or headline as `query`, get back the markets to watch.
- **Backtest query expansion**: a research script with a list of hypotheses; for each hypothesis, find the most-related market on each venue.
- **Agent reasoning**: an agent sees a tweet, calls this with the tweet text, and now knows which prices to look at.

## Tips

- Bundle dedup is on by default. If you want the per-outcome breakdown (e.g. all 30 candidates in a presidential bundle), pass `group_by=none`.
- The 0.40 floor is calibrated for "this query specifically routes here". For exploratory searches drop to 0.30 — you'll get more candidates and have to filter them yourself.
- Sort order is always descending by `similarity`.
