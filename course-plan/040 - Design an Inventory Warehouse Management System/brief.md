# Design an Inventory & Warehouse Management System

| | |
|---|---|
| **Publish order** | 040 |
| **Course #** | 105 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~30 min |
| **Primary search keyword** | `design inventory system` |
| **Demand** | Moderate |

**Thumbnail text idea:** STOCK IS TRUTH
**One-line hook (first 15s):** Inventory design sounds like CRUD until Black Friday: now every warehouse, cart, reservation, return, and oversell bug is fighting for the same SKU count.

## Learning objectives
- Model SKU, warehouse, inventory lot, reservation, allocation, shipment, and adjustment.
- Design reservation/commit/release flows that prevent oversell.
- Handle multi-warehouse availability, replenishment, and event-driven updates.
- Explain consistency tradeoffs between browse availability and checkout truth.

## Topics & items to cover
- **Step 1 — Requirements:** show available stock, reserve on checkout, allocate from warehouse, decrement on shipment, handle returns/adjustments, audit changes. Exclude route optimization. Strong consistency per SKU-location reservation.
- **Step 2 — Estimation:** read-heavy product availability; write spikes during sales. Hot SKUs dominate. Warehouse integrations may be delayed and event-driven.
- **Step 3 — API/Data model:** `GET /inventory?sku&zip`, `POST /reservations`, `POST /reservations/{id}/commit`, `POST /adjustments`. Tables: `Inventory(sku, warehouse_id, on_hand, reserved, version)`, Reservation, StockMovement, Warehouse.
- **Step 4 — HLD:** catalog → availability service/cache → inventory service with SQL conditional updates → reservation expiry worker → warehouse management integrations → event stream for search/order updates.
- **Step 5 — Deep dives:** 1) Oversell prevention: `available=on_hand-reserved`; conditional update with version per SKU-warehouse. 2) Allocation: choose nearest warehouse with available stock, split shipments if needed. 3) Reconciliation: warehouse counts/returns generate stock movements and exception reports.
- **Step 6 — Wrap-up:** availability shown to shoppers can be approximate; reservation path must be authoritative.

## Anecdotes & war stories to use
- Amazon’s retail systems are the archetype for separating catalog browsing from fulfillment/inventory truth.
- Shopify and commerce platforms commonly expose inventory levels per location, reflecting real multi-warehouse complexity.
- Ticketing/airline reservation patterns map directly to inventory holds with TTLs.
- Event-sourcing examples are useful because stock movements form an audit log much like a ledger.

## Things to mention / interview tips
- Use “stock movement ledger” phrasing: adjustments are events, not silent count edits.
- Name the consistency boundary: SKU + warehouse row.
- Add reservation expiration so abandoned carts release stock.
- Discuss hot SKU mitigation: queue, per-SKU serialization, or bounded oversell rules.

## Common mistakes to call out
- Updating `available_count` directly from multiple services.
- Reserving inventory only after payment capture.
- Ignoring returns, damaged goods, and manual adjustments.
- Serving cached availability as checkout truth.

## Diagrams / visuals to draw on screen
- Inventory state: on_hand, reserved, available, committed.
- Checkout reservation sequence with TTL expiry.
- Multi-warehouse allocation map/table.

## Series glue
- Reference Ticket Booking, Cache Stampede, and Ledger; next Pub/Sub explains how warehouse events fan out. CTA: subscribe and use GitHub schemas.
