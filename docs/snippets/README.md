# Snippets

Reusable include-fragments for the four pytheum endpoints, one file per
(language, endpoint) pair.

## Convention

Each file is just a code block. Pages can include them inline once we move
to an SSG. Until then, copy-paste them into wherever you need.

Every snippet uses the same demo query (`"fed cut june"`) and limit (`5`)
so the three languages are directly comparable side-by-side.

## Layout

```
snippets/
  curl/         markets-relevant-to.md  markets-context.md  bundles-context.md  events-related.md
  python/       (same four)
  typescript/   (same four)
```

- `curl/` — raw shell, pipes to `jq` for readability.
- `python/` — `httpx` sync client. Python 3.11+.
- `typescript/` — global `fetch`. Node 18+ / any modern runtime.
