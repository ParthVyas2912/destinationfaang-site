# Stream Processing at Scale (Flink / Spark)

| | |
|---|---|
| **Publish order** | 064 |
| **Course #** | 41 |
| **Module** | M04 — Messaging & Event-Driven Systems |
| **Type** | concept |
| **Target length** | ~16 min |
| **Primary search keyword** | `stream processing` |
| **Demand** | Moderate |

**Thumbnail text idea:** STREAMS AT SCALE
**One-line hook (first 15s):** Batch asks what happened yesterday; stream processing asks what should we do in the next five seconds?

## Learning objectives
- Explain events, windows, state, watermarks, checkpoints, and sinks.
- Compare Flink/Spark-style stateful processing with simple consumers.
- Design scalable jobs for joins, aggregations, alerts, late data, and recovery.

## Topics & items to cover
- Hook: counting purchases per minute is easy until events arrive late and workers restart mid-window.
- Definition: stream processing continuously transforms unbounded event streams using time windows and stateful operators.
- Worked example: 100K events/sec purchase stream. Key by `user_id` for sessions, aggregate 1-minute revenue windows by `merchant_id`, use event time with a 2-minute watermark. Operator state stores partial aggregates; checkpoints snapshot offsets plus state. On failure, restore checkpoint and replay Kafka offsets.
- Tradeoffs: low latency and continuous outputs; operational complexity, state size, late-event rules, debugging difficulty.
- Real usage: fraud velocity checks, real-time analytics, IoT alerts, ad bidding, CDC materialized views.
- Interview sentence: “For stateful real-time aggregation, I’ll use event-time windows with watermarks and checkpointed state, then make sinks idempotent or transactional.”
- Recap: streams need time semantics and recovery semantics, not consumers in a loop.

## Anecdotes & war stories to use
- Flink is known for stateful event-time processing and checkpointing.
- Spark Streaming made micro-batch processing approachable.
- The Dataflow model paper shaped modern watermark/window thinking.

## Things to mention / interview tips
- Define event time vs processing time.
- Pick tumbling, sliding, or session windows explicitly.
- Use state TTL for unbounded keys.

## Common mistakes to call out
- Treating Kafka consumers as a full stream processor.
- Ignoring late data and correction output.
- Writing non-idempotent sinks after retries.

## Diagrams / visuals to draw on screen
- Kafka partitions → keyed operators → sink.
- Window with watermark and late event.
- Checkpoint restore sequence.

## Series glue
- Builds on outbox reliability. Next: recommendation engines. Subscribe and use GitHub diagrams.
