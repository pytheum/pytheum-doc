```python
import httpx

with httpx.Client(base_url="https://api.pytheum.com", timeout=30.0) as client:
    # Discover an event_id from any context response.
    ctx = client.get(
        "/v1/markets/polymarket:101772/context",
        params={"limit": 1},
    ).json()
    event_id = ctx["context"][0]["event_id"]

    r = client.get(
        f"/v1/events/{event_id}/related-markets",
        params={"limit": 5},
    )
    r.raise_for_status()
    for m in r.json()["markets"]:
        print(f"[{m['similarity']:.3f}] {m['id']:<30} {m.get('question') or ''}")
```
