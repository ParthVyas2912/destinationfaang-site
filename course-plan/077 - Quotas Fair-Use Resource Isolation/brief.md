# Quotas, Fair-Use & Resource Isolation

| | |
|---|---|
| **Publish order** | 077 |
| **Course #** | 52 |
| **Module** | M05 — Microservices & Reliability |
| **Type** | concept |
| **Target length** | ~10 min |
| **Primary search keyword** | `rate limiting quotas` |
| **Demand** | Moderate |

**Thumbnail text idea:** FAIR USE
**One-line hook (first 15s):** A quota is how your system says: one customer cannot turn everyone else’s outage into their feature launch.

## Learning objectives
- Distinguish rate limits, quotas, concurrency limits, and reservations.
- Implement token bucket and leaky bucket controls with concrete keys.
- Design fair sharing across tenants, users, APIs, and jobs.
- Explain user-facing throttling behavior.

## Topics & items to cover
- Hook: one tenant exports every report and starves the shared worker queue.
- Definition: quotas and fair-use controls bound resource consumption so quality stays predictable.
- Worked example: tenant `acme` gets 100 requests/sec, burst 200 via token bucket keyed by `tenant_id:endpoint`; exports get 5 concurrent jobs and 50GB/day.
- How it works: token refill, Redis counters, local prefetch, priority queues, weighted fair queuing, 429 with `Retry-After`, admin overrides.
- Tradeoffs: strict limits protect systems but annoy customers; distributed counters are approximate; user and tenant limits must compose.
- Real-world usage: GitHub API limits, AWS service quotas, Kubernetes requests/limits, cloud billing guardrails.
- Interview sentence: "I’d enforce quotas at the edge for requests and inside worker pools for expensive resources, keyed by tenant and operation cost."
- Recap: rate limiting protects APIs; resource isolation protects the platform.

## Anecdotes & war stories to use
- Public APIs such as GitHub expose rate-limit headers so clients can adapt.
- Kubernetes popularized CPU/memory requests and limits for multi-tenant clusters.
- Cloud providers use service quotas to prevent accidental runaway spend and capacity abuse.
- SaaS systems often learn background jobs need quotas as much as synchronous APIs.

## Things to mention / interview tips
- Limit by cost units, not only request count.
- Include metrics: top throttled tenants, near-limit alerts, override audit logs.
- Return deterministic 429/403 instead of random timeouts.
- Use hierarchical limits: user, tenant, region, global.

## Common mistakes to call out
- Limiting API calls while exports and webhooks remain unbounded.
- Using one global limit that punishes all customers.
- Forgetting retries can amplify throttling storms.
- Not documenting limits to clients.

## Diagrams / visuals to draw on screen
- Token bucket refill and burst drain.
- Hierarchical quota tree: global, tenant, user, endpoint.
- Worker pool with per-tenant lanes.

## Series glue
- Continues multi-tenancy by making fairness enforceable; next is chaos engineering to test failure assumptions. CTA: subscribe and check GitHub examples.
