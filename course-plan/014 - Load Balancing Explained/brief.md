# Load Balancing Explained (L4 vs L7, DNS, Anycast)

| | |
|---|---|
| **Publish order** | 014 |
| **Course #** | 16 |
| **Module** | M02 — Networking & Delivery |
| **Type** | concept |
| **Target length** | ~18 min |
| **Primary search keyword** | `load balancing` |
| **Demand** | Very High |

**Thumbnail text idea:** ROUTE TRAFFIC
**One-line hook (first 15s):** Load balancers are where availability, latency, and failure isolation become concrete.

## Learning objectives
- Distinguish DNS, L4, L7, and Anycast load balancing.
- Explain health checks, connection draining, and failure isolation.
- Choose a balancing strategy for web, API, and regional traffic.

## Topics & items to cover
- Hook: one server dies; users should not know, but existing requests should not be dropped randomly.
- Definition: load balancing distributes traffic across healthy backends while enforcing routing, capacity, and failure policies.
- How it works: DNS sends users to nearest region; Anycast routes to nearest edge; L4 balances TCP connections by 5-tuple; L7 reverse proxy routes `/api/payments` to payment service and can use headers/cookies.
- Tradeoffs: DNS is simple but cached; L4 is fast and protocol-agnostic; L7 is smarter but costlier; sticky sessions help stateful apps but hurt balancing.
- Real-world usage: NGINX/Envoy/HAProxy, AWS ALB/NLB, Google Global Load Balancer, Cloudflare edge.
- Exact interview sentence: "I would use global DNS/Anycast for regional entry and L7 load balancing inside the region for path-based routing and health-aware retries."
- Recap: load balancing is part routing, part health management, part blast-radius control.

## Anecdotes & war stories to use
- Cloudflare's Anycast network is a public example of routing users to nearby edge capacity.
- The 2021 Facebook outage involved BGP reachability issues, showing global routing can take services off the internet.
- Envoy became widely adopted through service-mesh patterns where L7 retries, timeouts, and circuit breaking matter.

## Things to mention / interview tips
- Mention active and passive health checks.
- Explain connection draining during deploys.
- Avoid retry storms: retries need budgets and backoff.
- State whether sessions are stateless or sticky.

## Common mistakes to call out
- Assuming round-robin is enough.
- Forgetting health checks and slow-start after recovery.
- Retrying non-idempotent requests blindly.
- Using sticky sessions to hide bad state management.

## Diagrams / visuals to draw on screen
- Global DNS/Anycast to regional load balancer.
- L4 versus L7 packet/request routing.
- Health check and connection draining timeline.

## Series glue
- Reference Uber regional routing; point forward to notification systems where provider failover uses similar health logic. CTA: subscribe and see configs in GitHub.
