# Layered Caching: CDN, App & Client Caches

| | |
|---|---|
| **Publish order** | 055 |
| **Course #** | 32 |
| **Module** | M03 — Data, Storage & Caching |
| **Type** | concept |
| **Target length** | ~12 min |
| **Primary search keyword** | `layered caching` |
| **Demand** | Moderate |

**Thumbnail text idea:** CACHE LAYERS
**One-line hook (first 15s):** The fastest request is the one your origin never sees—but every cache layer can also serve the wrong thing.

## Learning objectives
- Distinguish CDN, browser, app, and database caches.
- Design cache keys, TTLs, invalidation, stale behavior, and stampede control.
- Avoid privacy leaks from shared caches.

## Topics & items to cover
- Hook: one product page may hit browser cache, CDN, Redis, and DB buffer cache before rendering.
- Definition: layered caching stores reusable data at multiple distances from the user, each with different latency and consistency.
- Worked example: `/products/123?currency=USD`. Browser caches fingerprinted images for a year; CDN caches HTML for 60s with key `{path,country,currency}`; app Redis caches `product:123:v42` for 5 minutes; DB is source of truth. On price update, publish Redis invalidation and CDN purge by surrogate key `product-123`.
- Tradeoffs: lower latency and cost; harder invalidation, stale data, key explosion, personalized data hazards.
- Real-world usage: Cloudflare/Fastly CDNs, Redis/Memcached, mobile offline caches.
- Interview sentence: “Cache immutable assets aggressively, shared dynamic data with short TTL plus purge, and personalized data only when the user is in the key.”
- Recap: cache placement follows reuse, freshness, and blast radius.

## Anecdotes & war stories to use
- CDN outages at major providers have taken large parts of the web offline, showing value and concentration risk.
- Fastly surrogate-key purging is a known pattern for invalidating related objects.
- Privacy incidents often stem from shared caches missing `Vary` or auth-aware keys.

## Things to mention / interview tips
- Say the exact cache key out loud.
- Distinguish TTL from event-driven invalidation.
- Add request coalescing/locks for stampede prevention.

## Common mistakes to call out
- Caching per-user data under a shared key.
- Assuming purge is instant everywhere.
- Using one TTL for all data.

## Diagrams / visuals to draw on screen
- Browser → CDN → app cache → DB ladder.
- Cache key examples.
- Stale-while-revalidate timeline.

## Series glue
- Sets up write-through vs write-back caching. Next: cloud data warehouse design. Subscribe and check GitHub.
