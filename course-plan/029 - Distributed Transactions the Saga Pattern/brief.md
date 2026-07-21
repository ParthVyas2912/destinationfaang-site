# Distributed Transactions & the Saga Pattern

| | |
|---|---|
| **Publish order** | 029 |
| **Course #** | 40 |
| **Module** | M04 — Messaging & Event-Driven Systems |
| **Type** | concept |
| **Target length** | ~20 min |
| **Primary search keyword** | `saga pattern` |
| **Demand** | High |

**Thumbnail text idea:** NO 2PC NEEDED
**One-line hook (first 15s):** The moment your order, payment, inventory, and email live in different services, one database transaction is gone—so what replaces it?

## Learning objectives
- Explain Saga orchestration vs choreography with concrete order-flow steps.
- Design compensating actions and idempotent message handlers.
- Decide when Saga is appropriate versus 2PC or a single-service transaction.
- Identify failure modes: duplicate events, stuck steps, and partial completion.

## Topics & items to cover
- **Hook:** checkout succeeds in payment but inventory reservation times out; the user needs a truthful final state.
- **Definition:** a Saga is a sequence of local transactions where each successful step has a compensating step if the workflow later fails.
- **Worked example:** order total $80. Step 1 create `Order=PENDING`; Step 2 reserve 2 SKUs; Step 3 authorize card; Step 4 create shipment; Step 5 mark `CONFIRMED`. If shipment fails, release inventory and void authorization. Each command carries `saga_id`, `step`, and idempotency key.
- **Tradeoffs:** better availability and service autonomy than 2PC; weaker isolation, more state-machine complexity, and compensation may be business-specific rather than true rollback.
- **Real-world usage:** e-commerce checkout, travel booking, food delivery assignment/payment, account onboarding.
- **Interview sentence:** “I’ll model this as a durable workflow state machine with idempotent steps and explicit compensations, not as a distributed DB transaction.”
- **Recap:** Saga gives eventual consistency with auditable progress.

## Anecdotes & war stories to use
- The Saga pattern traces back to the 1987 paper “Sagas” by Hector Garcia-Molina and Kenneth Salem for long-lived transactions.
- Chris Richardson’s microservices material popularized orchestration/choreography examples like order creation with customer credit reservation.
- AWS Step Functions and Temporal are modern workflow engines that embody durable retries and state transitions for Saga-like flows.
- Stripe-style idempotency keys are essential because retries are normal when payment or network calls are uncertain.

## Things to mention / interview tips
- Name the coordinator if using orchestration: OrderWorkflow owns state, not every service guessing.
- Every handler must be idempotent: receiving `ReserveInventory` twice must not reserve twice.
- Compensation is not always inverse; “refund” is different from “pretend the charge never happened.”
- Add dead-letter queues and operator dashboards for stuck sagas.

## Common mistakes to call out
- Calling compensation “rollback” as if external side effects disappear.
- Forgetting to persist saga state before making the next call.
- Letting services publish events without a correlation ID.
- Choosing Saga for strongly isolated financial ledger writes that need a single atomic boundary.

## Diagrams / visuals to draw on screen
- Orchestrated order saga state machine.
- Choreography event chain with correlation IDs.
- Failure path showing compensation arrows.

## Series glue
- Tie back to Payment System and Kafka; preview Ledger/Reconciliation where Sagas are not enough for accounting truth. CTA: subscribe and get workflow diagrams on GitHub.
