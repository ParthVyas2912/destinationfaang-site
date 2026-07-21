# Design a Rate Limiter — System Design Interview

| | |
|---|---|
| **Publish order** | 011 |
| **Course #** | 18 |
| **Module** | M02 — Networking & Delivery |
| **Type** | concept |
| **Target length** | ~20 min |
| **Primary search keyword** | `design rate limiter` |
| **Demand** | Very High |

**Thumbnail text idea:** STOP ABUSE
**One-line hook (first 15s):** A good rate limiter is not just a counter; it is a fairness contract at the edge of your system.

## Learning objectives
- Compare fixed window, sliding window, leaky bucket, and token bucket limiters.
- Design distributed counters that work at API gateway scale.
- Explain fairness, burst handling, and failure behavior.

## Topics & items to cover
- Hook: one API key sends 10,000 login attempts in a minute; what blocks it without hurting everyone else?
- Definition: a rate limiter enforces a policy like `100 requests/user/minute` or `10 writes/IP/second` before expensive work happens.
- How it works: token bucket with capacity 100 and refill 10 tokens/sec lets a user burst to 100 then sustain 10/sec; each request atomically decrements Redis key `rl:{user_id}:{route}` with TTL.
- Tradeoffs: fixed windows are simple but bursty at boundaries; sliding logs are accurate but memory-heavy; approximate counters are cheaper; local limiters are fast but less globally fair.
- Real-world usage: API gateways, login protection, GitHub/Twitter API quotas, Stripe idempotency plus throttling for payment endpoints.
- Exact interview sentence: "I would enforce coarse limits at the edge and precise per-user or per-tenant limits in Redis using token buckets with fail-closed only for abusive paths."
- Recap: limiter policy, key, algorithm, and failure mode matter more than naming an algorithm.

## Anecdotes & war stories to use
- Public APIs like GitHub and X/Twitter expose rate-limit headers, making quotas visible to clients.
- Cloudflare and Fastly outages illustrate how edge infrastructure decisions can affect huge parts of the web.
- Login brute-force defenses often combine IP, account, and device limits because any single key is easy to evade.

## Things to mention / interview tips
- Name the limiter key: user ID, API key, IP, route, tenant, or combination.
- Return `429` with `Retry-After` and rate-limit headers.
- Mention atomic operations/Lua scripts for Redis token updates.
- Decide fail-open versus fail-closed based on endpoint risk.

## Common mistakes to call out
- Using only IP limits and breaking NAT/mobile users.
- Putting limiter checks after expensive database work.
- Ignoring burst behavior at fixed-window boundaries.
- Assuming one global counter scales.

## Diagrams / visuals to draw on screen
- Token bucket fill/drain timeline.
- API gateway to Redis cluster limiter path.
- Multi-key policy matrix for login versus read API.

## Series glue
- Reference CAP/counter consistency tradeoffs; point forward to video streaming where quotas also protect transcode and bandwidth. CTA: subscribe and use repo snippets.
