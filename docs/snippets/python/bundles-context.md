```python
import httpx

bundle_id = "polymarket:fomc"
with httpx.Client(base_url="https://api.pytheum.com", timeout=30.0) as client:
    r = client.get(
        f"/v1/bundles/{bundle_id}/context",
        params={"limit": 5},
    )
    r.raise_for_status()
    data = r.json()
    print("bundle:", data["bundle"])
    for ev in data["context"]:
        print(f"  {ev['kind']:<14} {ev['event_id'][:24]}")
```
