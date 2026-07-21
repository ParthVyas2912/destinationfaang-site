# Pub/Sub Systems & Event Routing Explained

| | |
|---|---|
| **Publish order** | 041 |
| **Course #** | 37 |
| **Module** | M04 — Messaging & Event-Driven Systems |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `pub sub system` |
| **Demand** | Moderate |

**Thumbnail text idea:** EVENTS ROUTE
**One-line hook (first 15s):** Pub/sub is what lets one ‘order created’ fact wake up email, warehouse, fraud, analytics, and search—without the order service knowing all of them.

## Learning objectives
- Explain topics, subscriptions, routing keys, fanout, filtering, and delivery semantics.
- Design event routing for a concrete order-created workflow.
- Compare broker-managed subscriptions with log-based consumer groups.
- Handle retries, dead letters, ordering, and schema evolution.

## Topics & items to cover
- **Hook:** adding a loyalty service should not require editing checkout code.
- **Definition:** pub/sub lets publishers emit messages to topics while subscribers independently receive messages based on topics, filters, or routing keys.
- **Worked example:** `order.created` event: Email subscription sends receipt; Warehouse subscription reserves pick-pack; Fraud subscription scores; Analytics subscription stores facts. Topic has events keyed by `order_id`; subscriptions each have retry policy and DLQ. Add `order.cancelled` later without changing existing consumers.
- **Tradeoffs:** decoupling and fanout are strong; debugging, schema compatibility, and eventual consistency get harder. Broker filtering saves consumers work but adds routing complexity.
- **Real-world usage:** Google Pub/Sub, AWS SNS/SQS fanout, Kafka topics, RabbitMQ exchanges, NATS subjects.
- **Interview sentence:** “I’ll publish domain facts, not commands to specific downstream teams, and each subscriber owns its retry/DLQ policy.”
- **Recap:** pub/sub decouples producers from consumer count and timing.

## Anecdotes & war stories to use
- Kafka’s LinkedIn origin story is a strong example of many systems consuming the same activity events independently.
- AWS SNS to SQS fanout is a concrete managed-cloud pattern for topic-to-queue delivery.
- RabbitMQ exchanges show classic routing patterns: direct, topic, fanout, headers.
- CloudEvents is a CNCF specification that demonstrates industry need for consistent event envelopes.

## Things to mention / interview tips
- Include an event envelope: id, type, version, timestamp, producer, correlation id.
- State ordering scope: per order, per user, or no ordering.
- Add schema registry/compatibility rules for long-lived consumers.
- Use DLQs and replay tooling rather than losing bad events.

## Common mistakes to call out
- Publishing vague events like `data_changed` with no business meaning.
- Assuming all subscribers process at the same speed.
- Forgetting idempotency for redelivered messages.
- Creating cycles where events trigger infinite event loops.

## Diagrams / visuals to draw on screen
- Topic fanout from Order Service to multiple subscriptions.
- Routing-key exchange example: `order.*`, `payment.failed`.
- Retry and DLQ lifecycle per subscriber.

## Series glue
- Connect to Queues vs Streams and Food Delivery; next Job Scheduler uses events for job state changes. CTA: subscribe and see event envelope examples on GitHub.
