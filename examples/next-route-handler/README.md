# Next.js App Router — pytheum proxy route

A minimal Next.js 14+ App Router route handler that calls
`https://api.pytheum.com/v1/markets/relevant-to` and returns the JSON
verbatim. Use it as a server-side proxy from your own UI.

## Caveats

- **Server-side only.** pytheum does not currently send permissive
  CORS headers, so you cannot fetch `api.pytheum.com` directly from
  browser JavaScript. This route handler is the workaround — it runs in
  your Next.js server and your client hits your own origin.
- **Cache as you like.** This example uses `revalidate = 60` so
  Vercel/Next will cache the response for a minute. Tune per your needs.
- **No auth needed today.** Once pytheum adds auth, you'd inject the
  API key here so it never reaches the browser.

## Drop into an existing Next.js project

Copy `app/api/related-markets/route.ts` into the same path under your
`app/` directory. From the client:

```ts
const res = await fetch(`/api/related-markets?q=${encodeURIComponent("fed cut june")}`);
const data = await res.json();
```

## Run standalone

```bash
npm install
npm run dev
# Then: http://localhost:3000/api/related-markets?q=fed%20cut%20june
```

## What it returns

Whatever `https://api.pytheum.com/v1/markets/relevant-to` returns —
see the [OpenAPI spec](../../openapi.yaml) for the schema. The route
forwards `query` and clamps `limit` to a sane default of 5.
