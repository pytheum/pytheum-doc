# Point-in-time (PIT)

Point-in-time means every event we record is stamped with the moment we observed it, and the record never gets edited or backfilled. If you ask later what the world looked like at `2026-04-15T14:00Z`, you see only what was actually known by then — not what we wish we'd known, or what got revised in.

This is the single most load-bearing property of the archive. Everything else (the embedding index, the pairings log, the future replay endpoint) inherits its trust from PIT discipline at the collection layer.

## How it's preserved on disk

Every collector writes one record per event to a daily-partitioned JSONL file:

```
data/<track>/<category>/dt=YYYY-MM-DD/*.jsonl
```

Records are append-only. Older partitions roll to `s3://pytheum-v1/...` gzipped. **No rewrites, no upserts, no edits.** If a record turns out to be wrong (e.g. an HN story whose title later changed), the correction comes in as a *new* record with its own observed timestamp — the original stays put.

Ticks carry two timestamps: `t` (our wall-clock receive) and `vt` (the venue's server timestamp), so you can align Kalshi and Polymarket events sub-millisecond after the fact.

## What the API exposes today

The four context endpoints today read from a **rolling 24h in-memory index**. Events older than 24h are pruned out of memory; they're still on disk and in S3, just not queryable through the REST API yet.

For long-horizon questions, you currently have to:

1. Pull the cold-tier JSONL.gz partitions directly from S3.
2. Or wait for the v1 replay endpoint.

## The v1 replay endpoint

The persistent `market_event_pairings` table in Postgres started accumulating on 2026-05-26. Once that table has enough history, the v1 replay endpoint will expose it:

```
GET /v1/replay?market_id=polymarket:287395&at=2026-04-15T14:00Z
```

…returning the markets + paired events as they stood at that timestamp. See [ROADMAP.md](../../ROADMAP.md) for the v1.0 milestone.

## Why this matters for agents

LLM agents often hallucinate retrocausally — pulling in information that didn't exist at the time of the question. The PIT archive is the substrate that lets you check: was this signal actually available at decision time, or did the agent peek at the future?

Backtests against the archive will, by construction, never leak.

## See also

- [Architecture](architecture.md) — how PIT propagates through the pipeline
- [Embedding & pairing](embedding-pairing.md) — what the durable pairings log stores
- [Event kinds](event-kinds.md) — which records get embedded
