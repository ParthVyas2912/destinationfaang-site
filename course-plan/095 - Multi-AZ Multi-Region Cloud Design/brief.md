# Multi-AZ & Multi-Region Cloud Design

| | |
|---|---|
| **Publish order** | 095 |
| **Course #** | 74 |
| **Module** | M07 — Cloud & Infrastructure |
| **Type** | concept |
| **Target length** | ~16 min |
| **Primary search keyword** | `multi region architecture` |
| **Demand** | High |

**Thumbnail text idea:** SURVIVE REGION DOWN
**One-line hook (first 15s):** Multi-AZ is a reliability default; multi-region is a product and consistency decision you must defend.

## Learning objectives
- Compare AZ redundancy, active-passive regions, and active-active regions.
- Use RTO/RPO to pick replication and failover strategies.
- Design traffic routing, database promotion, and stateful recovery.
- Explain split brain, stale reads, DNS failover, and data residency pitfalls.

## Topics & items to cover
- Hook: “deploy in two regions” is incomplete until writes and failover are defined.
- Definition: multi-AZ tolerates datacenter failure; multi-region tolerates regional outages/control-plane problems.
- Worked example: e-commerce API with 5k reads/sec and 500 writes/sec; app in 3 AZs, primary DB with synchronous AZ replication, async replica in second region, 5-minute RPO and 30-minute RTO.
- How it works: global DNS/anycast -> regional LB -> multi-AZ service -> DB; promote secondary only after fencing primary writes.
- Tradeoffs: active-passive is simpler/cheaper but has lag; active-active lowers latency but needs conflict rules, global IDs, cache invalidation.
- Real-world usage: banking pays for low RPO; social feeds may accept regional degradation and async repair.
- Interview sentence: “I start with RTO/RPO, then choose active-passive unless the product truly needs active-active writes.”
- Recap: recovery goals drive region strategy.

## Anecdotes & war stories to use
- AWS Well-Architected frames multi-region as cost/complexity, not a default.
- Google Spanner shows global consistency is possible but requires consensus, clocks, and latency-aware design.
- Outage postmortems often show DNS TTLs and cached clients delaying failover.
- Inventory/payment systems avoid casual active-active writes because conflicts become money loss.

## Things to mention / interview tips
- Define RTO and RPO before boxes.
- Prevent split brain with leader election, fencing tokens, or single-writer routing.
- Test failover with game days.
- Separate stateless app recovery from stateful DB promotion.

## Common mistakes to call out
- Treating async replicas as zero-data-loss backups.
- Forgetting queues, jobs, secrets, and feature flags.
- Depending only on high-TTL DNS.
- Designing active-active without conflict semantics.

## Diagrams / visuals to draw on screen
- Multi-AZ regional stack.
- Active-passive failover path.
- RTO/RPO recovery timeline.
- Split-brain two-primary diagram.

## Series glue
- Connect to database replication and caching modules. Next: service mesh for regional traffic policy. CTA: subscribe and use the GitHub RTO/RPO checklist.
