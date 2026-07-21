# Every System Design Tradeoff You Must Know

| | |
|---|---|
| **Publish order** | 082 |
| **Course #** | 9 |
| **Module** | M01 — Scalability Foundations |
| **Type** | concept |
| **Target length** | ~12 min |
| **Primary search keyword** | `system design tradeoffs` |
| **Demand** | High |

**Thumbnail text idea:** TRADEOFF MAP
**One-line hook (first 15s):** System design interviews are not about perfect architectures — they are about naming the tradeoff you just chose.

## Learning objectives
- Recognize recurring tradeoff families in system design.
- Explain tradeoffs with workload-specific examples.
- Use constraints to justify choices under ambiguity.
- Build a decision vocabulary interviewers trust.

## Topics & items to cover
- Hook: every box buys one property by selling another.
- Definition: a system design tradeoff intentionally exchanges qualities such as latency, consistency, cost, availability, simplicity, and operability.
- Worked example: news feed fanout-on-write gives fast reads but expensive celebrity writes; fanout-on-read makes writes cheap but reads slower.
- How it works: consistency vs availability, latency vs durability, normalization vs read speed, sync vs async, monolith vs microservices, cache freshness vs load.
- Tradeoffs: no universal winners; answer depends on read/write ratio, failure model, team size, compliance, and growth path.
- Real-world usage: Dynamo availability, Spanner strong consistency, CDN caching, Kafka async pipelines, denormalized read models.
- Interview sentence: "Given the read-heavy workload, I’m choosing denormalized cached reads and accepting controlled staleness with invalidation."
- Recap: articulate, constrain, choose, revisit.

## Anecdotes & war stories to use
- Amazon Dynamo prioritized availability and partition tolerance for shopping-cart-like workloads.
- Google Spanner accepted infrastructure complexity for externally consistent transactions.
- Twitter timeline architecture is a classic hybrid fanout example for celebrities.
- Netflix embraced microservices and resilience tooling during its cloud transition.

## Things to mention / interview tips
- Attach each tradeoff to a requirement: "because reads dominate..."
- Offer a fallback if assumptions change.
- Use concrete numbers: QPS, fanout, storage, latency target.
- Say what you are deliberately not optimizing.

## Common mistakes to call out
- Reciting CAP theorem for every design.
- Choosing microservices before team or scale pressure.
- Adding Kafka/cache/search without explaining why.
- Pretending a design has no downside.

## Diagrams / visuals to draw on screen
- Tradeoff matrix: choice, benefit, cost, when to use.
- Feed fanout-on-write vs fanout-on-read flow.
- Triangle of latency, consistency, cost.

## Series glue
- Summarizes lessons from foundations through reliability; next deepens conflict resolution with vector clocks. CTA: subscribe and clone the GitHub matrix.
