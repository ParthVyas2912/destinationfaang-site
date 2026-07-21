# Orchestration: Airflow vs Temporal

| | |
|---|---|
| **Publish order** | 120 |
| **Course #** | 79 |
| **Module** | M08 — Data Engineering & AI Systems |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `airflow vs temporal` |
| **Demand** | Moderate |

**Thumbnail text idea:** DAGS OR WORKFLOWS
**One-line hook (first 15s):** Airflow and Temporal both orchestrate work, but one thinks in scheduled DAGs and the other thinks in durable code execution.
## Learning objectives
- Explain the difference between data orchestration and durable workflow orchestration.
- Choose Airflow or Temporal for concrete scenarios.
- Model retries, state, backfills, and human-in-the-loop steps.
- Avoid using one tool as a poor substitute for the other.

## Topics & items to cover
- Hook: choosing the wrong orchestrator creates invisible operational pain.
- Definition: Airflow schedules and monitors DAGs of tasks; Temporal runs fault-tolerant workflows whose state survives crashes and retries.
- How it works: an ETL DAG extracts orders hourly, transforms with dbt, loads a warehouse, and backfills last month; a checkout workflow reserves inventory, charges payment, sends email, waits for shipment, and compensates if payment fails.
- Tradeoffs: Airflow is excellent for cron-like batch pipelines and lineage views; Temporal is better for long-running business processes, retries, signals, and compensation; Airflow DAG code should not become a request-time transaction engine.
- Real-world usage: Airflow in data teams; Temporal/Cadence-style systems for payments, provisioning, and order workflows.
- Interview sentence: “If the work is scheduled data movement, I’ll use Airflow; if it is a user/business transaction that must survive failures for days, I’ll use Temporal.”
- Recap: schedule vs stateful workflow is the axis.

## Anecdotes & war stories to use
- Airbnb open-sourced Airflow after using it to manage complex data workflows.
- Uber’s Cadence, the predecessor idea behind Temporal, addressed durable workflow execution at service scale.
- Payment and fulfillment systems need compensation steps; simple queues often lose the process context.
- Data teams love Airflow backfills, but request-serving teams need lower-latency workflow state.

## Things to mention / interview tips
- Ask if tasks are time-scheduled or event/user-triggered.
- Mention idempotent activities and retry policies.
- For Airflow, discuss backfills, SLAs, and task dependencies.
- For Temporal, discuss signals, timers, compensation, and workflow history.

## Common mistakes to call out
- Using Airflow for synchronous checkout flows.
- Building cron spaghetti instead of a visible DAG.
- Retrying non-idempotent payments without idempotency keys.
- Ignoring workflow versioning during deployments.

## Diagrams / visuals to draw on screen
- Airflow DAG for hourly ETL.
- Temporal workflow timeline with retry and compensation.
- Decision matrix: data pipeline vs business process.

## Series glue
- Builds on batch/streaming and prepares for ML pipelines. CTA: subscribe and grab the orchestration comparison sheet from GitHub.
