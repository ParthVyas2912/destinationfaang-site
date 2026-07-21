# Design an API Gateway (Architecture Deep Dive)

| | |
|---|---|
| **Publish order** | 046 |
| **Course #** | 117 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~28 min |
| **Primary search keyword** | `design api gateway` |
| **Demand** | High |

**Thumbnail text idea:** FRONT DOOR
**One-line hook (first 15s):** An API gateway is the front door of your platform: auth, routing, rate limits, observability, and failure policy before traffic touches services.

## Learning objectives
- Design gateway responsibilities and what not to put there.
- Explain routing, auth, rate limiting, TLS termination, request shaping, and observability.
- Compare API gateway, load balancer, service mesh, and BFF.
- Handle retries, timeouts, versioning, and multi-tenant isolation.

## Topics & items to cover
- **Step 1 — Requirements:** route external requests to services, validate auth/JWT, rate-limit tenants, terminate TLS, log/trace, transform/version APIs. Exclude business logic and long-running workflows. Gateway must be highly available and low latency.
- **Step 2 — Estimation:** all external QPS passes through gateway; design horizontal stateless fleet. Rate-limit state may use Redis/local tokens; logs are high-volume async.
- **Step 3 — API/Data model:** route config `host/path/method → upstream`, `Consumer`, `APIKey`, `Quota`, `Policy`, `Certificate`. Admin APIs for config deploy and rollback.
- **Step 4 — HLD:** clients → CDN/WAF → L4/L7 load balancer → gateway fleet → service discovery/upstreams; side channel to auth service, rate-limit store, config control plane, logging pipeline.
- **Step 5 — Deep dives:** 1) Rate limiting: local token bucket with Redis/global quota fallback. 2) Auth: verify JWT locally via JWKS cache; introspect opaque tokens only when needed. 3) Reliability: timeouts, circuit breakers, retries only for idempotent methods.
- **Step 6 — Wrap-up:** gateway enforces cross-cutting policy; services still own authorization/business rules.

## Anecdotes & war stories to use
- Netflix Zuul is a famous API gateway story for routing and resilience at large scale.
- Kong/Envoy/NGINX demonstrate common gateway architecture: plugins/filters, upstream clusters, dynamic config.
- AWS API Gateway shows managed throttling, auth integration, and stage/version concepts.
- Google’s BeyondCorp/IAP-style patterns illustrate identity-aware access at the edge.

## Things to mention / interview tips
- Draw a clear line: authentication at gateway, fine-grained authorization in services.
- Mention config rollout safety: versioned config, canary, instant rollback.
- Add correlation IDs and distributed tracing headers.
- Avoid retry storms: budgeted retries with jitter and idempotency checks.

## Common mistakes to call out
- Putting domain-specific business logic in gateway plugins.
- Making gateway call auth DB synchronously for every request.
- Retrying POST/payment requests blindly.
- Forgetting gateway itself is now a critical dependency.

## Diagrams / visuals to draw on screen
- Edge stack: CDN/WAF/LB/API gateway/services.
- Gateway request filter chain: TLS → auth → rate limit → route → observe.
- Control plane pushing config to data-plane gateways.

## Series glue
- Reference REST/gRPC/GraphQL, Rate Limiter, and Observability; next Bloom Filters covers one small data structure gateways sometimes use for fast membership checks. CTA: subscribe and get config examples on GitHub.
