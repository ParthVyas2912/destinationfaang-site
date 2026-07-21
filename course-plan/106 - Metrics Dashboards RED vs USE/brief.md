# Metrics & Dashboards: RED vs USE

| | |
|---|---|
| **Publish order** | 106 |
| **Course #** | 66 |
| **Module** | M06 — Security, Observability & FinOps |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `red use metrics` |
| **Demand** | Moderate |

**Thumbnail text idea:** MEASURE WHAT MATTERS
**One-line hook (first 15s):** A dashboard is useful only if it tells you whether users are hurting and where the system is saturated.

## Learning objectives
- Explain RED: rate, errors, duration for request-driven services.
- Explain USE: utilization, saturation, errors for resources.
- Build dashboards that connect SLIs, SLOs, and alerts.
- Avoid vanity metrics and high-cardinality explosions.

## Topics & items to cover
- Hook: CPU at 40% does not matter if checkout p99 is timing out.
- Definition: RED measures service behavior; USE measures resource health.
- Worked example: checkout API at 2k RPS; dashboard shows request rate, 5xx/4xx split, p50/p95/p99 latency, DB connection saturation, queue depth, CPU, memory, and error-budget burn.
- How it works: instrument app counters/histograms -> scrape/push metrics -> aggregate by low-cardinality labels -> alert on SLO symptoms -> use USE panels for diagnosis.
- Tradeoffs: more labels improve slicing but can melt metric stores; averages are cheap but hide tail pain; too many alerts create fatigue.
- Real-world usage: API gateways, databases, Kafka consumers, Kubernetes nodes, canary gates, incident review.
- Interview sentence: “I would alert on user-facing SLO symptoms with RED, then diagnose resource bottlenecks with USE.”
- Recap: RED answers “is the service healthy?” and USE answers “what resource is constrained?”

## Anecdotes & war stories to use
- Google SRE popularized SLIs/SLOs and error budgets as operational decision tools.
- Brendan Gregg’s USE method gives a systematic way to investigate resource bottlenecks.
- Prometheus made dimensional metrics common, along with the operational pain of high-cardinality labels.
- Many incidents are missed by average latency dashboards because only p95/p99 shows user pain.

## Things to mention / interview tips
- Use histograms/percentiles for latency, not only averages.
- Label carefully: route/status/region are useful; user_id is dangerous.
- Alert on symptoms, page on impact, ticket on capacity trends.
- Tie canary promotion to RED metrics and business KPIs.

## Common mistakes to call out
- Building CPU-only dashboards for user-facing services.
- Alerting on every warning metric.
- Using unbounded labels like request ID.
- Mixing 4xx user errors with 5xx service failures without context.

## Diagrams / visuals to draw on screen
- RED dashboard layout for checkout.
- USE dashboard for one node or database.
- SLO/error-budget burn chart.
- Metric label cardinality example.

## Series glue
- Reference rollout and patching videos: metrics are the safety gate. Next: distributed tracing when metrics say “bad” but not “where.” CTA: subscribe and use GitHub dashboard templates.
