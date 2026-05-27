```ts
// Discover an event_id from any context response.
const ctxUrl = new URL("https://api.pytheum.com/v1/markets/polymarket:101772/context");
ctxUrl.searchParams.set("limit", "1");
const ctx = await (await fetch(ctxUrl)).json();
const eventId: string = ctx.context[0].event_id;

const url = new URL(`https://api.pytheum.com/v1/events/${eventId}/related-markets`);
url.searchParams.set("limit", "5");
const res = await fetch(url);
if (!res.ok) throw new Error(`pytheum ${res.status}`);
const data = await res.json();
for (const m of data.markets) {
  console.log(`[${m.similarity.toFixed(3)}] ${m.id.padEnd(30)} ${m.question ?? ""}`);
}
```
