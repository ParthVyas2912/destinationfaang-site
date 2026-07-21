# Final Project: Design Your Own System (Capstone)

| | |
|---|---|
| **Publish order** | 133 |
| **Course #** | MOCK6 |
| **Module** | M10 — Mock Interview & Practice |
| **Type** | mock |
| **Target length** | ~90 min |
| **Primary search keyword** | `system design project` |
| **Demand** | Moderate |

**Thumbnail text idea:** FINAL CAPSTONE
**One-line hook (first 15s):** The capstone is where you prove you can choose a system, set scope, defend tradeoffs, and explain how it would survive production.
## Learning objectives
- Complete a self-directed system design project from prompt to final architecture.
- Apply the full course rubric across requirements, scale, APIs, data, design, and bottlenecks.
- Pick a project scope that is challenging but interview-sized.
- Present a production-ready design with tradeoffs and metrics.

## Topics & items to cover
- Full interview arc: 0-10 min choose system and define scope; 10-20 estimate scale; 20-35 APIs/data model; 35-60 architecture; 60-80 deep dives; 80-90 final review.
- Rubric: 20% requirements and non-goals, 15% estimates tied to decisions, 20% APIs/data/shard keys, 25% architecture and bottlenecks, 10% reliability/security/observability, 10% communication.
- Example project 1: “Design a campus food delivery platform” with restaurants, couriers, order tracking, payment, surge traffic.
- Example project 2: “Design an enterprise RAG assistant” with connectors, ACLs, vector search, evals, guardrails.
- Example project 3: “Design a live sports notification system” with subscriptions, event ingestion, fanout, dedupe, push latency.
- Scoring callouts: every diagram box needs a reason; every bottleneck needs a mitigation; every metric needs an owner.
- Final deliverable: one architecture diagram, one API/schema page, one estimate page, one tradeoff page, one risk/monitoring page.

## Anecdotes & war stories to use
- Real design docs are judged on alternatives and risks, not diagram beauty.
- Strong interview loops reward candidates who can narrow ambiguity into a testable scope.
- Many production failures come from omitted operational plans: backfills, retries, alerts, and rollback.
- Capstone projects mirror staff-engineer communication: define the problem, align stakeholders, and defend choices.

## Things to mention / interview tips
- Start with non-goals so the project does not sprawl.
- Pick one or two deep dives that are genuinely hard for your system.
- Use the phrase “the bottleneck I expect first is…” and then test it.
- Close with launch plan: MVP, metrics, and future improvements.

## Common mistakes to call out
- Choosing a project so broad it cannot be completed in 90 minutes.
- Drawing a generic microservices map with no data flow.
- Skipping estimates because it is “just a project.”
- Ignoring security, privacy, or abuse for user-facing systems.

## Diagrams / visuals to draw on screen
- Capstone grading rubric table.
- Template architecture canvas.
- Three example system prompt cards.
- Final series map from fundamentals to cases to mocks.

## Series glue
- Wrap up the whole course: revisit fundamentals, case studies, AI systems, and M10 mocks. CTA: subscribe, star the GitHub repo, share your capstone design, and keep practicing aloud.
