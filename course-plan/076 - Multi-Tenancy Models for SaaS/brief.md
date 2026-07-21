# Multi-Tenancy Models for SaaS

| | |
|---|---|
| **Publish order** | 076 |
| **Course #** | 51 |
| **Module** | M05 — Microservices & Reliability |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `multi tenancy saas` |
| **Demand** | Moderate |

**Thumbnail text idea:** TENANT BOUNDARIES
**One-line hook (first 15s):** Multi-tenancy is not just adding a `tenant_id` column — it is deciding how blast radius, cost, and isolation work.

## Learning objectives
- Compare shared-table, shared-schema, database-per-tenant, and cell-based SaaS.
- Choose tenant isolation by compliance, noisy-neighbor risk, and cost.
- Design tenant-aware auth, routing, quotas, and deletion.
- Explain migration from shared tenancy to enterprise isolation.

## Topics & items to cover
- Hook: one customer’s analytics query locks a table and every other customer feels it.
- Definition: multi-tenancy serves many customer organizations from shared software while enforcing boundaries.
- Worked example: 5,000 small tenants share Postgres tables keyed by `tenant_id`; 20 enterprise tenants get dedicated databases and a router maps `tenant_slug` to a cell.
- How it works: tenant context from auth token, row-level security, composite indexes `(tenant_id, entity_id)`, per-tenant keys, quota counters, cell router.
- Tradeoffs: shared tables are cheap but risk noisy neighbors; dedicated DBs isolate but complicate migrations/reporting; cells limit blast radius.
- Real-world usage: Salesforce orgs, Slack workspaces, Atlassian cloud tenants, regional SaaS cells.
- Interview sentence: "I’ll make tenant context explicit on every request and data access path, then choose isolation tiers by risk and customer segment."
- Recap: tenancy is a boundary model across data, compute, operations, and support.

## Anecdotes & war stories to use
- Salesforce popularized large-scale multi-tenant SaaS with metadata-driven customization.
- SaaS vendors often move toward cells/regions to reduce global blast radius and satisfy residency.
- Postgres row-level security is frequently used to enforce tenant filters below app code.
- Noisy-neighbor incidents are a common reason enterprise tiers get dedicated capacity.

## Things to mention / interview tips
- Put `tenant_id` in indexes, logs, metrics, and audit events.
- Discuss tenant deletion/export workflows.
- Mention per-tenant rate limits and background job fairness.
- Separate authorization isolation from physical isolation.

## Common mistakes to call out
- Relying on developers to remember every `WHERE tenant_id = ?`.
- Using global sequential IDs that leak scale.
- Forgetting workers and caches need tenant scope.
- Offering dedicated tenancy without migration automation.

## Diagrams / visuals to draw on screen
- Shared table, shared DB, and dedicated DB models.
- Request path: auth token to tenant router to cell/database.
- Noisy-neighbor quota lane per tenant.

## Series glue
- Follows schema evolution because tenants upgrade at different speeds; next focuses on quotas and resource isolation. CTA: subscribe and use the repo matrix.
