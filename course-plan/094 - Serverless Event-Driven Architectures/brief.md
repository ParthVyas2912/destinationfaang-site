# Serverless & Event-Driven Architectures

| | |
|---|---|
| **Publish order** | 094 |
| **Course #** | 73 |
| **Module** | M07 — Cloud & Infrastructure |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `serverless architecture` |
| **Demand** | High |

**Thumbnail text idea:** EVENTS RUN CODE
**One-line hook (first 15s):** Serverless is not “no servers”; it is choosing queues, functions, and managed state so failures become retries, not pager alerts.

## Learning objectives
- Distinguish functions, managed storage, event buses, queues, and workflows.
- Design idempotent handlers with retries and dead-letter queues.
- Explain cold starts, concurrency limits, ordering, and exactly-once myths.
- Decide when serverless beats containers in an interview design.

## Topics & items to cover
- Hook: checkout should not synchronously email, invoice, update analytics, and call fulfillment in one request.
- Definition: short-lived handlers run on events while the provider manages scale and infrastructure.
- Worked example: 1,000 orders/min enter `OrderCreated`; payment function has concurrency 200, writes idempotency key `order_id:attempt`, emits `PaymentCaptured`, retries 3 times, then DLQ.
- How it works: API Gateway -> function -> queue/event bus -> subscriber functions -> state store; use outbox when events originate from DB transactions.
- Tradeoffs: scale-to-zero and speed versus cold starts, vendor coupling, local testing, and trace complexity.
- Real-world usage: thumbnails, IoT ingestion, fraud signals, scheduled jobs, SaaS glue.
- Interview sentence: “Each consumer is idempotent, durable queues sit between steps, and DLQs plus correlation IDs make retries observable.”
- Recap: serverless wins for bursty, independent events with at-least-once delivery.

## Anecdotes & war stories to use
- AWS Lambda made managed functions mainstream; concurrency quotas quickly became an architecture concern.
- Stripe-style webhooks teach receivers to be idempotent because senders retry ambiguous failures.
- Object-storage events naturally power image/video processing pipelines.
- Step Functions, Temporal, and Durable Functions exist because long business processes need explicit state.

## Things to mention / interview tips
- Say “at-least-once unless proven otherwise.”
- Put idempotency keys in the schema.
- Define DLQ ownership: alert, inspect, replay, or compensate.
- Use workflow engines for sagas, humans, and long timers.

## Common mistakes to call out
- Chaining direct function calls instead of durable events.
- Ignoring duplicates and double-charging.
- Assuming ordering across partitions.
- Using serverless for long-lived low-latency sockets without checking limits.

## Diagrams / visuals to draw on screen
- Checkout event fanout to payment, email, fulfillment, analytics.
- Retry/backoff timeline ending in DLQ.
- Outbox table draining to event bus.
- Concurrency throttling under burst traffic.

## Series glue
- Reference queues, pub/sub, and idempotency from earlier reliability videos. Next: multi-region design, where events power recovery. CTA: subscribe and check GitHub for event schemas.
