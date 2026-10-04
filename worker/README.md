# Visitor counter Worker

A tiny Cloudflare Worker + KV that powers the unique-visitor count shown in the
site footer. Free tier is far more than enough (100k reads + 1k writes/day).

## What it does
- Counts **unique visitors** (one count per browser, via a 1-year `df_visitor` cookie).
- Stores the total in a single KV key `unique_visitors`.
- Returns `{ "count": <number> }` as JSON with CORS for `destinationengineer.com`,
  `destinationfaang.com`, and both `www` variants during the transition.

## Rebrand deployment

Keep the existing Worker name, KV namespace, `unique_visitors` key, and
`df_visitor` cookie. Renaming any of them is unnecessary and can lose continuity.
The frontend continues to use the existing `workers.dev` endpoint.

```powershell
npx wrangler deploy --dry-run --config .\worker\wrangler.toml
npx wrangler deploy --config .\worker\wrangler.toml
```

Deploy the updated origin allowlist before switching the website domain.
Do not create a new KV namespace for this migration.

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

As a separate change, a custom domain such as `counter.destinationengineer.com`
can make requests same-site. Configure that domain explicitly before changing
`COUNTER_ENDPOINT`; doing so also changes the cookie host. Do not change the
endpoint merely to rebrand the site. Browser third-party-cookie restrictions
can still affect the existing `workers.dev` counter.

## Notes
- KV is eventually consistent, so under heavy concurrent traffic the count may
  be off by a few — perfectly fine for a visitor counter.
- To reset/seed the count: `npx wrangler kv key put --binding COUNTER unique_visitors 1000`.
