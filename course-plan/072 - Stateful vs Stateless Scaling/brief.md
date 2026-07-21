# Stateful vs Stateless Scaling

| | |
|---|---|
| **Publish order** | 072 |
| **Course #** | 56 |
| **Module** | M05 — Microservices & Reliability |
| **Type** | concept |
| **Target length** | ~12 min |
| **Primary search keyword** | `stateful vs stateless` |
| **Demand** | Moderate |

**Thumbnail text idea:** STATE MATTERS
**One-line hook (first 15s):** The fastest way to scale is to remove memory from your servers — but not every workload lets you do that.

## Learning objectives
- Distinguish stateless request handling from stateful ownership of sessions, shards, or streams.
- Choose scaling patterns for APIs, chat servers, and databases.
- Explain why sticky sessions solve one problem while creating failover pain.
- Design migration from local state to externalized state.

## Topics & items to cover
- Hook: ten web servers behind a load balancer work only if none owns unique user state.
- Definition: stateless services can process any request anywhere; stateful services must preserve or locate mutable state.
- Worked example: 10,000 logged-in users with JWT and Redis cart storage can hit any API pod; WebSocket rooms may be pinned to connection gateways.
- How it works: load balancing, external session stores, shard maps, consistent hashing, handoff, graceful draining.
- Tradeoffs: stateless is elastic and easy to roll; stateful reduces hops but requires replication, rebalancing, and failover.
- Real-world usage: stateless web frontends; stateful Kafka brokers, Redis primaries, game servers, databases.
- Interview sentence: "I’ll keep compute stateless where possible and make state explicit in Redis, a database, or partition ownership."
- Recap: stateless scales replicas; stateful scales ownership.

## Anecdotes & war stories to use
- Twelve-Factor App popularized stateless processes for cloud deployment.
- Kubernetes made Deployments easy, then added StatefulSets for stable identity and volumes.
- Sticky sessions in classic web apps caused painful deploys when a busy node disappeared.
- Large chat systems often split stateless APIs from stateful connection fanout gateways.

## Things to mention / interview tips
- Ask "what state exists and who owns it?" before drawing boxes.
- Name concrete state: auth session, cart, stream offset, room membership.
- Propose drain and rebalance protocols for stateful nodes.
- Externalize state only when latency and cost are acceptable.

## Common mistakes to call out
- Saying "just add servers" for databases or WebSocket tiers.
- Hiding state in local caches without invalidation.
- Assuming sticky sessions are high availability.
- Ignoring warm-up time after moving state.

## Diagrams / visuals to draw on screen
- Load balancer to stateless API pods with shared Redis/Postgres.
- Shard ownership map for users A-M and N-Z.
- Node drain sequence moving connections or partitions.

## Series glue
- Builds on load balancing and caching foundations; next video shows discovery and config so services can find changing replicas. CTA: subscribe and use the repo checklist.
