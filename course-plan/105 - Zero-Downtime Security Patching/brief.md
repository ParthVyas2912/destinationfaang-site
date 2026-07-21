# Zero-Downtime Security Patching

| | |
|---|---|
| **Publish order** | 105 |
| **Course #** | 62 |
| **Module** | M06 — Security, Observability & FinOps |
| **Type** | concept |
| **Target length** | ~10 min |
| **Primary search keyword** | `zero downtime patching` |
| **Demand** | Moderate |

**Thumbnail text idea:** PATCH WITHOUT OUTAGE
**One-line hook (first 15s):** The hard part of security patching is not applying the fix; it is draining, rolling, verifying, and rolling back without opening a bigger incident.

## Learning objectives
- Design rolling patches for stateless and stateful services.
- Use draining, health checks, surge capacity, and compatibility windows.
- Patch dependencies, base images, kernels, and managed services safely.
- Balance exploit urgency against availability risk.

## Topics & items to cover
- Hook: a critical CVE with an unsafe rollout can become both a security incident and an outage.
- Definition: zero-downtime patching updates vulnerable components while maintaining service availability through redundancy and controlled traffic movement.
- Worked example: 40 API pods across 3 AZs; set maxUnavailable=0 and maxSurge=25%, drain one node at a time, require readiness before routing, watch p95/error budget, then continue by AZ.
- How it works: inventory vulnerable assets -> build patched artifact -> canary -> rolling update/drain -> verify security and SLOs -> revoke old images/keys -> document closure.
- Tradeoffs: slower rollouts reduce risk but prolong exposure; fast patching reduces exploit window but needs strong rollback; stateful services need leader/follower and schema compatibility plans.
- Real-world usage: OpenSSL/JVM/base-image CVEs, Kubernetes node upgrades, database minor versions, WAF/rule updates.
- Interview sentence: “I would use redundancy, readiness gates, canaries, and staged drains, while tracking both exploit exposure and SLO burn.”
- Recap: patching is a reliability workflow with security urgency.

## Anecdotes & war stories to use
- Heartbleed showed that patching code is not enough; certificates and keys may also need rotation.
- Log4Shell forced many organizations to inventory transitive dependencies quickly, highlighting SBOM value.
- Kubernetes node upgrades rely on cordon/drain plus PodDisruptionBudgets to preserve availability.
- Browser and OS vendors use staged rollouts because patches themselves can introduce regressions.

## Things to mention / interview tips
- Maintain asset inventory and dependency visibility before the emergency.
- Pair patch rollout with key/cert rotation when compromise is possible.
- Respect PDBs and quorum for stateful systems.
- Define “patched” as verified running version, not merged PR.

## Common mistakes to call out
- Patching images but leaving old pods/nodes running.
- Ignoring transitive dependencies and sidecars.
- Draining too many quorum members at once.
- Having no rollback for the patched artifact.

## Diagrams / visuals to draw on screen
- Rolling update across pods/AZs.
- Node cordon/drain/replace sequence.
- CVE workflow from detection to verification.
- Exposure window timeline.

## Series glue
- Tie back to STRIDE mitigations and secrets rotation. Next: metrics dashboards provide the evidence that rollout health is safe. CTA: subscribe and grab the patch runbook from GitHub.
