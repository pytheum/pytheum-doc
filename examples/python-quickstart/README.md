# Python quickstart

Run this in a fresh venv. No SDK needed — uses `httpx` directly against
`https://api.pytheum.com`. All four endpoints are unauthenticated GETs.

## Run

```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python quickstart.py
```

## What it does

The script chains all four endpoints in order, using each response to
discover the next ID so you never have to hardcode a market or event:

1. `/v1/markets/relevant-to?query=fed cut june` — find the top market
2. `/v1/markets/{id}/context` — pull events paired with that market
3. `/v1/bundles/{bundle_id}/context` — fan out to the whole bundle
4. `/v1/events/{event_id}/related-markets` — walk an event back to its markets

Output is plain text to stdout, one section per endpoint.

## No keys

See [`.env.example`](./.env.example) — there are no keys to set for v0.
