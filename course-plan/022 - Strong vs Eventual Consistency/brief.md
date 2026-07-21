# Strong vs Eventual Consistency (with Examples)

| | |
|---|---|
| **Publish order** | 022 |
| **Course #** | 6 |
| **Module** | M01 — Scalability Foundations |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `eventual consistency` |
| **Demand** | High |

**Thumbnail text idea:** CONSISTENCY CHOICE
**One-line hook (first 15s):** Strong versus eventual consistency is not theory; it decides whether a user sees money, likes, or inventory correctly.

## Learning objectives
- Define strong and eventual consistency with user-facing examples.
- Choose consistency per operation and invariant.
- Explain read-your-writes, monotonic reads, quorum, and reconciliation.

## Topics & items to cover
- Hook: you upload a profile photo, refresh, and the old photo appears; is that acceptable or a bug?
- Definition: strong consistency makes reads reflect the latest committed write according to a single order; eventual consistency allows temporary divergence that converges if writes stop.
- How it works: with 3 replicas and quorum `W=2, R=2`, a read overlaps a write quorum and usually sees latest data; with async replication, region B may lag 500 ms or several seconds but later catches up.
- Tradeoffs: strong consistency costs latency/availability across regions; eventual consistency improves speed and resilience but needs conflict resolution and user messaging.
- Real-world usage: banking ledgers and inventory reservations need strong invariants; likes, views, feeds, search indexes, and presence often tolerate eventual consistency.
- Exact interview sentence: "I would make the order/payment state strongly consistent, but the feed/search projection can be eventually consistent and rebuilt from events."
- Recap: consistency is a feature-level decision, not a database checkbox.

## Anecdotes & war stories to use
- Amazon Dynamo embraced eventual consistency for availability, using reconciliation for divergent versions.
- DNS is a familiar eventually consistent system because records propagate through caches over time.
- Social networks commonly show eventually consistent likes/view counts to keep interactions fast.

## Things to mention / interview tips
- Name the invariant that requires strong consistency.
- Mention read-your-writes for user experience even in eventually consistent systems.
- Discuss conflict resolution: last-write-wins, vector clocks, merge rules.
- Tie consistency to latency and region topology.

## Common mistakes to call out
- Saying eventual consistency means data loss.
- Making every operation strongly consistent by default.
- Ignoring user-visible anomalies after writes.
- Forgetting derived indexes lag source-of-truth data.

## Diagrams / visuals to draw on screen
- Three-replica quorum read/write overlap.
- Async primary-to-replica lag timeline.
- Source-of-truth DB feeding eventually consistent search/feed projection.

## Series glue
- Reference e-commerce checkout choices; point forward to web crawler freshness and dedupe tradeoffs. CTA: subscribe and check the GitHub examples.
