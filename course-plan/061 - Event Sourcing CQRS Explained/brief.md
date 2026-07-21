# Event Sourcing & CQRS Explained

| | |
|---|---|
| **Publish order** | 061 |
| **Course #** | 38 |
| **Module** | M04 — Messaging & Event-Driven Systems |
| **Type** | concept |
| **Target length** | ~18 min |
| **Primary search keyword** | `event sourcing cqrs` |
| **Demand** | High |

**Thumbnail text idea:** EVENTS AS TRUTH
**One-line hook (first 15s):** What if your database didn’t store the current account balance—it stored every deposit and withdrawal forever?

## Learning objectives
- Explain event sourcing and CQRS without buzzwords.
- Design command handlers, event store, projections, query models, snapshots, and replay.
- Decide when event sourcing helps versus when CRUD is simpler.

## Topics & items to cover
- Hook: current state is convenient, but history explains bugs.
- Definition: event sourcing stores immutable state changes; CQRS separates write commands from read-optimized projections.
- Worked example: account stream has `DepositMade($100)`, `CardHoldPlaced($20)`, `WithdrawalMade($30)`. Command handler reconstructs account from stream `account-123`, validates withdrawal, appends event with expected version 17. Projectors update `AccountBalanceView` and `MonthlyStatementView`; snapshots every 500 events avoid full replay.
- Tradeoffs: audit trail, replayable projections, temporal debugging; more moving parts, eventual consistency, schema/version burden.
- Real usage: ledgers, order lifecycles, inventory reservations, collaborative systems.
- Interview sentence: “I’d use event sourcing when history is the source of truth and multiple read models need replay; otherwise a normal relational model is cheaper.”
- Recap: events are facts; projections are disposable views.

## Anecdotes & war stories to use
- Martin Fowler’s writing popularized CQRS/event sourcing vocabulary.
- Kafka’s log abstraction made replayable event streams familiar.
- Financial ledgers have long used append-only transaction records for auditability.

## Things to mention / interview tips
- Name events in past tense: `OrderShipped`, not `ShipOrder`.
- Use optimistic concurrency with stream version.
- Make projectors idempotent and replay-safe.

## Common mistakes to call out
- Emitting vague `EntityUpdated` events.
- Mutating old events.
- Using CQRS everywhere because it sounds advanced.

## Diagrams / visuals to draw on screen
- Command handler → event store → projectors → read models.
- Account stream reconstructing balance.
- Snapshot plus replay timeline.

## Series glue
- Opens messaging module. Next: exactly-once and outbox. Subscribe and see GitHub examples.
