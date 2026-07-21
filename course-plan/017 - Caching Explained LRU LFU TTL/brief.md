# Caching Explained: LRU, LFU & TTL (Interview Guide)

| | |
|---|---|
| **Publish order** | 017 |
| **Course #** | 31 |
| **Module** | M03 — Data, Storage & Caching |
| **Type** | concept |
| **Target length** | ~16 min |
| **Primary search keyword** | `caching lru lfu ttl` |
| **Demand** | High |

**Thumbnail text idea:** CACHE WISELY
**One-line hook (first 15s):** Caching is the fastest way to speed up a system and the fastest way to serve stale or wrong data.

## Learning objectives
- Explain LRU, LFU, TTL, write-through, and cache-aside patterns.
- Choose cache keys, eviction policy, and invalidation strategy.
- Identify stampedes, hot keys, and stale data risks.

## Topics & items to cover
- Hook: a single product page gets featured; without cache control, your database becomes the cache.
- Definition: a cache stores computed or fetched data closer to the request path with an eviction and freshness policy.
- How it works: product `p123` is read 10,000 times/minute; cache-aside checks `product:p123`, DB miss costs 20 ms, Redis hit costs 1 ms, TTL 5 minutes bounds staleness; LRU evicts least recently used keys when memory fills, LFU protects frequently used keys.
- Tradeoffs: LRU adapts to recency but can be polluted by scans; LFU handles hot items but is slower/more stateful; TTL is simple but can serve stale data; invalidation is precise but complex.
- Real-world usage: CDN edge caches, Redis/Memcached for app data, browser caches, database buffer pools.
- Exact interview sentence: "I would use cache-aside with TTL plus explicit invalidation on writes for hot read-heavy objects, and protect misses with request coalescing."
- Recap: caching is an optimization with correctness consequences.

## Anecdotes & war stories to use
- Memcached became famous at Facebook and other large web companies for reducing database read load.
- CDN cache behavior has caused high-profile stale-content and outage incidents, proving invalidation matters.
- Cache stampedes are common enough that patterns like request coalescing and probabilistic early refresh are standard.

## Things to mention / interview tips
- Always name the cache key and invalidation trigger.
- Mention TTL jitter to avoid synchronized expiry.
- Protect hot keys with replication/local caching.
- Track hit rate, p99 latency, and stale-read tolerance.

## Common mistakes to call out
- Saying "just add Redis" without a freshness plan.
- Caching per-user secrets with shared keys.
- Letting all requests regenerate an expired key.
- Using TTL when the business requires read-after-write.

## Diagrams / visuals to draw on screen
- Cache-aside read miss/hit sequence.
- LRU versus LFU eviction example.
- Stampede timeline and request coalescing fix.

## Series glue
- Reference autocomplete hot-prefix caching; point forward to Dropbox where local and server metadata caches matter. CTA: subscribe and check repo exercises.
