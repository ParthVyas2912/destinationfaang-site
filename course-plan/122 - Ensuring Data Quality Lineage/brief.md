# Ensuring Data Quality & Lineage

| | |
|---|---|
| **Publish order** | 122 |
| **Course #** | 81 |
| **Module** | M08 — Data Engineering & AI Systems |
| **Type** | concept |
| **Target length** | ~12 min |
| **Primary search keyword** | `data quality lineage` |
| **Demand** | Moderate |

**Thumbnail text idea:** TRUST DATA
**One-line hook (first 15s):** Bad data is worse than no data because it makes dashboards and models confidently wrong.
## Learning objectives
- Define data quality dimensions and lineage.
- Design checks for freshness, volume, schema, nulls, and business invariants.
- Trace a metric from dashboard back to source events.
- Explain incident response for broken pipelines.

## Topics & items to cover
- Hook: the executive dashboard is only as trustworthy as the weakest upstream event.
- Definition: data quality ensures datasets meet expectations; lineage records where data came from, how it changed, and who consumes it.
- How it works: orders table expects `order_id` non-null, `total_amount >= 0`, daily row count within historical bands, schema compatible, freshness under 2 hours; a lineage graph links `checkout_service.orders` → `raw_orders` → `fact_orders` → revenue dashboard and churn model.
- Tradeoffs: strict checks catch issues early but can block pipelines; soft alerts preserve availability but risk bad downstream decisions; column-level lineage is richer but harder to maintain.
- Real-world usage: Great Expectations, Deequ, dbt tests, OpenLineage/Marquez, DataHub, Monte Carlo-style observability.
- Interview sentence: “I’ll treat datasets like APIs: contracts, owners, SLAs, tests, versioning, and consumer impact analysis.”
- Recap: prevent, detect, triage, and backfill.

## Anecdotes & war stories to use
- Amazon’s Deequ was built for large-scale data quality checks on Spark datasets.
- OpenLineage emerged to standardize lineage metadata across schedulers and engines.
- dbt made simple tests like unique/not-null common in analytics engineering workflows.
- Many ML incidents trace back to silent upstream schema or distribution changes rather than model code.

## Things to mention / interview tips
- Always include dataset owners and alert routing.
- Mention quarantine tables for bad records.
- Use freshness and volume checks before expensive transformations.
- Discuss backfill and consumer notification after an incident.

## Common mistakes to call out
- Checking only schema, not business invariants.
- Alerting everyone and owning nothing.
- Letting downstream consumers discover breakages first.
- Lacking lineage, so impact analysis becomes manual archaeology.

## Diagrams / visuals to draw on screen
- Lineage DAG from source service to dashboard/model.
- Quality gates at raw, curated, and serving layers.
- Incident flow: detect → quarantine → fix → backfill → notify.

## Series glue
- Connects warehouse/lakehouse and ML reliability; next case uses experimentation data. CTA: subscribe and download quality-check examples from GitHub.
