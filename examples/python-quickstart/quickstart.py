"""End-to-end quickstart against api.pytheum.com.

Walks all four endpoints in order, discovering IDs as it goes:
  relevant-to -> market context -> bundle context -> event related-markets

Run:
    pip install -r requirements.txt
    python quickstart.py
"""

from __future__ import annotations

import asyncio
import json

import httpx

API_BASE = "https://api.pytheum.com"
QUERY = "fed cut june"
LIMIT = 5


def _print_header(title: str) -> None:
    bar = "=" * 72
    print(f"\n{bar}\n{title}\n{bar}")


async def main() -> None:
    async with httpx.AsyncClient(base_url=API_BASE, timeout=30.0) as client:
        # 1. Find markets matching a query.
        _print_header(f"1. /v1/markets/relevant-to?query={QUERY!r}")
        r = await client.get(
            "/v1/markets/relevant-to",
            params={"query": QUERY, "limit": LIMIT},
        )
        r.raise_for_status()
        relevant = r.json()
        markets = relevant.get("markets", [])
        if not markets:
            print("No markets matched the query — try lowering min_similarity.")
            return
        for m in markets:
            print(f"  [{m['similarity']:.3f}] {m['id']:<30} {m.get('question') or ''}")

        top = markets[0]
        market_id = top["id"]
        bundle_id = top.get("bundle_id")

        # 2. Pull events paired with the top market.
        _print_header(f"2. /v1/markets/{market_id}/context")
        r = await client.get(
            f"/v1/markets/{market_id}/context",
            params={"limit": LIMIT},
        )
        r.raise_for_status()
        market_ctx = r.json()
        events = market_ctx.get("context", [])
        print(f"  market: {market_ctx.get('market', {}).get('question')}")
        print(f"  total_in_window: {market_ctx.get('meta', {}).get('total_in_window')}")
        for ev in events:
            sim = ev.get("similarity")
            sim_s = f"{sim:.3f}" if sim is not None else "  -  "
            title = ev.get("snapshot", {}).get("title") or ev.get("snapshot", {}).get("text") or ""
            print(f"  [{sim_s}] {ev['kind']:<14} {ev['event_id'][:24]}  {title[:60]}")

        # 3. Fan out to the whole bundle (if the top market is in one).
        if bundle_id:
            _print_header(f"3. /v1/bundles/{bundle_id}/context")
            r = await client.get(
                f"/v1/bundles/{bundle_id}/context",
                params={"limit": LIMIT},
            )
            r.raise_for_status()
            bundle_ctx = r.json()
            print(f"  bundle: {json.dumps(bundle_ctx.get('bundle'), indent=2)}")
            for ev in bundle_ctx.get("context", []):
                title = ev.get("snapshot", {}).get("title") or ""
                print(f"  - {ev['kind']:<14} {ev['event_id'][:24]}  {title[:60]}")
        else:
            print("\n(Top market has no bundle_id, skipping step 3.)")

        # 4. Walk the first event back to its markets.
        if not events:
            print("\n(No events in the market context window, skipping step 4.)")
            return
        event_id = events[0]["event_id"]
        _print_header(f"4. /v1/events/{event_id}/related-markets")
        r = await client.get(
            f"/v1/events/{event_id}/related-markets",
            params={"limit": LIMIT},
        )
        r.raise_for_status()
        related = r.json()
        for m in related.get("markets", []):
            print(f"  [{m['similarity']:.3f}] {m['id']:<30} {m.get('question') or ''}")


if __name__ == "__main__":
    asyncio.run(main())
