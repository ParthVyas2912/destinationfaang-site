# Service Discovery & Config Management

| | |
|---|---|
| **Publish order** | 073 |
| **Course #** | 45 |
| **Module** | M05 — Microservices & Reliability |
| **Type** | concept |
| **Target length** | ~12 min |
| **Primary search keyword** | `service discovery` |
| **Demand** | Moderate |

**Thumbnail text idea:** FIND SERVICES
**One-line hook (first 15s):** A microservice call starts with a deceptively hard question: where is the other service right now?

## Learning objectives
- Explain client-side, server-side, and DNS-based discovery.
- Design health checks, registration, and deregistration for autoscaled services.
- Separate dynamic service location from config and secrets.
- Avoid config rollouts that take down a fleet.

## Topics & items to cover
- Hook: a payment service scales from 5 to 50 pods; hardcoded IPs instantly fail.
- Definition: discovery maps a logical name to healthy instances; config management distributes behavior safely.
- Worked example: checkout calls `payments.service.local`; resolver returns 10 healthy endpoints, Envoy retries one failed connection, and a flag routes 5% to v2.
- How it works: registry agents, heartbeats, readiness checks, DNS TTLs, sidecars, xDS/control planes, config versions, rollback.
- Tradeoffs: DNS is simple but TTL-sensitive; client libraries are flexible but language-specific; mesh centralizes policy but adds ops complexity.
- Real-world usage: Kubernetes Services/CoreDNS, Consul, Eureka, Envoy/Istio, feature flags.
- Interview sentence: "Instances register with health metadata; clients resolve logical names; config rolls out versioned with validation and rollback."
- Recap: discovery is where; config is how behavior changes.

## Anecdotes & war stories to use
- Netflix Eureka was built for cloud instances that constantly appeared and disappeared.
- Consul combined service discovery, health checks, and key-value config.
- Kubernetes Services hide pod churn behind stable virtual service names.
- Envoy xDS popularized dynamic config push for proxies and service meshes.

## Things to mention / interview tips
- Distinguish liveness from readiness.
- Include TTLs, stale cache behavior, and retry budgets.
- Validate config schemas before global rollout.
- Keep secrets in a secrets manager, not plain config.

## Common mistakes to call out
- Hardcoding hostnames or IPs in service code.
- Using long DNS TTLs with rapidly changing backends.
- Treating config updates as harmless.
- Forgetting deregistration on shutdown.

## Diagrams / visuals to draw on screen
- Instance registering, client resolving, load balancing.
- Kubernetes Service to pods through readiness gates.
- Config rollout: validate, canary, expand, rollback.

## Series glue
- Follows stateful/stateless scaling because replicas only help if callers find them; next is gossip for decentralized discovery. CTA: subscribe and clone the GitHub repo.
