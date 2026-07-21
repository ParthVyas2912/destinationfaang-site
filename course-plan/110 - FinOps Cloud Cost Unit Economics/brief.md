# FinOps: Cloud Cost & Unit Economics

| | |
|---|---|
| **Publish order** | 110 |
| **Course #** | 69 |
| **Module** | M06 — Security, Observability & FinOps |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `finops cloud cost` |
| **Demand** | Moderate |

**Thumbnail text idea:** COST PER REQUEST
**One-line hook (first 15s):** A senior system design answer does not just scale; it knows what one user action costs and which knob changes that cost.

## Learning objectives
- Explain FinOps and unit economics for cloud systems.
- Break costs into compute, storage, network, databases, observability, and third-party APIs.
- Design tagging, allocation, budgets, and anomaly detection.
- Optimize without sacrificing reliability or product value.

## Topics & items to cover
- Hook: “autoscale everything” can hide a margin problem until the bill arrives.
- Definition: FinOps is the operating practice of making cloud cost visible, accountable, and optimizable through engineering/business collaboration.
- Worked example: video service serves 10M play starts/day; calculate cost per play from CDN egress, origin storage, transcoding jobs, metadata DB reads, observability ingest, and recommendation calls; optimize by cache hit rate and encoding ladder.
- How it works: tag resources by service/team/env -> ingest billing data -> allocate shared costs -> dashboard unit metrics -> detect anomalies -> choose levers like rightsizing, reserved capacity, spot, lifecycle policies.
- Tradeoffs: reserved capacity saves money but reduces flexibility; aggressive downsampling cuts observability; cheap storage tiers add restore latency; spot capacity needs interruption handling.
- Real-world usage: SaaS gross margin, ML inference cost, logs retention, CDN-heavy media, data warehouse spend.
- Interview sentence: “I would track cost per business unit, such as per order or per streamed minute, then optimize the largest driver with SLO guardrails.”
- Recap: cost is an architecture dimension.

## Anecdotes & war stories to use
- The FinOps Foundation formalized cloud cost management as a cross-functional practice, not only procurement.
- Netflix publicly discusses cloud efficiency and CDN choices because streaming unit cost directly affects margins.
- Data warehouse bill surprises often come from unbounded queries and duplicated pipelines.
- Observability platforms can become major spend when logs and high-cardinality metrics are ingested without retention strategy.

## Things to mention / interview tips
- Use unit metrics: cost/order, cost/search, cost/GB processed, cost/1k requests.
- Tag everything and allocate shared platform costs transparently.
- Optimize after measuring top drivers, not by random micro-savings.
- Keep SLO/error-budget guardrails during cost reduction.

## Common mistakes to call out
- Treating cloud bill as finance-only.
- Optimizing idle dev resources while ignoring egress or database hot spots.
- Using spot for workloads that cannot tolerate interruption.
- Cutting logs/replicas blindly and increasing incident cost.

## Diagrams / visuals to draw on screen
- Cost stack by request path.
- Unit economics formula for cost per play/order.
- Rightsizing versus reserved/spot decision tree.
- Cost anomaly dashboard with owner tags.

## Series glue
- Tie to logging and telemetry cost decisions. Next module moves into AI/data systems, where cost per query becomes even more visible. CTA: subscribe and use the GitHub cost-model spreadsheet.
