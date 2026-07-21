# Design a Food Delivery App (DoorDash / Zomato)

| | |
|---|---|
| **Publish order** | 034 |
| **Course #** | 104 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~35 min |
| **Primary search keyword** | `design food delivery` |
| **Demand** | High |

**Thumbnail text idea:** DELIVER HOT FOOD
**One-line hook (first 15s):** Food delivery is three systems colliding: marketplace search, real-time dispatch, and money movement—under a promise that dinner arrives on time.

## Learning objectives
- Design restaurant browsing, cart/order, driver dispatch, tracking, and payment flows.
- Model geo queries, ETA, assignment, and order state transitions.
- Use events and sagas for restaurant acceptance, courier pickup, and payment.
- Identify bottlenecks in peak dinner traffic and real-time location updates.

## Topics & items to cover
- **Step 1 — Requirements:** browse nearby restaurants, menu/cart, place order, restaurant accept/reject, assign courier, live tracking, payment/refund. Exclude ads and loyalty. Low-latency tracking; strong money/order state.
- **Step 2 — Estimation:** city peak: many read searches, fewer order writes, courier GPS every few seconds. Location writes are high-volume ephemeral; order state is durable.
- **Step 3 — API/Data model:** `GET /restaurants?lat,lng`, `POST /orders`, `POST /orders/{id}/accept`, `POST /couriers/{id}/location`, `POST /dispatch/assign`. Entities: Restaurant, MenuItem, Order, Delivery, CourierLocation, Payment.
- **Step 4 — HLD:** client/gateway → restaurant/menu service + geo index → order service → payment → dispatch service → courier app; Kafka for order events; Redis/geo store for live courier positions.
- **Step 5 — Deep dives:** 1) Dispatch matching: filter couriers by H3/geohash cell, rank by ETA, capacity, fairness; lease assignment. 2) Order saga: authorize payment, restaurant accept, courier assign; compensate with void/refund. 3) Tracking scale: store latest location in Redis, append sampled events for history.
- **Step 6 — Wrap-up:** consistency differs: menu can be stale briefly, payment/order cannot.

## Anecdotes & war stories to use
- Uber’s H3 hexagonal indexing is a well-documented geo-indexing reference for nearby matching and spatial aggregation.
- DoorDash engineering blogs discuss dispatch, logistics, and reliability challenges in marketplace delivery.
- Google’s S2 geometry library and H3 are good contrasts for spatial indexing choices.
- Stripe idempotency/payment patterns apply directly to duplicate checkout and refund handling.

## Things to mention / interview tips
- Say “latest courier location is cache-like; order ledger is durable.”
- Use leases for courier assignment so two orders do not claim the same courier simultaneously.
- Model explicit states: placed → accepted → picked_up → delivered/cancelled.
- Discuss surge/peak dinner load and graceful degradation of map refresh rate.

## Common mistakes to call out
- Using SQL radius scans without spatial indexes or cells.
- Treating restaurant acceptance and payment capture as one atomic call.
- Persisting every GPS ping forever in the OLTP database.
- Ignoring cancellation/refund paths.

## Diagrams / visuals to draw on screen
- Marketplace HLD with order, dispatch, payment, tracking services.
- H3/geohash cells around restaurant and couriers.
- Order/delivery state machine with saga compensation.

## Series glue
- Reference Uber, Payments, Saga, and Pub/Sub; forward to Replication/Partitioning and Ledger. CTA: subscribe and get the state-machine diagram in GitHub.
