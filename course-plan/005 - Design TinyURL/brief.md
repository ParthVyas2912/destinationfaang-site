# Design TinyURL — System Design Interview (Step by Step)

| | |
|---|---|
| **Publish order** | 005 |
| **Course #** | 88 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~30 min |
| **Primary search keyword** | `design tinyurl` |
| **Demand** | Very High |

**Thumbnail text idea:** SHORT LINKS
**One-line hook (first 15s):** TinyURL looks easy until I ask: what happens when one hot link gets 10 million clicks in an hour?

## Learning objectives
- Turn a URL shortener into clear functional and non-functional requirements.
- Design collision-free short code generation and redirect storage.
- Handle hot links, abuse, expiration, and analytics without slowing redirects.

## Topics & items to cover
- Requirements: shorten long URLs, redirect `GET /{code}`, optional custom aliases, TTL, owner dashboard, abuse takedown.
- Estimation: 100M new links/month, 10:1 read/write ratio, 7-character Base62 gives trillions of combinations; redirects need low tens-of-ms latency.
- API/Data model: `POST /v1/links {long_url, custom_alias, expires_at}`, `GET /{code}`; table `links(code PK, long_url, owner_id, created_at, expires_at, status)`; analytics event stream keyed by `code`.
- High-level design: API service validates URL, ID generator allocates code, primary store holds mapping, Redis/CDN cache serves redirects, Kafka collects click events asynchronously.
- Deep dives/bottlenecks: ID generation via Snowflake/sequence-to-Base62 avoids random collision loops; hot celebrity links need CDN/edge cache and request coalescing; abuse scanning should be async but status checks must be on redirect path.
- Wrap-up: state SLOs, failure mode if analytics is down, and migration path for multi-region active-active.

## Anecdotes & war stories to use
- TinyURL popularized simple aliases; bitly added analytics and branded links, which is why redirects and click events should be separated.
- Twitter's `t.co` wraps every outbound link for safety scanning and analytics, showing that URL shorteners become security infrastructure.
- Snowflake-style IDs came from Twitter's need for distributed unique IDs without a single database bottleneck.

## Things to mention / interview tips
- Say: "Redirect latency is the product path; analytics is off the critical path."
- Pick `code` as the shard/cache key and explain hot-key mitigation.
- Clarify whether custom aliases must be globally unique.
- Discuss malicious URLs, phishing reports, and disabled-link states.

## Common mistakes to call out
- Generating random strings without a collision strategy.
- Putting click aggregation synchronously in `GET /{code}`.
- Ignoring expired, banned, or custom links.
- Assuming a relational auto-increment ID works unchanged across regions.

## Diagrams / visuals to draw on screen
- Request flow from shorten API to ID generator to storage.
- Redirect fast path with CDN/Redis and fallback database lookup.
- Analytics pipeline: redirect service to Kafka to batch counters.

## Series glue
- Reference earlier scalability and hashing ideas; point forward to Twitter/X where ID generation and hot keys become harder. CTA: subscribe and grab the diagrams/code from the GitHub repo.
