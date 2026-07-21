# CAP Theorem in 10 Minutes (with Real Examples)

| | |
|---|---|
| **Publish order** | 010 |
| **Course #** | 8 |
| **Module** | M01 — Scalability Foundations |
| **Type** | concept |
| **Target length** | ~12 min |
| **Primary search keyword** | `cap theorem` |
| **Demand** | Very High |

**Thumbnail text idea:** CAP TRADEOFF
**One-line hook (first 15s):** CAP is not 'pick two forever'; it is what your system does during a network partition.

## Learning objectives
- State CAP accurately and apply it during partitions.
- Classify real systems by behavior, not marketing labels.
- Explain why latency and consistency choices are product decisions.

## Topics & items to cover
- Hook: two database replicas cannot talk; a user writes on one side and reads on the other.
- Definition: during a network partition, a distributed system must choose between rejecting/pausing some operations for consistency or accepting divergent operations for availability.
- How it works: inventory has 1 item left in region A and B. If both regions accept checkout during a partition, you may oversell; if one side requires quorum/leader, some users get errors but invariant holds.
- Tradeoffs: CP protects invariants like balances/inventory; AP keeps feeds, likes, and presence responsive; partition tolerance is mandatory once nodes communicate over networks.
- Real-world usage: Dynamo/Cassandra lean availability with reconciliation; ZooKeeper/etcd prioritize consistent coordination; many products mix choices by feature.
- Exact interview sentence: "For this feature, under partition I choose consistency over availability because double-spending is worse than a temporary failure."
- Recap: CAP is a partition-time decision, not a universal database ranking.

## Anecdotes & war stories to use
- Amazon Dynamo was motivated by shopping-cart availability, accepting reconciliation for customer experience.
- ZooKeeper and etcd are used for coordination because stale leadership decisions can be dangerous.
- The 2021 Facebook outage showed how network/control-plane failures can make theoretically healthy services unavailable.

## Things to mention / interview tips
- Always tie CAP to a concrete invariant.
- Say which operations degrade and what the user sees.
- Mention PACELC if asked: else latency versus consistency.
- Avoid saying "CA system" for a partitioned distributed system.

## Common mistakes to call out
- Saying CAP means choose any two in normal operation.
- Treating availability as 100% uptime rather than non-error responses from non-failing nodes.
- Applying one CAP choice to every feature.
- Ignoring reconciliation after AP writes.

## Diagrams / visuals to draw on screen
- Two replicas separated by a partition with conflicting writes.
- CP checkout quorum versus AP likes counter.
- CAP triangle annotated with partition-time behavior.

## Series glue
- Reference WhatsApp offline delivery and prepare for rate limiting, where consistency of counters affects fairness. CTA: subscribe and see examples in the GitHub repo.
