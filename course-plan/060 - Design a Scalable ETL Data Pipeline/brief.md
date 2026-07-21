# Design a Scalable ETL Data Pipeline

| | |
|---|---|
| **Publish order** | 060 |
| **Course #** | 118 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~28 min |
| **Primary search keyword** | `design etl pipeline` |
| **Demand** | Moderate |

**Thumbnail text idea:** ETL PIPELINE
**One-line hook (first 15s):** A scalable ETL pipeline is less about moving files and more about making bad data recoverable.

## Learning objectives
- Design batch and streaming ETL from sources to warehouse/lake.
- Model jobs, datasets, schemas, checkpoints, lineage, and quality rules.
- Handle retries, idempotency, backfills, schema evolution, and atomic publishes.

## Topics & items to cover
- Requirements: ingest DB CDC, SaaS APIs, and logs; transform to warehouse tables; daily SLA by 7am plus near-real-time updates; audit lineage and reprocess history.
- Estimation: 20TB/day raw, 500 jobs, thousands of partitions/day. Partition by `dataset_name + event_date`; checkpoint by source offset or file marker.
- API/Data model: `POST /jobs`, `GET /runs/{id}`, `POST /datasets/{id}/backfill`; entities: Source, Dataset, Job, TaskRun, SchemaVersion, Checkpoint, QualityRule.
- High-level design: connectors → raw object storage → orchestrator (Airflow/Dagster-style) → Spark/dbt transforms → curated warehouse → catalog/lineage → alerting.
- Deep dives/bottlenecks: idempotent writes using temp paths then atomic publish; schema compatibility checks and quarantine; backfills that respect downstream dependencies and don’t blindly overwrite current partitions.
- Wrap-up: raw is immutable, curated is rebuildable, every step observable.

## Anecdotes & war stories to use
- Airflow emerged at Airbnb to manage complex data workflows.
- dbt popularized versioned, tested SQL transformations.
- “Data lake swamp” is the cautionary tale when raw data lacks catalog, ownership, and quality checks.

## Things to mention / interview tips
- Use idempotency as the reliability theme.
- Add quality gates before publishing partitions.
- Include lineage for metric-debugging.

## Common mistakes to call out
- Retrying jobs that append duplicates.
- Overwriting partitions without atomic commit semantics.
- Ignoring SaaS/API schema changes.

## Diagrams / visuals to draw on screen
- Bronze/raw → silver/clean → gold/serving pipeline.
- DAG with checkpoints and retries.
- Backfill from immutable raw partitions.

## Series glue
- Builds on warehouse/precomputation. Next: event sourcing and CQRS. Subscribe and use the GitHub repo.
