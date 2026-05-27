```ts
const bundleId = "polymarket:fomc";
const url = new URL(`https://api.pytheum.com/v1/bundles/${bundleId}/context`);
url.searchParams.set("limit", "5");

const res = await fetch(url);
if (!res.ok) throw new Error(`pytheum ${res.status}`);
const data = await res.json();
console.log("bundle:", data.bundle);
for (const ev of data.context) {
  console.log(`  ${ev.kind.padEnd(14)} ${ev.event_id.slice(0, 24)}`);
}
```
