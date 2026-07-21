# Microservices: DDD & Service Boundaries

| | |
|---|---|
| **Publish order** | 066 |
| **Course #** | 43 |
| **Module** | M05 — Microservices & Reliability |
| **Type** | concept |
| **Target length** | ~18 min |
| **Primary search keyword** | `microservices design` |
| **Demand** | High |

**Thumbnail text idea:** SERVICE BOUNDARIES
**One-line hook (first 15s):** Microservices fail when they’re sliced by nouns in the org chart instead of business capabilities.

## Learning objectives
- Explain DDD bounded contexts and service boundaries.
- Identify good and bad service cuts in a real domain.
- Discuss data ownership, APIs, events, transactions, and team autonomy.

## Topics & items to cover
- Hook: `UserService` often becomes a distributed database table with HTTP latency.
- Definition: microservices are independently deployable services around business capabilities; DDD bounded contexts define where models and language are consistent.
- Worked example: e-commerce split: Catalog owns product display; Inventory owns stock reservations; Ordering owns cart/order; Payments owns authorization/capture; Fulfillment owns shipments. `Order` in Ordering is not a shipment model. Services communicate with command APIs and events like `OrderPlaced`, not shared tables.
- Tradeoffs: autonomy and independent scaling; network failures, duplicated data, eventual consistency, ops overhead. Modular monolith is better for small teams/domains.
- Real usage: Amazon service ownership stories; many companies later warn about premature distributed monoliths.
- Interview sentence: “I’ll split by business capability and data ownership, not technical layer, and introduce a service only when independent deployment or scaling justifies it.”
- Recap: service boundaries are socio-technical boundaries.

## Anecdotes & war stories to use
- Amazon’s two-pizza team/service ownership story is a common reference.
- Eric Evans’ Domain-Driven Design introduced bounded contexts and ubiquitous language.
- Industry retrospectives warn about distributed monoliths from over-splitting.

## Things to mention / interview tips
- Ask “who owns the data?” for every service.
- Avoid shared databases.
- Use events for facts and APIs for commands/queries.

## Common mistakes to call out
- Splitting by controller/model/database layers.
- Making `UserService` a dependency of every request.
- Assuming microservices automatically improve reliability.

## Diagrams / visuals to draw on screen
- Bounded context map for e-commerce.
- Bad layered split vs capability split.
- Data ownership boxes with events.

## Series glue
- Opens reliability/microservices module. Next: circuit breakers and retries. Subscribe and use GitHub diagrams.
