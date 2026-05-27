# Bluesky watchlist

The Bluesky firehose is high-volume and embedding budget is finite. To make the budget count, a normalizer in front of the embedder admits posts only from a curated + discovered DID set of high-signal authors. Posts from accounts outside the watchlist are dropped before they consume any embedding budget.

## Composition of the watchlist

The active set is the union of three sources, ~5,400 unique DIDs total:

1. **24 baseline DIDs** — econ, policy, news outlets. Hardcoded fallback so the firehose has *something* even if the other lists fail to load.
2. **163 curated accounts** across six categories: politics, econ + Fed, geopolitics, crypto + finance, sports, entertainment. Hand-picked and verified against the Bluesky AppView.
3. **5,251 discovered accounts** with ≥5,000 followers, harvested from the firehose itself. Refreshed periodically (daily refresh cron is on the v0.1 roadmap).

A post is admitted if its author DID appears in any of the three sets.

## Effect on the pipeline

With the watchlist in place, the embedder spends its full budget on text from authors likely to matter — Fed correspondents, politics beat reporters, geopolitics analysts, crypto OGs, sports analytics — rather than on the arbitrary tail of the firehose.

Filtering up-front rather than downstream matters because embedding cost is linear in events processed. A discarded post that you embedded is pure waste.

## Why curation matters even with discovery

The discovery pass (≥5k followers) catches the long tail — popular voices we didn't hand-pick. But follower count alone is a weak proxy for signal: a high-follower meme account often isn't useful, and a smaller-follower economist with FOMC takes often is. The curated 163 is the floor for things follower-count would miss.

The combination is robust: discovery handles volume, curation handles precision.

## What this means for the API

When you call `/v1/markets/{ref}/context?kinds=social_post`, every post you see came from a DID in this watchlist. If a post you'd expect to see isn't there:

- The author may not be on the watchlist (yet — discovery runs daily once shipped).
- The post may have failed the embedding similarity floor for that market.
- The post may be older than the 24h rolling window.

## See also

- [Architecture](architecture.md) — where the normalizer sits
- [Event kinds](event-kinds.md) — `social_post` in context
- [Embedding & pairing](embedding-pairing.md) — what happens after admission
