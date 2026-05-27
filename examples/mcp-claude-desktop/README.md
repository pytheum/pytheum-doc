# Claude Desktop — pytheum MCP server

Wire pytheum into Claude Desktop so Claude can call the four pytheum endpoints
as native tools (find relevant markets, pull market/bundle context, walk
events back to markets).

## When this works

> **Heads up:** The `pytheum-mcp` package lands on PyPI in **v0.2**. Until
> then, this config will fail with "command not found". Star
> [`pytheum/pytheum-doc`](https://github.com/pytheum/pytheum-doc) to get
> pinged when it ships.

## Install

1. Locate your Claude Desktop config:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
2. Merge the snippet in [`claude_desktop_config.json.example`](./claude_desktop_config.json.example)
   into that file. If you already have an `"mcpServers"` block, add `"pytheum"`
   alongside your other servers — don't replace the whole block.
3. Restart Claude Desktop. You should see a hammer icon listing pytheum's
   tools in the chat composer.

## What you get

Once the server is live, Claude can call:

- `find_relevant_markets(query, limit?)` — wraps `/v1/markets/relevant-to`
- `get_market_context(market_id, limit?)` — wraps `/v1/markets/{id}/context`
- `get_bundle_context(bundle_id, limit?)` — wraps `/v1/bundles/{id}/context`
- `get_event_related_markets(event_id, limit?)` — wraps `/v1/events/{id}/related-markets`

The server runs over stdio via `uvx`, so you don't need to clone anything —
`uvx` fetches `pytheum-mcp` from PyPI on first launch and caches it.

## Configuration

The only env var the server cares about today is `PYTHEUM_API_BASE`
(defaults to `https://api.pytheum.com`). Override it to point at a staging
environment or a local stub.

```json
"env": { "PYTHEUM_API_BASE": "https://staging.api.pytheum.com" }
```

## Troubleshooting

- **"command not found: uvx"** — install [uv](https://docs.astral.sh/uv/) first
  (`curl -LsSf https://astral.sh/uv/install.sh | sh`).
- **No hammer icon** — open Claude Desktop's "Settings → Developer →
  Open MCP log" and look for `pytheum` lines.
- **All tool calls return 404** — your `PYTHEUM_API_BASE` is pointing somewhere
  without the v1 routes; drop the env var and let it default.

See [`docs/api/`](../../docs/api/) for the underlying HTTP shape if you want
to verify the server's tool outputs against the raw API.
