# Mock System Design Interview: E-Commerce Checkout

| | |
|---|---|
| **Publish order** | 130 |
| **Course #** | MOCK3 |
| **Module** | M10 — Mock Interview & Practice |
| **Type** | mock |
| **Target length** | ~55 min |
| **Primary search keyword** | `mock system design interview` |
| **Demand** | High |

**Thumbnail text idea:** CHECKOUT MOCK
**One-line hook (first 15s):** Checkout design is where interviewers test whether you understand money: idempotency, inventory, payment failure, and compensation.
## Learning objectives
- Practice an e-commerce checkout system design interview.
- Model cart, orders, payments, inventory reservations, and fulfillment.
- Explain idempotency and exactly-once effects in payment flows.
- Use rubric cues for senior-level tradeoff discussion.

## Topics & items to cover
- 0-5 min clarify: marketplace or single merchant, digital/physical goods, coupons, tax, payment providers, guest checkout.
- 5-10 requirements: create cart, price items, reserve inventory, authorize/capture payment, create order, send confirmation; availability vs consistency decisions.
- 10-15 estimation: checkout QPS, SKU count, peak sale spikes; rubric: identifies payment and inventory as correctness hotspots.
- 15-23 APIs/data: `POST /checkout`, `POST /payments/confirm`, `GET /orders/{id}`; `Cart`, `InventoryReservation`, `PaymentAttempt`, `Order`, `OrderEvent`; shard orders by `user_id` or `order_id`, inventory by `sku_id`.
- 23-38 design: checkout orchestrator validates cart/prices, reserves inventory, creates payment intent, commits order, emits events to fulfillment/email.
- 38-50 deep dives: idempotency keys for retries; reservation TTL and release; saga/Temporal-style compensation when payment succeeds but order creation fails; fraud/risk checks.
- 50-55 wrap: metrics: conversion, payment success, oversell rate, checkout latency, abandoned carts.

## Anecdotes & war stories to use
- Stripe’s public API design popularized idempotency keys for safe payment retries.
- Ticketing and flash-sale systems show why inventory reservation and queueing matter under spikes.
- Amazon-style checkout experiences hide complex pricing, tax, inventory, and fulfillment workflows.
- Payment providers use asynchronous webhooks, so systems must handle out-of-order confirmations.

## Things to mention / interview tips
- Say “external payment calls are not exactly-once; my system makes retries safe.”
- Keep an immutable order event log for auditability.
- Use reservation TTLs rather than holding inventory forever.
- Separate authorization from capture if fulfillment can fail.

## Common mistakes to call out
- Charging the card before validating inventory and price.
- Retrying payment without idempotency.
- Treating webhooks as ordered and reliable.
- Ignoring oversell during flash sales.

## Diagrams / visuals to draw on screen
- Checkout saga sequence diagram.
- Inventory reservation state machine.
- Payment attempt lifecycle with webhook reconciliation.

## Series glue
- References APIs, transactions, queues, and Temporal; next speed drills sharpen estimates and schemas. CTA: subscribe and practice with the repo rubric.
