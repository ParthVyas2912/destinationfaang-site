# Message Queues vs Event Streams (Kafka vs RabbitMQ)

| | |
|---|---|
| **Publish order** | 033 |
| **Course #** | 35 |
| **Module** | M04 — Messaging & Event-Driven Systems |
| **Type** | concept |
| **Target length** | ~16 min |
| **Primary search keyword** | `message queue vs event stream` |
| **Demand** | High |

**Thumbnail text idea:** QUEUE OR STREAM
**One-line hook (first 15s):** Kafka and RabbitMQ both move messages, but in interviews the winning answer is knowing whether you need work distribution or an immutable event log.

## Learning objectives
- Distinguish queues, pub/sub, and event streams by retention and consumption model.
- Pick Kafka, RabbitMQ/SQS, or pub/sub for concrete workloads.
- Explain ordering, consumer groups, retries, dead letters, and replay.
- Avoid common “Kafka for everything” mistakes.

## Topics & items to cover
- **Hook:** sending password-reset emails and replaying every order event for analytics are not the same problem.
- **Definition:** a queue assigns work to consumers and usually removes/acknowledges messages; an event stream stores an ordered log that consumers read by offset and can replay.
- **Worked example:** 10k orders/min. Email workers use a queue: each order email is processed once with DLQ on failure. Analytics uses Kafka topic `orders`, 12 partitions by `merchant_id`; fraud, warehouse, and BI consumer groups each maintain offsets and replay from yesterday if their code changes.
- **Tradeoffs:** queues simplify task distribution and retries; streams provide retention, replay, and multiple independent consumers but require partition-key and offset discipline.
- **Real-world usage:** RabbitMQ/SQS/Celery for jobs; Kafka/Pulsar/Kinesis for event logs; Redis streams for lighter use.
- **Interview sentence:** “If I need replay and multiple independent consumers, I’ll use an event stream; if I need one worker to perform a task, I’ll use a queue.”
- **Recap:** retention and ownership of consumption are the core difference.

## Anecdotes & war stories to use
- Kafka was created at LinkedIn to handle high-volume activity streams and became open source through Apache.
- RabbitMQ’s AMQP roots make it a classic broker for routing, acknowledgments, and work queues.
- AWS SQS visibility timeout is a concrete example of queue leasing rather than true deletion at receive time.
- Many companies use Kafka compacted topics for latest state, showing streams are not only for analytics.

## Things to mention / interview tips
- Always name the partition key and what ordering guarantee it gives.
- Include DLQ and retry backoff for queues; include retention and offset commits for streams.
- Say whether messages are commands (“send email”) or facts (“order_created”).
- Mention idempotent consumers because duplicate delivery is normal.

## Common mistakes to call out
- Claiming queues guarantee exactly-once side effects.
- Partitioning Kafka by random UUID then needing per-user ordering.
- Using a stream when no replay or fanout is needed.
- Forgetting poison messages that block a partition or queue.

## Diagrams / visuals to draw on screen
- Queue: many workers compete for one task stream.
- Kafka log: partitions, offsets, consumer groups.
- Retry/DLQ flow for failed messages.

## Series glue
- Connect to Kafka performance and Notification System; next Food Delivery uses both streams and queues. CTA: subscribe and see comparison tables on GitHub.
