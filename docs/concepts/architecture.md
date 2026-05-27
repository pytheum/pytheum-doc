# Architecture

A 30-second tour of what's behind the four endpoints.

```mermaid
flowchart TD
    subgraph Collectors["Collectors (24/7)"]
        K[Kalshi + Polymarket + Manifold ticks]
        B[Bluesky firehose<br/>filtered to ~5400 DIDs]
        R[RSS + article body extraction]
        H[HackerNews items + updates]
        M[Macro releases<br/>FOMC, ALFRED, BEA, BLS]
    end

    Disk[(JSONL on local disk<br/>append-only, PIT preserved)]
    S3[(S3 cold tier<br/>s3://pytheum-v1)]

    Collectors --> Disk
    Disk -->|gzipped daily| S3

    subgraph Embedder["Embedding worker"]
        Tail[Tail JSONL files]
        Embed[Embed via OpenAI<br/>text-embedding-3-large]
        KNN[kNN against Pinecone<br/>market index]
        Tail --> Embed --> KNN
    end

    Disk --> Tail

    Mem[(In-memory<br/>rolling 24h index)]
    PG[(Postgres<br/>market_event_pairings)]
    Pine[(Pinecone<br/>market vectors)]

    KNN --> Mem
    KNN --> PG
    KNN -.reads.-> Pine

    API[API<br/>api.pytheum.com]
    Mem --> API
    PG -.v1 replay.-> API
    Pine -.market metadata join.-> API
```

## Index composition

- **Markets** (Pinecone): top ~10k by volume across Kalshi + Polymarket + Manifold. Embedded once at backfill time; refreshed periodically. See [Embedding & Pairing](embedding-pairing.md).
- **Events** (rolling 24h, in-memory): every news/social/HN/macro event from the last 24h that passed the [watchlist filter](watchlist.md). Capped at 8,000 entries FIFO.
- **Pairings** (Postgres, durable): every (event, market, similarity) tuple is logged for [PIT replay](pit.md) in v1.

## Storage tiers

| Tier | Where | What |
|---|---|---|
| Hot | EC2 local disk | JSONL being written, in-memory rolling index, Pinecone serverless |
| Warm | Postgres (Supabase Pro) | Markets metadata + pairings log |
| Cold | S3 (`s3://pytheum-v1`) | JSONL.gz daily partitions |

The Pinecone index is canonical for **vectors**. Postgres is canonical for **metadata**. The API JOINs them at query time.

## See also

- [Point-in-time](pit.md) — what we guarantee about historical accuracy
- [Embedding & Pairing](embedding-pairing.md) — how events get matched to markets
- [Watchlist](watchlist.md) — why we filter the Bluesky firehose
