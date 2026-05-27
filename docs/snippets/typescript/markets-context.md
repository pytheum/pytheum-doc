```ts
const marketId = "polymarket:101772";
const url = new URL(`https://api.pytheum.com/v1/markets/${marketId}/context`);
url.searchParams.set("limit", "5");

const res = await fetch(url);
if (!res.ok) throw new Error(`pytheum ${res.status}`);
const data = await res.json();
console.log("market:", data.market.question);
for (const ev of data.context) {
  const title: string = ev.snapshot?.title ?? ev.snapshot?.text ?? "";
  console.log(`  ${ev.kind.padEnd(14)} ${ev.event_id.slice(0, 24)}  ${title.slice(0, 60)}`);
}
```
