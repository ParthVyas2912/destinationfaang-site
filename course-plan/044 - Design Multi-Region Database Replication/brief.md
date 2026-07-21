# Design Multi-Region Database Replication

| | |
|---|---|
| **Publish order** | 044 |
| **Course #** | 114 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~30 min |
| **Primary search keyword** | `multi region database` |
| **Demand** | High |

**Thumbnail text idea:** GLOBAL DATA
**One-line hook (first 15s):** Multi-region databases force one brutal question: when New York and Singapore disagree for 200 milliseconds, who is allowed to write?

## Learning objectives
- Design active-passive, active-active, and region-partitioned database topologies.
- Explain replication lag, conflict resolution, failover, RPO/RTO, and latency.
- Choose consistency strategy per data type: profile, cart, ledger, inventory.
- Sketch operational runbooks for regional outage and recovery.

## Topics & items to cover
- **Step 1 — Requirements:** global reads/writes, regional failover, low latency, data durability, compliance boundaries. Clarify consistency: user profile vs payments vs inventory differ.
- **Step 2 — Estimation:** cross-region RTT dominates synchronous writes. Read traffic can be local; write traffic may route to home region. Define RPO=acceptable data loss and RTO=failover time.
- **Step 3 — API/Data model:** `User(home_region)`, `Order(region, id)`, `LedgerEntry` single-writer, conflict metadata `version/vector_clock/updated_at`. APIs route writes by entity home.
- **Step 4 — HLD:** global DNS/traffic manager → regional app stacks → local DB replicas → async replication bus; control plane for failover; observability comparing lag.
- **Step 5 — Deep dives:** 1) Write ownership: single-writer per user/tenant avoids conflicts. 2) Active-active conflicts: LWW only for low-value fields; use CRDT/merge or user resolution for collaborative data. 3) Failover: freeze writes or promote region, replay logs, handle split brain.
- **Step 6 — Wrap-up:** there is no free lunch: latency, availability, consistency—pick per workflow.

## Anecdotes & war stories to use
- Google Spanner/TrueTime is the canonical example of globally distributed transactions with clock uncertainty made explicit.
- Amazon Dynamo emphasized always-writable systems with conflict resolution and hinted handoff for shopping-cart-like workloads.
- Many SaaS systems use regional primaries or failover rather than active-active for all writes, because conflict rules are business-specific.
- CockroachDB/Yugabyte popularize geo-partitioning and consensus replication tradeoffs for SQL systems.

## Things to mention / interview tips
- Define RPO and RTO early; it shows operational maturity.
- Use “home region” or “single writer per entity” as a practical default.
- Mention data residency: EU user data may need EU storage/processing.
- Include replication-lag metrics and failover drills.

## Common mistakes to call out
- Saying “active-active” without conflict rules.
- Assuming synchronous global writes are low-latency.
- Failing over automatically during a network partition and creating split brain.
- Treating all data with the same consistency requirement.

## Diagrams / visuals to draw on screen
- Active-passive vs active-active topology side by side.
- Home-region routing for user-owned data.
- Failover timeline with RPO/RTO and replication lag.

## Series glue
- Reference Replication/Partitioning, CAP, and Raft; forward to RDBMS Internals for local guarantees. CTA: subscribe and get topology diagrams on GitHub.
