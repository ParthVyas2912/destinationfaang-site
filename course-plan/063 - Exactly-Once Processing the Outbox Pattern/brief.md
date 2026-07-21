# Exactly-Once Processing & the Outbox Pattern

| | |
|---|---|
| **Publish order** | 063 |
| **Course #** | 39 |
| **Module** | M04 — Messaging & Event-Driven Systems |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `exactly once outbox` |
| **Demand** | Moderate |

**Thumbnail text idea:** NO LOST EVENTS
**One-line hook (first 15s):** Exactly-once is the phrase candidates overpromise; the outbox pattern is how senior engineers stay honest.

## Learning objectives
- Explain practical exactly-once semantics versus magic delivery claims.
- Implement transactional outbox for DB + broker consistency.
- Design idempotent consumers with event IDs, offsets, and dedupe windows.

## Topics & items to cover
- Hook: update the order DB, crash before publishing `OrderCreated`, and downstream services never know.
- Definition: exactly-once usually means effects happen once through atomic writes, idempotency, and dedupe, not perfect networks.
- Worked example: one DB transaction inserts `orders(id=123,status=PLACED)` and `outbox(id=evt-9,type=OrderPlaced,payload)`. Relay publishes unsent rows to Kafka and marks sent. If it publishes twice before marking sent, consumers use `event_id` or upsert by business key to avoid double shipment.
- Tradeoffs: strong local atomicity and replay; relay lag, cleanup, and downstream idempotency still required.
- Real usage: microservices with Kafka/RabbitMQ, Debezium CDC outbox, order/payment workflows.
- Interview sentence: “I won’t rely on dual writes; I’ll write state and outbox in the same transaction, then make consumers idempotent because delivery is still at least once.”
- Recap: exactly-once is built from boring safeguards.

## Anecdotes & war stories to use
- Kafka exactly-once improves stream guarantees, but external effects still need idempotency.
- Debezium documents the outbox pattern for reliable DB event publication.
- Payment APIs expose idempotency keys because network retries are unavoidable.

## Things to mention / interview tips
- Say “dual writes are the bug.”
- Walk through crash points.
- Distinguish broker delivery from business side effects.

## Common mistakes to call out
- Claiming Kafka alone solves all exactly-once problems.
- Publishing before DB commit.
- Making email/payment/shipping consumers non-idempotent.

## Diagrams / visuals to draw on screen
- Failed dual-write timeline.
- Business row + outbox row in one transaction.
- Relay retry and dedupe consumer flow.

## Series glue
- Follows event sourcing and supports stream processing. Subscribe and grab GitHub sketches.
