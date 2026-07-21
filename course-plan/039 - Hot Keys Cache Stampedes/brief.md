# Hot Keys & Cache Stampedes (and How to Fix Them)

| | |
|---|---|
| **Publish order** | 039 |
| **Course #** | 34 |
| **Module** | M03 — Data, Storage & Caching |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `cache stampede` |
| **Demand** | Moderate |

**Thumbnail text idea:** CACHE MELTDOWN
**One-line hook (first 15s):** Your cache can save your database—or synchronize 10,000 clients to attack it at the exact same second.

## Learning objectives
- Explain hot keys, cache stampedes, thundering herds, and penetration.
- Apply mutexes, request coalescing, TTL jitter, stale-while-revalidate, and negative caching.
- Design cache protection for a concrete celebrity/product/flash-sale key.
- Know when to replicate, shard, or bypass a hot cache key.

## Topics & items to cover
- **Hook:** one viral product detail page expires from cache and every request misses at once.
- **Definition:** a hot key is a key with disproportionate traffic; a stampede is many clients recomputing/refetching the same expired value simultaneously.
- **Worked example:** `product:ps5` gets 50k RPS. TTL is 60s. If it expires globally, 50k requests hit DB/API. Fix: early refresh at 50s by one worker, serve stale up to 5 minutes, add TTL jitter ±10%, and use single-flight lock so only one request recomputes.
- **Tradeoffs:** stale serving improves availability but may show old prices/stock; locks reduce load but can become bottlenecks; replication helps reads but not expensive recomputation.
- **Real-world usage:** news homepages, celebrity profiles, flash-sale inventory, ad campaign configs, feature flags.
- **Interview sentence:** “For hot keys, I’ll prefer stale-while-revalidate plus request coalescing so expiry does not turn into synchronized database load.”
- **Recap:** cache design includes failure behavior at expiry.

## Anecdotes & war stories to use
- Facebook’s “memcache at Facebook” paper describes large-scale cache deployment and operational issues around hot keys.
- Redis has documented hot key detection and clustering implications; a single key can overload one shard.
- CDN origin-shield designs exist largely to prevent global cache misses from stampeding the origin.
- Many outage writeups cite thundering herds after cache flushes or deploys, making “never flush everything at once” practical advice.

## Things to mention / interview tips
- Define cache key cardinality and traffic distribution; interviewers love seeing skew awareness.
- Use TTL jitter whenever many keys are written at the same time.
- Add negative caching for nonexistent IDs to stop cache penetration.
- For mutable hot inventory, separate display cache from authoritative write path.

## Common mistakes to call out
- Setting identical TTLs for millions of keys loaded by a batch job.
- Using a distributed lock without timeout/fallback.
- Caching “not found” forever and hiding newly created data.
- Believing more cache nodes automatically fix one single hot key.

## Diagrams / visuals to draw on screen
- Timeline of TTL expiry causing DB spike.
- Single-flight/request coalescing flow.
- Stale-while-revalidate cache state diagram.

## Series glue
- Connect to CDN, Caching, and Ticket Booking; next Inventory case applies hot-key thinking to stock counts. CTA: subscribe and get cache patterns on GitHub.
