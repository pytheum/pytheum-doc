```python
import httpx

market_id = "polymarket:101772"
with httpx.Client(base_url="https://api.pytheum.com", timeout=30.0) as client:
    r = client.get(
        f"/v1/markets/{market_id}/context",
        params={"limit": 5},
    )
    r.raise_for_status()
    data = r.json()
    print("market:", data["market"].get("question"))
    for ev in data["context"]:
        title = ev["snapshot"].get("title") or ev["snapshot"].get("text") or ""
        print(f"  {ev['kind']:<14} {ev['event_id'][:24]}  {title[:60]}")
```
