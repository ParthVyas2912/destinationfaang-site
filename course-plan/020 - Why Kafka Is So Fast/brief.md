# Why Kafka Is So Fast — Message Queues Explained

| | |
|---|---|
| **Publish order** | 020 |
| **Course #** | 36 |
| **Module** | M04 — Messaging & Event-Driven Systems |
| **Type** | concept |
| **Target length** | ~18 min |
| **Primary search keyword** | `what is kafka` |
| **Demand** | Very High |

**Thumbnail text idea:** LOG SPEED
**One-line hook (first 15s):** Kafka is fast because it treats messages like an append-only log, not like tiny database rows.

## Learning objectives
- Explain Kafka's append-only log, partitions, offsets, and consumer groups.
- Understand why sequential I/O and batching make Kafka fast.
- Apply Kafka to event-driven system designs without overclaiming exactly-once.

## Topics & items to cover
- Hook: Kafka can move huge event streams because it avoids per-message random database work.
- Definition: Kafka is a distributed commit log where producers append records to topic partitions and consumers track offsets.
- How it works: topic `orders` has 12 partitions; key `merchant_id=42` hashes to partition 7, preserving order for that key; producer batches 1,000 records, broker appends sequentially, consumers in a group split partitions and commit offsets.
- Tradeoffs: partition count controls parallelism but not infinite ordering; retention enables replay but costs storage; consumer lag must be monitored; exactly-once requires careful transactional producers/consumers and still depends on sinks.
- Real-world usage: LinkedIn created Kafka for activity streams; it is common for logs, CDC, analytics, notifications, and stream processing.
- Exact interview sentence: "I would use Kafka when I need durable, replayable event streams with consumer groups, not as a simple request/response queue."
- Recap: Kafka is fast because of append-only partitions, batching, page cache, and zero-copy style transfer.

## Anecdotes & war stories to use
- Kafka originated at LinkedIn to handle high-volume activity data pipelines.
- Many companies use Kafka for change data capture so downstream systems can rebuild projections.
- Operational incidents often come from consumer lag, bad partition keys, or unbounded retention rather than broker CPU alone.

## Things to mention / interview tips
- Name the event key and why it preserves ordering.
- Discuss retention and replay as product features.
- Mention backpressure through consumer lag.
- Avoid using Kafka for synchronous user-facing RPC.

## Common mistakes to call out
- Saying Kafka globally orders a topic.
- Choosing a low-cardinality key that creates hot partitions.
- Ignoring schema evolution.
- Treating committed offset as proof the database write succeeded.

## Diagrams / visuals to draw on screen
- Topic with partitions and offsets.
- Producer batching to broker append log.
- Consumer group assignment and lag.

## Series glue
- Reference payments and notifications as event producers/consumers; point forward to e-commerce where event streams connect many domains. CTA: subscribe and see repo examples.
