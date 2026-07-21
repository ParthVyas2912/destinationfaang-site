# Design a Feature Flag System (LaunchDarkly-Style)

| | |
|---|---|
| **Publish order** | 058 |
| **Course #** | 113 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~22 min |
| **Primary search keyword** | `design feature flags` |
| **Demand** | Moderate |

**Thumbnail text idea:** SAFE LAUNCHES
**One-line hook (first 15s):** Feature flags are not just booleans—they’re a distributed decision system on every request path.

## Learning objectives
- Design a LaunchDarkly-style flag evaluation and distribution system.
- Model flags, environments, targeting rules, segments, SDKs, and audit history.
- Handle low-latency reads, consistency, privacy, and stale fallbacks.

## Topics & items to cover
- Requirements: create/update flags, target users and segments, percentage rollouts, SDK evaluation under 5ms locally, propagation in seconds, audit and approvals.
- Estimation: 100K customers, millions of SDK instances, billions of local evaluations/day. Shard control-plane data by `project_id`; stream deltas by environment.
- API/Data model: `POST /flags`, `PATCH /flags/{key}`, `GET /sdk/eval`, `GET /sdk/stream`; entities: Project, Environment, Flag, Rule, Segment, Variation, AuditLog.
- High-level design: admin UI/API → config DB → changelog → SSE/streaming fanout → SDK local cache; optional relay proxy in customer VPC; analytics events separate.
- Deep dives/bottlenecks: deterministic rollout with hash(`flag_key,user_key`) buckets; offline SDK bootstrap/TTL fallback; large segments via precomputed membership or compact sync.
- Wrap-up: flag serving is read-heavy edge config plus strict auditability.

## Anecdotes & war stories to use
- Flickr and Etsy popularized continuous deployment with feature toggles.
- LaunchDarkly became a product because homegrown toggles become operational risk.
- Outage postmortems often mention kill switches, or the lack of them.

## Things to mention / interview tips
- Never put a network call on every hot-path flag check.
- Say “deterministic hashing” for stable percentage rollout.
- Separate control plane from data plane.

## Common mistakes to call out
- Randomizing rollout on every request.
- Letting flags live forever with no cleanup.
- Leaking server-side targeting rules to clients.

## Diagrams / visuals to draw on screen
- Control plane streaming to SDK caches.
- Rule evaluation tree.
- Percentage rollout buckets.

## Series glue
- Uses caching/consistency concepts. Next: secondary indexes and precomputation. Subscribe and use the GitHub repo.
