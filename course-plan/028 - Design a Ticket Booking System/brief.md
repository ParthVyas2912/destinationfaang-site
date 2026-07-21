# Design a Ticket Booking System (Concurrency & Locking)

| | |
|---|---|
| **Publish order** | 028 |
| **Course #** | 106 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~35 min |
| **Primary search keyword** | `design ticketmaster` |
| **Demand** | High |

**Thumbnail text idea:** NO DOUBLE BOOKING
**One-line hook (first 15s):** Two fans click the same seat at the same millisecond—your design either sells it once, or your company refunds angry customers all night.

## Learning objectives
- Model seats, events, holds, orders, payments, and tickets with correct consistency boundaries.
- Use locking, leases, idempotency, and queues to prevent double booking under spikes.
- Estimate traffic for onsale bursts and separate browse load from checkout load.
- Explain fairness, waiting rooms, and failure recovery in a Ticketmaster-style system.

## Topics & items to cover
- **Step 1 — Requirements:** browse events/sections, show live seat map, hold seats for 5 minutes, checkout with payment, issue ticket/QR. Exclude resale and recommendations. Strong consistency for a seat’s final ownership; high availability for browsing.
- **Step 2 — Estimation:** onsale for a stadium: millions waiting, but only stadium-scale seats. Read-heavy seat-map polling; checkout writes are bounded by inventory. Cache event metadata; protect inventory service from fanout.
- **Step 3 — API/Data model:** `GET /events/{id}/seats`, `POST /holds {event_id, seat_ids, idempotency_key}`, `POST /orders`, `POST /payments/callback`. Tables: `Seat(event_id, seat_id, status, version)`, `Hold(hold_id, expires_at)`, `Order`, `Ticket`.
- **Step 4 — HLD:** clients → CDN/API gateway → waiting room → catalog cache → seat inventory service → strongly consistent SQL/kv store; payment async via queue; ticket issuer after payment success.
- **Step 5 — Deep dives:** 1) Seat locking: conditional update `WHERE status='available' AND version=x`, create lease with TTL; expiry worker releases holds. 2) Flash crowd: tokenized waiting room meters checkout QPS and blocks bots. 3) Payment uncertainty: order remains `pending_payment`; idempotent callbacks finalize once.
- **Step 6 — Wrap-up:** trade off perfect seat-map freshness for checkout correctness; name graceful degradation: browsing stale, checkout authoritative.

## Anecdotes & war stories to use
- Ticketmaster’s Taylor Swift onsale problems are a public example of demand, bots, and queueing overwhelming ticketing workflows.
- Stripe’s public idempotency-key API is the clean reference for retry-safe payment/order creation.
- Redis Redlock debates are useful: for seat ownership, prefer database conditional writes or consensus-backed locks over casual cache locks.
- Airline and hotel reservation systems popularized temporary holds because payment and final issuance are not instantaneous.

## Things to mention / interview tips
- Say “the seat inventory row is the source of truth; cache is only advisory.”
- Use lease expiration, not permanent locks, for abandoned carts.
- Separate “best available seat search” from exact seat purchase path.
- Discuss bot/rate limiting as a core requirement, not an afterthought.

## Common mistakes to call out
- Letting the UI seat map decide availability.
- Holding seats in Redis only, then losing locks on failover.
- Charging payment before proving the seat hold exists.
- Ignoring idempotency when clients retry checkout.

## Diagrams / visuals to draw on screen
- State machine: available → held → sold or expired.
- Sequence diagram for hold, payment, ticket issuance.
- Waiting-room token bucket in front of checkout.

## Series glue
- Call back to Rate Limiter, Payment System, and Saga Pattern; next case studies reuse reservation/idempotency ideas. CTA: subscribe and use the GitHub repo templates.
