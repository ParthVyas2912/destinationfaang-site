# What Is a CDN? Edge Delivery Explained

| | |
|---|---|
| **Publish order** | 031 |
| **Course #** | 17 |
| **Module** | M02 — Networking & Delivery |
| **Type** | concept |
| **Target length** | ~16 min |
| **Primary search keyword** | `what is a cdn` |
| **Demand** | High |

**Thumbnail text idea:** EDGE WINS
**One-line hook (first 15s):** A CDN is not just ‘a cache near users’—it is DNS, routing, invalidation, origin shielding, and failure strategy all in one.

## Learning objectives
- Explain the CDN request path from DNS to edge cache to origin.
- Use cache-control, TTLs, purging, and versioned URLs correctly.
- Describe edge placement, origin shielding, and failover tradeoffs.
- Apply CDN thinking to images, video, APIs, and static assets.

## Topics & items to cover
- **Hook:** a user in Mumbai should not fetch a 2MB image from Virginia if an edge POP can serve it locally.
- **Definition:** a CDN is a geographically distributed edge network that caches and delivers content closer to users while protecting origins.
- **Worked example:** `/logo.v42.png` has `Cache-Control: public, max-age=31536000`; first Mumbai request misses edge and fetches origin, next 100k requests hit the POP. For `/api/feed`, cache for 5 seconds or bypass if personalized.
- **Tradeoffs:** high hit ratio lowers latency/cost; stale data and invalidation complexity increase. Long TTL plus versioned filenames beats constant purges for static assets.
- **Real-world usage:** Netflix Open Connect for video, Cloudflare/Fastly/Akamai for web, image resizing at the edge, software downloads.
- **Interview sentence:** “I’ll serve immutable assets with long TTLs and versioned URLs, and reserve purge/invalidation for exceptional cases.”
- **Recap:** CDN design is cache policy plus routing plus origin protection.

## Anecdotes & war stories to use
- Netflix Open Connect places appliances inside ISPs to move video closer to viewers rather than hauling every stream across the public internet.
- The 2017 AWS S3 us-east-1 outage affected many sites’ static assets, showing why origin dependency and regional assumptions matter.
- Fastly’s 2021 outage briefly took major sites offline, demonstrating the CDN as a critical tier, not a harmless add-on.
- Cloudflare Workers/Fastly Compute show the industry shift from passive caching to programmable edge logic.

## Things to mention / interview tips
- Separate static immutable, static mutable, dynamic public, and personalized content policies.
- Mention origin shield to collapse cache misses before they stampede your origin.
- Say how you purge: surrogate keys, versioned URLs, or short TTLs.
- Discuss TLS termination and WAF/rate-limit features when relevant.

## Common mistakes to call out
- Saying “put CDN in front” without cache keys or headers.
- Caching authenticated responses without varying on auth/user.
- Depending on instant global purge for correctness.
- Ignoring cache-miss storms after deploy or expiry.

## Diagrams / visuals to draw on screen
- DNS/Anycast route to nearest POP, then origin fetch on miss.
- Cache lifecycle: miss → fill → hit → stale/revalidate → purge.
- Origin shield layer collapsing many POP misses.

## Series glue
- Connect to Load Balancing and Caching; next Image CDN case turns this concept into a full design. CTA: subscribe and check GitHub for header examples.
