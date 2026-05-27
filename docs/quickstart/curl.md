# Quickstart — curl

Every endpoint is a `GET`. No auth. Copy-paste these and tweak.

## 1. Find markets matching a query

```bash
curl 'https://api.pytheum.com/v1/markets/relevant-to?query=fed+cut+june&limit=5' | jq
```

What you get back: top 5 markets matched to the query, deduped by bundle, ranked by cosine similarity.

## 2. Pull context for a specific market

Compose step 1 → step 2 so the id is always live:

```bash
MARKET=$(curl -s 'https://api.pytheum.com/v1/markets/relevant-to?query=fed+cut+june&limit=1' | jq -r '.markets[0].id')
curl "https://api.pytheum.com/v1/markets/${MARKET}/context?limit=10" | jq
```

Or pass any explicit `<venue>:<id>` (e.g. `polymarket:101772`, `kalshi:KXFED-24DEC-525`, `manifold:pudqyS5EA9`). Returns the news/social/HN events from the last 24h that paired with that market.

## 3. Pull context for a whole bundle

```bash
curl 'https://api.pytheum.com/v1/bundles/polymarket:fomc/context?limit=10' | jq
```

Bundles group multi-outcome markets. `polymarket:fomc` has 3 child markets (rate cuts, holds, hikes); the response includes events that paired with **any** of them, deduped.

## 4. Follow an event back to its markets

```bash
# First, grab an event_id from any context response
EVENT_ID=$(curl -s 'https://api.pytheum.com/v1/markets/polymarket:101772/context?limit=1' | jq -r '.context[0].event_id')

# Then chase it back to the markets it pairs with
curl "https://api.pytheum.com/v1/events/${EVENT_ID}/related-markets" | jq
```

## Filter by venue, kinds, or similarity

```bash
# Only Kalshi markets
curl 'https://api.pytheum.com/v1/markets/relevant-to?query=trump+2028&venue=kalshi&limit=10' | jq

# Only news events (skip social posts)
curl 'https://api.pytheum.com/v1/markets/polymarket:101772/context?kinds=news_headline&limit=10' | jq

# Lower the similarity floor for exploratory results
curl 'https://api.pytheum.com/v1/markets/relevant-to?query=quiet+market+phrase&min_similarity=0.25&limit=20' | jq
```

## Tips

- All similarity values are cosine, [0, 1]. Results are sorted descending.
- `meta.total_in_window` on context endpoints reports indexed-event count for the rolling 24h window. Currently capped at **8,000** (FIFO drop when exceeded).
- If you're getting empty results on `markets/relevant-to`, try `min_similarity=0.30` (the 0.40 default is calibrated for high-precision routing).

## Common errors

- `404 market not found` — venue prefix wrong, or a typo in the id
- `422 market has no embedding yet` — that market exists but isn't in our top-N coverage today
- `400 missing required query param: query` — on `relevant-to` only, `query` is mandatory
