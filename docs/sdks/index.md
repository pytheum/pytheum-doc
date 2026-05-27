# SDKs

> All SDKs are thin wrappers over [`openapi.yaml`](../../openapi.yaml) — generated where possible, hand-maintained for ergonomics. Anything you can do with `curl` today, you can do with an SDK once it lands. Nothing is gated behind the SDK.

Three official SDKs are planned for v0.2. None are shipped yet — install snippets are placeholders pinned for when packages publish.

## `pytheum-mcp` — MCP server

**Status**: v0.1.0 code complete; awaiting first publish to PyPI + npm.
**Source**: [github.com/pytheum/pytheum-mcp](https://github.com/pytheum/pytheum-mcp)

The MCP server for AI agents (Claude Desktop, Cursor, Windsurf, any MCP-compatible client). Ships as a Python package on PyPI plus a thin npm shim — same code path, two install routes:

```bash
# via npm (no Python required on the client; Claude Desktop's default)
npx -y @pytheum/mcp

# via PyPI (Python-native)
uvx pytheum-mcp
```

Exposes the four context endpoints as MCP tools so an agent can call `t_find_markets("fed cut june")` natively. Full setup in [`docs/quickstart/mcp.md`](../quickstart/mcp.md).

## `pytheum` — Python client

**Status**: planned, v0.2. Sync + async, fully typed.

```bash
# Placeholder — package not yet on PyPI
pip install pytheum
```

Example call (matching the curl quickstart):

```python
from pytheum import Pytheum

client = Pytheum()  # no auth in v0; reads PYTHEUM_API_KEY in v0.2+
markets = client.markets.relevant_to(query="fed cut june", limit=5)
for m in markets:
    print(m.id, m.similarity, m.question)
```

Async variant:

```python
from pytheum import AsyncPytheum

async with AsyncPytheum() as client:
    markets = await client.markets.relevant_to(query="fed cut june", limit=5)
```

## `@pytheum/client` — TypeScript client

**Status**: planned, v0.2. Works in Node and modern browsers.

```bash
# Placeholder — package not yet on npm
npm install @pytheum/client
```

Example:

```ts
import { Pytheum } from "@pytheum/client";

const client = new Pytheum();
const { markets } = await client.markets.relevantTo({
  query: "fed cut june",
  limit: 5,
});
console.log(markets.map((m) => `${m.id}\t${m.similarity}\t${m.question}`));
```

## Until they ship

Hit the HTTP API directly — see [`docs/quickstart/curl.md`](../quickstart/curl.md). All four endpoints are stable and won't change shape under the SDK release.

## See also

- [API overview](../api/overview.md)
- [MCP quickstart](../quickstart/mcp.md)
- [ROADMAP](../../ROADMAP.md)
