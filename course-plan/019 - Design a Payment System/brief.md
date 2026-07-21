# Design a Payment System (Stripe-Style)

| | |
|---|---|
| **Publish order** | 019 |
| **Course #** | 99 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~40 min |
| **Primary search keyword** | `design payment system` |
| **Demand** | High |

**Thumbnail text idea:** PAYMENTS SAFELY
**One-line hook (first 15s):** In payments, success is not low latency; success is never charging twice and always reconciling.

## Learning objectives
- Design payment intents, authorization, capture, refunds, and reconciliation.
- Use idempotency keys and ledgers to prevent double charges.
- Explain provider integration and asynchronous webhooks.

## Topics & items to cover
- Requirements: create payment, charge card/bank, handle 3DS/auth, capture, refund, webhooks, merchant dashboard, audit trail.
- Estimation: correctness beats latency; external providers are slow/unreliable; every state transition must be auditable.
- API/Data model: `POST /payment_intents` with `Idempotency-Key`, `POST /payment_intents/{id}/confirm`, `POST /refunds`; `PaymentIntent(id, merchant_id, amount, currency, state)`, `Charge`, `LedgerEntry(account_id, amount, direction, ref_id)`; shard by merchant/time or intent ID.
- High-level design: API creates intent, payment orchestrator calls processor, state machine records auth/capture/refund, webhook handler reconciles provider events, ledger records immutable entries.
- Deep dives/bottlenecks: idempotency keys dedupe client retries; state transitions must be transactional with ledger writes; reconciliation jobs compare internal state with provider settlement files.
- Wrap-up: never mutate balances directly; append ledger entries and derive balances.

## Anecdotes & war stories to use
- Stripe popularized PaymentIntents and idempotency keys as developer-facing primitives for reliable payment flows.
- PayPal and card networks show why asynchronous settlement and disputes are normal, not edge cases.
- Double-charge incidents are reputationally severe, so payment systems bias toward auditability over speed.

## Things to mention / interview tips
- Say: "Every externally retried operation has an idempotency key and every money movement has an immutable ledger entry."
- Distinguish auth, capture, settlement, refund, and chargeback.
- Treat webhooks as at-least-once and out-of-order.
- Store provider request/response IDs for reconciliation.

## Common mistakes to call out
- Updating a `balance` column without a ledger.
- Assuming provider callbacks arrive once and in order.
- Charging synchronously without retry/idempotency semantics.
- Ignoring currency, precision, and audit requirements.

## Diagrams / visuals to draw on screen
- PaymentIntent state machine.
- API/orchestrator/provider/webhook flow.
- Double-entry ledger entries for a charge and refund.

## Series glue
- Reference Dropbox commit semantics; point forward to Kafka because payment webhooks and ledgers often feed event streams. CTA: subscribe and grab the GitHub checklist.
