```python
import httpx

with httpx.Client(base_url="https://api.pytheum.com", timeout=30.0) as client:
    r = client.get(
        "/v1/markets/relevant-to",
        params={"query": "fed cut june", "limit": 5},
    )
    r.raise_for_status()
    for m in r.json()["markets"]:
        print(f"[{m['similarity']:.3f}] {m['id']:<30} {m.get('question') or ''}")
```
