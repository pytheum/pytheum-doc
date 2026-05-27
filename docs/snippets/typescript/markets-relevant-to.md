```ts
const url = new URL("https://api.pytheum.com/v1/markets/relevant-to");
url.searchParams.set("query", "fed cut june");
url.searchParams.set("limit", "5");

const res = await fetch(url);
if (!res.ok) throw new Error(`pytheum ${res.status}`);
const data = await res.json();
for (const m of data.markets) {
  console.log(`[${m.similarity.toFixed(3)}] ${m.id.padEnd(30)} ${m.question ?? ""}`);
}
```
