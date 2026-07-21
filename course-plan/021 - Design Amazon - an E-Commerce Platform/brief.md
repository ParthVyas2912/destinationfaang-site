# Design Amazon / an E-Commerce Platform

| | |
|---|---|
| **Publish order** | 021 |
| **Course #** | 98 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~45 min |
| **Primary search keyword** | `design amazon` |
| **Demand** | High |

**Thumbnail text idea:** CART TO DOOR
**One-line hook (first 15s):** Amazon design connects catalog, cart, inventory, payment, and fulfillment without letting one outage take all of commerce down.

## Learning objectives
- Decompose e-commerce into catalog, search, cart, checkout, inventory, payment, and fulfillment.
- Explain consistency choices for carts versus inventory and orders.
- Design checkout with reservations, sagas, and failure recovery.

## Topics & items to cover
- Requirements: browse/search products, product detail, cart, checkout, payment, inventory, order tracking, recommendations optional.
- Estimation: reads dominate browsing; checkout has lower volume but high correctness; peak events create traffic spikes.
- API/Data model: `GET /products/{id}`, `POST /cart/items`, `POST /checkout`, `GET /orders/{id}`; `Product`, `SKU`, `Inventory(sku_id, location_id, available, reserved)`, `Cart(user_id)`, `Order(order_id, state)`; shard catalog by product/SKU, orders by user/order ID.
- High-level design: CDN/cache for product pages, search index for discovery, cart service stores mutable carts, checkout orchestrator reserves inventory, creates order, charges payment, emits fulfillment event.
- Deep dives/bottlenecks: inventory reservation TTL prevents oversell; saga handles payment success but fulfillment failure; search index is eventually consistent with catalog source of truth.
- Wrap-up: carts can be eventually consistent; orders/inventory/payment need controlled state machines.

## Anecdotes & war stories to use
- Amazon's Dynamo paper used shopping-cart availability as a motivating example for always-writable customer experience.
- Prime Day and Black Friday traffic spikes show why read paths and checkout paths need different scaling strategies.
- Marketplace systems often separate product catalog from offers/inventory because many sellers can sell the same item.

## Things to mention / interview tips
- Say: "I separate browse availability from checkout reservation; only reservation is authoritative."
- Use saga steps with compensating actions.
- Mention idempotent checkout requests to avoid duplicate orders.
- Keep search as a derived index, not the source of truth.

## Common mistakes to call out
- Treating cart contents as reserved inventory.
- Calling payment before verifying inventory reservation.
- Making product search hit the primary catalog DB.
- Ignoring retries that create duplicate orders.

## Diagrams / visuals to draw on screen
- Domain decomposition diagram.
- Checkout saga sequence with compensations.
- Inventory reservation state machine.

## Series glue
- Reference Kafka event streams and payment idempotency; point forward to consistency models that explain these choices. CTA: subscribe and use the GitHub repo checklists.
