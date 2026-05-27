# Errors

Every error response carries a JSON body with a single `detail` field describing what went wrong. In v0.2 we plan to add a stable `code` field for SDK-side error handling; until then, match on HTTP status.

## Status codes

| HTTP | Meaning | Action |
|---|---|---|
| 400 | Missing or invalid query parameter | Fix the request — `detail` names the param |
| 404 | Market, bundle, or event not found | Check the venue prefix and id |
| 422 | Market exists but has no embedding | Out of top-N coverage today; re-backfill is on the roadmap |
| 502 | Upstream embedding provider unavailable | Transient — retry with backoff |

## 400 — bad request

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{"detail": "missing required query param: query"}
```

Triggered when a required param is absent or unparseable (e.g. `limit=abc`, `min_similarity=2.5`). The `detail` names the offending field. No retry will help — fix the request.

## 404 — not found

```http
HTTP/1.1 404 Not Found
Content-Type: application/json

{"detail": "market not found: polymarket:99999999"}
```

The id parsed fine but nothing matches. Likely causes:

- Wrong venue prefix (`polymarket:` vs `kalshi:`).
- Typo in the id.
- For events: the event aged out of the rolling 24h window. PIT replay (v1) will let you look up older events by id; today they're gone from the in-memory index.

## 422 — no embedding

```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{"detail": "market has no embedding: polymarket:31875"}
```

The market is in our metadata but not in the Pinecone vector index — we only embed the top ~10k markets by volume. Re-backfilling with `volume_usd DESC` order is the highest-leverage fix; see the v0.1 milestone in [ROADMAP.md](../../ROADMAP.md).

## 502 — upstream embedding

```http
HTTP/1.1 502 Bad Gateway
Content-Type: application/json

{"detail": "upstream embedding provider unavailable"}
```

Only the `relevant-to` endpoint embeds at request time, so it's the only one that can hit this. OpenAI hiccuped or our key got rate-limited. Retry with exponential backoff (250ms → 1s → 4s).

## Planned: stable `code` field (v0.2)

To keep SDKs from string-matching `detail`, v0.2 responses will gain a `code` field:

```json
{"code": "market_not_in_index", "detail": "market has no embedding: polymarket:31875"}
```

The full enum will land with the SDK release. Until then, treat HTTP status as the contract and `detail` as human-readable only.

## See also

- [API overview](../api/overview.md)
- [Rate limits](rate-limits.md)
- [Authentication](authentication.md)
