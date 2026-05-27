```bash
# Discover an event_id from any context response, then chase it back.
EVENT_ID=$(curl -sG 'https://api.pytheum.com/v1/markets/polymarket:101772/context' \
  --data-urlencode 'limit=1' | jq -r '.context[0].event_id')

curl -sG "https://api.pytheum.com/v1/events/${EVENT_ID}/related-markets" \
  --data-urlencode 'limit=5' \
  | jq
```
