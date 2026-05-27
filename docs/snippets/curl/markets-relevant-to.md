```bash
curl -sG 'https://api.pytheum.com/v1/markets/relevant-to' \
  --data-urlencode 'query=fed cut june' \
  --data-urlencode 'limit=5' \
  | jq
```
