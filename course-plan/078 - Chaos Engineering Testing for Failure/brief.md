# Chaos Engineering: Testing for Failure

| | |
|---|---|
| **Publish order** | 078 |
| **Course #** | 57 |
| **Module** | M05 — Microservices & Reliability |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `chaos engineering` |
| **Demand** | High |

**Thumbnail text idea:** BREAK IT SAFELY
**One-line hook (first 15s):** Chaos engineering is not randomly deleting servers — it is running a controlled experiment with a rollback plan.

## Learning objectives
- Define a chaos experiment with hypothesis, blast radius, and abort conditions.
- Choose failures for services, databases, networks, and regions.
- Connect chaos testing to SLOs and incident readiness.
- Explain why game days and automation both matter.

## Topics & items to cover
- Hook: if losing a cache node is survivable, prove it Tuesday afternoon before it happens Friday night.
- Definition: chaos engineering deliberately injects failure to validate resilience assumptions.
- Worked example: hypothesis: checkout survives one payment-provider timeout with p95 under target. Inject 500ms latency and 5% errors for 10 minutes to one AZ, watch burn rate, abort if error rate doubles.
- How it works: steady-state metrics, small blast radius, fault proxy, kill instance, network delay, dependency blackhole, runbook validation, rollback.
- Tradeoffs: finds weaknesses but can create pain; staging misses production complexity; production needs guardrails.
- Real-world usage: Netflix Chaos Monkey/Simian Army, AWS Fault Injection Service, Gremlin-style tooling, Kubernetes disruption tests.
- Interview sentence: "I’d start with narrow, observable chaos experiments tied to SLOs and expand blast radius only after runbooks pass."
- Recap: controlled failure creates confidence.

## Anecdotes & war stories to use
- Netflix developed Chaos Monkey after moving to AWS to ensure instances could disappear safely.
- The Simian Army idea pushed teams to design for failure before incidents.
- Google SRE practices connect reliability work to error budgets and controlled risk.
- AWS Fault Injection Service shows chaos testing became a managed cloud practice.

## Things to mention / interview tips
- Say "steady state," "hypothesis," "blast radius," and "abort condition."
- Test DNS, cache, queue, payment gateway, regional failover.
- Include people: on-call notification and runbook execution.
- Start low-traffic before critical write paths.

## Common mistakes to call out
- Running chaos without dashboards or rollback.
- Treating staging success as proof production is resilient.
- Injecting too many failures at once.
- Blaming teams instead of fixing system weaknesses.

## Diagrams / visuals to draw on screen
- Experiment card: hypothesis, fault, scope, metrics, abort.
- Request flow with injected dependency latency.
- SLO burn-rate chart during a game day.

## Series glue
- Builds on quotas and isolation; next explains what to do when failure becomes a real incident. CTA: subscribe and use the GitHub chaos checklist.
