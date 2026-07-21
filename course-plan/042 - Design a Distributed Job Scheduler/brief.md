# Design a Distributed Job Scheduler

| | |
|---|---|
| **Publish order** | 042 |
| **Course #** | 115 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~30 min |
| **Primary search keyword** | `design job scheduler` |
| **Demand** | High |

**Thumbnail text idea:** RUN IT ONCE
**One-line hook (first 15s):** A distributed scheduler is easy until every worker thinks it owns the midnight billing job—or no worker runs it at all.

## Learning objectives
- Design recurring and one-off job scheduling across many workers.
- Use leases, heartbeats, idempotency, and retries to avoid duplicate side effects.
- Model job state, priority, dependencies, and execution history.
- Explain leader election vs partitioned schedulers and time-skew issues.

## Topics & items to cover
- **Step 1 — Requirements:** create cron/one-time jobs, run near scheduled time, retry failures, track status/logs, support priorities and cancellation. Exclude arbitrary workflow language unless asked. At-least-once execution with idempotent jobs.
- **Step 2 — Estimation:** millions of schedules, bursts at minute boundaries, job duration seconds to hours. Scheduler scans due jobs; workers execute and heartbeat.
- **Step 3 — API/Data model:** `POST /jobs`, `POST /jobs/{id}/cancel`, `GET /jobs/{id}`. Tables: JobDefinition, JobRun, Lease(owner, expires_at), Attempt, Dependency.
- **Step 4 — HLD:** API → scheduler partitions jobs by `job_id` hash/time bucket → durable DB/queue → worker pool → heartbeat/status store; metrics/alerts.
- **Step 5 — Deep dives:** 1) Claiming: conditional update due job from `scheduled` to `leased` with expiry. 2) Failure: heartbeat timeout requeues; retries use exponential backoff and max attempts. 3) Scale/time: bucket by next_run_time, jitter cron bursts, use UTC and tolerate clock skew.
- **Step 6 — Wrap-up:** promise at-least-once, then require idempotency key per run for side effects.

## Anecdotes & war stories to use
- Google Borg/Kubernetes CronJob concepts show cluster-level scheduling and controller reconciliation patterns.
- Airbnb’s Airflow origin and Apache Airflow’s DAG scheduler are familiar examples for workflow scheduling.
- Temporal/Cadence demonstrate durable timers and workflow replay for long-running jobs.
- Slack has written about job-queue redesigns, a useful reminder that queues and workers become core reliability infrastructure.

## Things to mention / interview tips
- Say “exactly-once scheduling is unrealistic; exactly-once effect requires idempotent operations.”
- Use leases with expiry, not permanent ownership flags.
- Track attempts separately from logical job runs.
- Add jitter to avoid every cron firing at `:00`.

## Common mistakes to call out
- Relying on one in-memory scheduler process with no recovery.
- No heartbeat, so stuck workers hold jobs forever.
- Retrying non-idempotent jobs like “charge card” blindly.
- Ignoring time zones and daylight-saving behavior for user cron.

## Diagrams / visuals to draw on screen
- Job lifecycle: scheduled → leased → running → succeeded/failed/retry.
- Lease/heartbeat sequence between worker and DB.
- Time-bucketed scheduler partitions.

## Series glue
- Reference Pub/Sub, Backoff, and Leader Election; next Paxos/Raft explains the consensus behind safe coordination. CTA: subscribe and get state machines on GitHub.
