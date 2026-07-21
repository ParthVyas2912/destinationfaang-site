# Canary, Blue-Green & Shadow Deployments

| | |
|---|---|
| **Publish order** | 097 |
| **Course #** | 77 |
| **Module** | M07 — Cloud & Infrastructure |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `blue green canary deployment` |
| **Demand** | High |

**Thumbnail text idea:** SHIP WITHOUT PANIC
**One-line hook (first 15s):** Deployment strategy is blast-radius management: who sees the new code, when, and how fast can you undo it?

## Learning objectives
- Compare rolling, blue-green, canary, and shadow deployments.
- Design gates with metrics, logs, traces, and business KPIs.
- Explain safe rollback for code, database migrations, and flags.
- Pick patterns for APIs, ML models, and checkout flows.

## Topics & items to cover
- Hook: the safest deploy has the smallest irreversible blast radius.
- Definition: blue-green swaps full environments, canary gradually shifts real traffic, shadow duplicates traffic to a non-impacting version.
- Worked example: checkout v2 starts at 1% for 15 minutes; promote to 5%, 25%, 50%, 100% only if p95 <300ms, error rate stays near baseline, and auth success does not regress.
- How it works: LB/mesh/feature flag routes cohorts; telemetry compares candidate to baseline; rollback flips routing; DB uses expand-contract migrations.
- Tradeoffs: blue-green gives fast rollback but doubles capacity; canary needs good metrics; shadow finds performance bugs but not user-visible correctness.
- Real-world usage: API releases, model scoring, mobile backends, payment/booking systems.
- Interview sentence: “I decouple deployment from release with feature flags, then use canary gates on technical and business metrics.”
- Recap: progressive delivery is controlled exposure plus evidence.

## Anecdotes & war stories to use
- Netflix popularized production experimentation/resilience because streaming regressions are user-visible.
- LaunchDarkly-style flags made release control mainstream, but stale flags become debt.
- Google SRE error budgets give a concrete stop condition for risky rollouts.
- Many incidents roll back code but not schema; expand-contract avoids that trap.

## Things to mention / interview tips
- Define rollback triggers before deployment.
- Use sticky cohorts so users do not bounce versions.
- Use dark launch/shadow traffic for read-only validation.
- Separate deploy, release, and migration vocabulary.

## Common mistakes to call out
- Canarying without enough traffic to detect regressions.
- Watching average latency instead of p95/p99 and error-budget burn.
- Ignoring schema compatibility.
- Shadowing writes into real downstream systems.

## Diagrams / visuals to draw on screen
- Blue/green environments behind one load balancer.
- Canary ramp ladder with gates.
- Shadow traffic tee to v2.
- Expand-contract migration timeline.

## Series glue
- Tie back to service mesh and dashboards. Next: Terraform for reproducible environments. CTA: subscribe and grab the rollout checklist from GitHub.
