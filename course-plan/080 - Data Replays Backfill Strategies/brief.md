# Data Replays & Backfill Strategies

| | |
|---|---|
| **Publish order** | 080 |
| **Course #** | 42 |
| **Module** | M04 — Messaging & Event-Driven Systems |
| **Type** | concept |
| **Target length** | ~12 min |
| **Primary search keyword** | `data backfill` |
| **Demand** | Moderate |

**Thumbnail text idea:** REPLAY SAFELY
**One-line hook (first 15s):** Backfill is production traffic wearing a batch-job disguise — treat it casually and it will take your database down.

## Learning objectives
- Design safe replay/backfill jobs for streams and databases.
- Choose idempotency keys, checkpoints, and throttling controls.
- Avoid double-counting, ordering bugs, and downstream overload.
- Explain replay versus direct database migration.

## Topics & items to cover
- Hook: a new analytics column needs two years of history without breaking today’s pipeline.
- Definition: backfill populates historical data; replay reprocesses past events through current logic.
- Worked example: replay Kafka topic `orders` from offset 0 to rebuild `daily_revenue`. Use idempotency key `order_id:version`, checkpoint every 10,000 events, throttle to 2,000 events/sec, and write a shadow table before cutover.
- How it works: source snapshot, offsets, watermarks, dedupe table, batch size, rate limiter, dry run, validation query, rollback.
- Tradeoffs: replay preserves business logic but may trigger side effects; direct SQL is faster but bypasses domain logic; old events may not match new schemas.
- Real-world usage: Kafka reprocessing, Airflow/dbt backfills, Flink savepoints, warehouse partition rebuilds.
- Interview sentence: "I’ll make the job idempotent, checkpointed, throttled, and validated against shadow output before promoting it."
- Recap: replay needs correctness and blast-radius control.

## Anecdotes & war stories to use
- Kafka’s retained log model made replay a core pattern for rebuilding derived views.
- LinkedIn’s Kafka origin story centered on activity streams as durable logs.
- Airflow became popular partly because scheduled backfills are normal data-platform work.
- dbt-style transformations emphasize rebuilding models from raw history with tests.

## Things to mention / interview tips
- Disable side effects like emails/webhooks during replay.
- Use checkpointing so restart does not start from zero.
- Validate counts and aggregates before cutover.
- Throttle backfill separately from online traffic.

## Common mistakes to call out
- Re-emitting old events to live consumers without a replay flag.
- Assuming old event schemas deserialize cleanly.
- Running an unbounded SQL update during peak hours.
- Not making writes idempotent.

## Diagrams / visuals to draw on screen
- Event log replay to shadow table, then cutover.
- Checkpoint and watermark timeline.
- Online traffic lane versus throttled backfill lane.

## Series glue
- References earlier Kafka/event videos and reliability guardrails; next revisits availability language with SLA/SLO/SLI. CTA: subscribe and use the repo runbook.
