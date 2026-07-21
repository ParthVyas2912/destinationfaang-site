# Batch vs Streaming Data Pipelines

| | |
|---|---|
| **Publish order** | 119 |
| **Course #** | 78 |
| **Module** | M08 — Data Engineering & AI Systems |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `batch vs streaming` |
| **Demand** | High |

**Thumbnail text idea:** BATCH OR STREAM
**One-line hook (first 15s):** Most pipeline mistakes come from forcing everything to be streaming when the business only needed yesterday’s answer — or batching something that needed seconds.
## Learning objectives
- Decide when a data pipeline should be batch, streaming, or hybrid.
- Explain latency, correctness, cost, and operational tradeoffs.
- Walk through concrete examples: fraud, dashboards, billing, personalization.
- Use event-time, watermarks, and backfills correctly.

## Topics & items to cover
- Hook: freshness is a product requirement, not a default architecture choice.
- Definition: batch processes bounded data on a schedule; streaming processes unbounded event flows continuously.
- How it works: daily revenue reporting can run Spark/dbt at 2 a.m. over yesterday’s partition; fraud detection reads card events from Kafka, updates 10-minute counters, and scores within 100 ms; a hybrid system streams recent counters then backfills the warehouse nightly.
- Tradeoffs: batch is simpler, cheaper, and easier to replay; streaming gives low latency but needs state, watermarks, exactly-once/idempotency thinking, and harder debugging.
- Real-world usage: Kafka/Flink for real-time events; Spark/dbt/Airflow for batch analytics; Lambda/Kappa-style architectures in data platforms.
- Interview sentence: “I’ll choose streaming only for decisions whose value decays within minutes; otherwise batch plus backfill is usually safer.”
- Recap: design around freshness SLA, replayability, and downstream consumers.

## Anecdotes & war stories to use
- LinkedIn created Kafka to handle high-volume activity streams across products.
- Apache Flink became popular for stateful streaming where event-time correctness matters.
- Many analytics teams adopted dbt because scheduled SQL transformations are enough for most reporting workflows.
- Fraud and ads bidding are classic cases where waiting for a daily batch is too late.

## Things to mention / interview tips
- Ask for required freshness: seconds, minutes, hours, or daily.
- Say “idempotent sinks” and “replay from offset/checkpoint.”
- Mention late events and watermarks for windowed aggregations.
- Include a backfill plan even for streaming systems.

## Common mistakes to call out
- Treating streaming as automatically more correct.
- Forgetting that dashboards often tolerate stale data.
- Ignoring duplicate events and replay semantics.
- Not separating event time from processing time.

## Diagrams / visuals to draw on screen
- Batch DAG vs streaming topology.
- Event-time window with late arrival.
- Hybrid serving layer: stream hot data + batch historical data.

## Series glue
- Connects feature stores and personalization to data infrastructure; next is Airflow vs Temporal. CTA: subscribe and use the repo’s freshness decision tree.
