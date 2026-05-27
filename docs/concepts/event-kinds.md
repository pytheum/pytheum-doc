# Event kinds

The embedder only processes four kinds of records. Everything else (market ticks, order book updates, internal metadata) is collected and archived, but never paired with markets.

| Kind | Source | Typical cadence | `snapshot` carries |
|---|---|---|---|
| `news_headline` | RSS feeds + article body extraction via trafilatura | ~50–200/hr | `title`, `body` (500–2500 chars), `url`, `published_at`, `body_fetch_state` |
| `social_post` | Bluesky firehose, filtered through the watchlist | ~5–20/min | `text`, `author_did`, `author_handle`, `posted_at`, `reply_to`, `links[]` |
| `hn_story` | HackerNews items + updates endpoint | ~30/hr | `title`, `url`, `score`, `author`, `posted_at`, `id` |
| `macro_release` | FOMC statements, ALFRED, BEA, BLS | ~0–5/day | `series_id`, `title`, `value`, `released_at`, `prior_value`, `source` |

Every event also carries its top-level `event_id`, `kind`, and `ts` (ingest timestamp).

## Why ticks aren't embedded

Kalshi + Polymarket together emit ~10k ticks/sec at peak. Embedding each one through OpenAI's API would cost roughly $50k/day and produce nothing useful — a tick is `(market_id, price, size, timestamp)`, with no embeddable text. The market itself is embedded once (off its question), and ticks attach to it by `market_id`.

If you need ticks, use the streaming endpoint at `wss://api.pytheum.com/v1/stream` (or pull the cold-tier JSONL from S3). The REST context endpoints are deliberately about *text* events.

## Why only these four kinds

They're the kinds that produce embeddable text we can trust:

- **News**: dated, attributed, body extractable.
- **Social**: dated, filtered to the watchlist so SNR is workable.
- **HN**: dated, links + titles + a community-vetted score.
- **Macro**: native PIT, dated by definition, schema-bound.

Coming kinds (per roadmap): Reddit posts, court filings, polls, on-chain events. Each gets added to the discriminated union in the schema, the embedder picks them up automatically, and the API exposes them via the same `kinds=` filter.

## See also

- [Embedding & pairing](embedding-pairing.md) — what happens after a kind is selected
- [Watchlist](watchlist.md) — why `social_post` doesn't flood the pipeline
- [Markets context endpoint](../api/markets-context.md) — filter by `kinds=`
