# Rate limits

**v0: no quotas.** The API is free and public while we calibrate quality.

## Today

There are no per-IP, per-key, or per-endpoint limits enforced. Be polite:

- Don't exceed ~10 req/sec sustained per client.
- If you need bulk access, prefer fewer queries with larger `limit=` over many small ones.
- For tick-level data, use the WebSocket firehose at `wss://api.pytheum.com/v1/stream` instead of polling.

If we observe abuse, we'll add per-IP soft caps without notice. Open an issue if you have a legitimate high-volume use case — easier to whitelist you than to play whack-a-mole.

## Planned (v0.2)

When auth ships, rate limits land with it. Three planned tiers:

| Tier | Intended for |
|---|---|
| Free | Indie devs, experimentation |
| Dev | Production agents, small services |
| Pro | High-throughput backends |

**No specific request/sec or daily-cap numbers are committed yet.** They'll be set once we have real usage shapes. Free will always cover prototyping.

## See also

- [Authentication](authentication.md) — how tier assignment will work
- [Errors](errors.md)
- [ROADMAP](../../ROADMAP.md)
