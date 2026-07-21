# Design a Ledger & Payment Reconciliation System

| | |
|---|---|
| **Publish order** | 036 |
| **Course #** | 108 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~35 min |
| **Primary search keyword** | `design ledger system` |
| **Demand** | Moderate |

**Thumbnail text idea:** MONEY MUST BALANCE
**One-line hook (first 15s):** Payment systems can fail and retry; ledgers cannot ‘kind of’ balance. This design is about making money movements auditable forever.

## Learning objectives
- Design double-entry ledger accounts, journal entries, balances, and reconciliation.
- Separate payment processing from accounting truth.
- Use idempotency, immutability, and audit trails for financial correctness.
- Explain reconciliation against external processors and bank statements.

## Topics & items to cover
- **Step 1 — Requirements:** record transfers, maintain account balances, expose transaction history, reconcile with payment providers/banks, support corrections. Exclude trading/risk. Invariant: every journal entry sums to zero.
- **Step 2 — Estimation:** ledger writes are modest compared with reads but require durability. Balance reads may be high; compute from immutable entries or maintain materialized balances transactionally.
- **Step 3 — API/Data model:** `POST /journal-entries` with idempotency key, `GET /accounts/{id}/balance`, `POST /reconciliation-runs`. Tables: Account, JournalEntry, Posting(debit/credit), BalanceSnapshot, ExternalTransaction, ReconciliationResult.
- **Step 4 — HLD:** payment service emits authorized/captured/refunded events → ledger service validates balanced postings → immutable ledger DB → balance projector → reconciliation workers import processor/bank files.
- **Step 5 — Deep dives:** 1) Double-entry atomic write: debit customer cash, credit merchant payable in one DB transaction. 2) Idempotency: provider event id prevents duplicate postings. 3) Reconciliation: match by provider id, amount, currency, date window; exceptions queue for ops.
- **Step 6 — Wrap-up:** never mutate history; corrections are reversing entries.

## Anecdotes & war stories to use
- Stripe has publicly emphasized idempotency keys and robust payment APIs because network retries are unavoidable.
- Square/Block and Airbnb engineering writings discuss ledgers as immutable financial records rather than mutable balances.
- Banking reconciliation practices predate software: external statements are independent truth sources to compare against internal books.
- The Saga pattern is useful around payments, but final accounting should be a strong transactional ledger boundary.

## Things to mention / interview tips
- Say the invariant: “sum of postings for a journal entry must equal zero per currency.”
- Use integer minor units, never floating point, for money.
- Treat balance as derived from ledger, even if materialized for speed.
- Include audit fields: source event, actor, timestamps, trace id.

## Common mistakes to call out
- Updating account balances directly without immutable entries.
- Mixing authorization/capture/refund semantics into one vague “payment” state.
- Ignoring duplicate webhooks from providers.
- Reconciling only totals instead of transaction-level exceptions.

## Diagrams / visuals to draw on screen
- Double-entry posting table for a $100 customer-to-merchant transfer.
- Payment event → ledger → balance projector pipeline.
- Reconciliation matching table: internal vs external vs exception.

## Series glue
- Reference Payment System and Saga; forward to API Design and Ad Auctions where money and idempotency reappear. CTA: subscribe and get ledger schemas on GitHub.
