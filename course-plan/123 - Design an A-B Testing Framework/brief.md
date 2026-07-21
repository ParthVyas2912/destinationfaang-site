# Design an A/B Testing Framework

| | |
|---|---|
| **Publish order** | 123 |
| **Course #** | 123 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~28 min |
| **Primary search keyword** | `design ab testing` |
| **Demand** | High |

**Thumbnail text idea:** TEST SAFELY
**One-line hook (first 15s):** An A/B platform is not just random assignment — it is the system that prevents teams from fooling themselves with bad experiments.
## Learning objectives
- Design experiment assignment, exposure logging, metrics, and analysis.
- Explain sticky bucketing, guardrails, and sample ratio mismatch.
- Choose sharding keys and data models for high-volume exposure events.
- Discuss rollout, targeting, and statistical validity.

## Topics & items to cover
- **Requirements:** create experiments, assign users consistently, support targeting, log exposures/conversions, compute metrics, ramp safely.
- **Estimation:** 100M users, billions of exposure events/day; assignment must be low-latency and highly available; analytics can be delayed.
- **API/Data model:** `GET /v1/assignments?user_id&experiment_key`; `POST /v1/exposures`; `Experiment`, `Variant`, `AudienceRule`, `Assignment`, `Exposure`, `Metric`; shard assignment/exposure by `user_id` or hash bucket, partition events by date.
- **High-level design:** config service → assignment SDK/service → exposure stream → warehouse → metric computation → dashboard/alerts; separate control plane from data plane.
- **Deep dives/bottlenecks:** sticky randomization via hash(`experiment_id`,`unit_id`) into buckets; sample-ratio-mismatch detection; metric guardrails for latency/errors/revenue; mutually exclusive layers prevent overlapping tests.
- **Wrap-up:** emphasize trust: reproducibility, audit logs, and experiment governance.

## Anecdotes & war stories to use
- Booking.com is well known for a culture of large-scale online experimentation.
- Microsoft experimentation papers discuss pitfalls like sample ratio mismatch and trustworthy analysis.
- Google and LinkedIn have published on controlled experiments and the need for guardrail metrics.
- Feature-flag systems often evolve into experimentation platforms but need stronger data rigor.

## Things to mention / interview tips
- Say “assignment unit” clearly: user, device, session, account, or request.
- Log exposure only when the user could actually see the variant.
- Include ramping: 1%, 5%, 25%, 50%, 100% with guardrail checks.
- Mention offline recomputation for auditability.

## Common mistakes to call out
- Randomizing on every request, causing variant flicker.
- Counting conversions without exposure logs.
- Ignoring overlapping experiments.
- Declaring wins without checking guardrails or SRM.

## Diagrams / visuals to draw on screen
- Control plane vs assignment data plane.
- Hash bucket allocation across experiments.
- Exposure/conversion event timeline.

## Series glue
- References personalization and data quality; next ML pipeline case uses similar control-plane/data-plane thinking. CTA: subscribe and grab the A/B checklist from GitHub.
