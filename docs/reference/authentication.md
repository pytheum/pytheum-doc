# Authentication

## Current (v0)

**No auth required.** Every endpoint is open and free. Just call the URL.

```bash
curl 'https://api.pytheum.com/v1/markets/relevant-to?query=fed+cut+june&limit=5'
```

Don't send an `Authorization` header — it's ignored today and may break under the planned migration if you ship code assuming auth is wired up.

## Planned (v0.2)

API keys, sent as a bearer token:

```
Authorization: Bearer pyk_<32-char-suffix>
```

Keys begin with the `pyk_` prefix so they're greppable in source-control leaks and visible in logs without confusion against unrelated tokens.

### Signup flow (planned)

1. Email signup on the pytheum site.
2. Free-tier key auto-issued, shown once, copyable.
3. Higher tiers (dev, pro) gated behind billing.

### Scopes (planned)

Initial keys are **read-only**. Every existing v0 endpoint is a `GET`, so this covers the surface area. Write scopes will be introduced if and when we ship endpoints that mutate state (none on the immediate roadmap).

### Rotation (planned)

- Each account can have up to 5 active keys at once.
- Keys can be revoked individually via the dashboard.
- A revoked key returns `401 Unauthorized` immediately — no grace period.
- We never rotate keys for you; you rotate when you want.

## The unauth → auth transition

When auth ships, we won't flip a switch. The plan:

1. **Grace period** — both unauth and authed requests work. Unauth gets a `Deprecation` header pointing at this page.
2. **Soft gating** — unauth requests get rate-limited aggressively (much tighter than the free tier).
3. **Hard cut** — unauth returns `401`. We'll announce the date at least 30 days in advance via the [ROADMAP](../../ROADMAP.md) and the GitHub repo.

If you're shipping now, you have time. The transition is purposely slow because we don't want to break working agents.

## See also

- [Rate limits](rate-limits.md) — how tiers map to limits
- [Errors](errors.md) — `401` and `403` will join the list in v0.2
- [ROADMAP](../../ROADMAP.md)
