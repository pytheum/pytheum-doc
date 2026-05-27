# integrations/

This directory is reserved for third-party integration recipes — things
like a LangChain tool wrapper, a Vercel AI SDK adapter, a LlamaIndex
retriever, or an OpenAI Responses API tool spec.

Not currently shipping any. See:

- [`examples/`](../examples/) — runnable scaffolds (MCP server config,
  Python httpx quickstart, Next.js App Router route handler).
- [`docs/sdks/`](../docs/sdks/) — the official SDK roadmap.
- [`docs/snippets/`](../docs/snippets/) — short per-endpoint copy-paste
  fragments in curl, Python, and TypeScript.

PRs that add a working recipe are welcome — open an issue first so we
can sketch the shape before you build it.
