# Visitor counter Worker

A tiny Cloudflare Worker + KV that powers the unique-visitor count shown in the
site footer. Free tier is far more than enough (100k reads + 1k writes/day).

## What it does
- Counts **unique visitors** (one count per browser, via a 1-year `df_visitor` cookie).
- Stores the total in a single KV key `unique_visitors`.
- Returns `{ "count": <number> }` as JSON with CORS for `destinationfaang.com`.

## One-time deploy

Prerequisites: a Cloudflare account and Node.js installed.

```bash
cd worker

# 1. Log in
npx wrangler login

# 2. Create the KV namespace, then paste the printed id into wrangler.toml
#    (the `id = "REPLACE_WITH_YOUR_KV_NAMESPACE_ID"` line).
npx wrangler kv namespace create COUNTER

# 3. Deploy
npx wrangler deploy
```

`wrangler deploy` prints the Worker URL, e.g.
`https://df-visitor-counter.<your-subdomain>.workers.dev`.

## Wire it to the site
Open `assets/visitor-counter.js` and set `COUNTER_ENDPOINT` to that URL.

**Recommended:** map the Worker to `counter.destinationfaang.com` (uncomment the
`routes` block in `wrangler.toml`, redeploy) so it is same-site with the main
domain and cookies are first-party. Then set
`COUNTER_ENDPOINT = "https://counter.destinationfaang.com"`.

## Notes
- KV is eventually consistent, so under heavy concurrent traffic the count may
  be off by a few — perfectly fine for a visitor counter.
- To reset/seed the count: `npx wrangler kv key put --binding COUNTER unique_visitors 1000`.
