# Embedding and pairing

A **pairing** is a `(event, market, similarity)` tuple — the embedder's claim that this event is relevant to this market, with a cosine score quantifying how much. Every context endpoint is, under the hood, a query over pairings.

## What the embedder does

When a new event arrives on disk (see [event kinds](event-kinds.md)), the worker:

1. Extracts the embeddable text — title + body for news, `text` for social, etc.
2. Embeds it via OpenAI `text-embedding-3-large` (3072-dim vector).
3. kNN-queries the Pinecone market index, top 10 by cosine similarity.
4. Writes the resulting pairings to two places:
   - The **rolling 24h in-memory index** (fast reads for the API).
   - The **Postgres `market_event_pairings` table** (durable PIT history).

Markets themselves are embedded once at backfill time (off the market question), refreshed periodically. They sit in Pinecone as the canonical vector store.

## Cosine similarity, in practice

All similarity values returned by the API are cosine in `[0, 1]`, sorted descending. A few rules of thumb from production:

- **> 0.65**: the event is almost certainly about this market.
- **0.40–0.65**: relevant, often via a shared topic. Strong default for `relevant-to`-style routing.
- **0.25–0.40**: tangential. Useful for "show me everything in the neighborhood".
- **< 0.15**: usually noise.

These numbers vary by query direction. A user's free-text query against market questions runs higher than an article body against a market question — different distributions on each side of the dot product.

## Per-endpoint `min_similarity` floors

The defaults are calibrated against the actual distributions for each endpoint:

| Endpoint | Default `min_similarity` | Why |
|---|---|---|
| `GET /v1/markets/relevant-to` | **0.40** | Query → market question is the cleanest match; high floor keeps results sharp |
| `GET /v1/events/{id}/related-markets` | **0.30** | Event body → market question, slightly noisier |
| `GET /v1/markets/{ref}/context` | **0.15** | Market question → event body; the long event text drags sims down structurally |
| `GET /v1/bundles/{ref}/context` | **0.15** | Same as markets/context |

You can override `min_similarity` on any endpoint. Dropping the floor on `relevant-to` to 0.30 gives you more candidates you can filter yourself; raising the context endpoints to 0.30 gives you only the strongest matches.

## In-memory rolling index vs durable log

These are two different stores serving two different needs:

| | In-memory rolling 24h | Postgres `market_event_pairings` |
|---|---|---|
| Holds | Events from the last 24h | Every pairing since 2026-05-26 |
| Used by | The four REST endpoints today | v1 PIT replay (planned) |
| Lookup | O(1) by event_id, O(n) by market | Indexed by (market_id, ts) and (event_id, ts) |
| Lifetime | Pruned every minute | Append-only |

When the v1 replay endpoint ships, the durable log becomes the canonical read path for historical queries and the in-memory index stays as a hot-path cache.

## Why pairings, not just searches

Pairings are precomputed: the embedder does the kNN at ingest time, once per event, against a fixed market index. The API then reads the result for free. Doing a fresh kNN per request would cost an OpenAI embedding call + a Pinecone query per query, which is both slow (~500ms) and expensive.

The single exception is `/v1/markets/relevant-to`, which **does** embed the user's `query` at request time — because the query isn't known in advance.

## See also

- [Architecture](architecture.md) — where pairing sits in the pipeline
- [PIT](pit.md) — what the durable log unlocks
- [Markets relevant-to](../api/markets-relevant-to.md)
- [Events related-markets](../api/events-related.md)
