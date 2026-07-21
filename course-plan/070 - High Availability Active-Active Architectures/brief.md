# High Availability: Active-Active Architectures

| | |
|---|---|
| **Publish order** | 070 |
| **Course #** | 53 |
| **Module** | M05 — Microservices & Reliability |
| **Type** | concept |
| **Target length** | ~16 min |
| **Primary search keyword** | `active active architecture` |
| **Demand** | High |

**Thumbnail text idea:** ALWAYS ON
**One-line hook (first 15s):** Active-active sounds like ‘just run in two regions’—until the same user updates the same record in both places.

## Learning objectives
- Explain active-active across regions or data centers.
- Design routing, replication, conflict handling, and failover.
- Choose strong versus eventual consistency per data domain.

## Topics & items to cover
- Hook: active-active improves availability only if data, routing, and operations are designed for it.
- Definition: active-active means multiple regions serve live traffic simultaneously, not one idle standby.
- Worked example: global app routes users to nearest healthy region via DNS/Anycast/GSLB. Stateless services run everywhere. Read-mostly data replicates globally. User-owned records use `home_region` for strong writes; feeds use async replication; collaborative/global data needs consensus or explicit conflict resolution. Failover moves traffic with defined RTO/RPO.
- Tradeoffs: low latency and regional fault tolerance; high cost, conflict handling, data residency, complex testing. Strong multi-region consistency adds latency; eventual consistency needs product semantics.
- Real usage: CDNs, Dynamo-style eventually consistent stores, Spanner-like globally consistent databases.
- Interview sentence: “I’ll keep stateless serving active-active, but choose data strategy per domain: home-region ownership for strong writes, async replication for feeds, and explicit conflict resolution for multi-writer data.”
- Recap: active-active is a data consistency design, not just deployment.

## Anecdotes & war stories to use
- Amazon Dynamo framed availability and eventual consistency under partitions.
- Google Spanner demonstrated globally distributed strong consistency with TrueTime assumptions.
- The 2016 Dyn DNS DDoS reminded teams that traffic-management dependencies affect availability.

## Things to mention / interview tips
- Ask RTO/RPO and data residency.
- Separate stateless from stateful active-active.
- Name conflict strategy: last-write-wins, version vectors, CRDT, or home region.

## Common mistakes to call out
- Assuming async replication means zero data loss.
- Making every table multi-writer without conflict semantics.
- Forgetting DNS/client cache behavior during failover.

## Diagrams / visuals to draw on screen
- Two-region active-active routing.
- Home-region writes with cross-region replication.
- Simultaneous update conflict timeline.

## Series glue
- Caps the reliability arc after backpressure/retries. Next videos can explore consensus and disaster recovery. Subscribe and use GitHub practice diagrams.
