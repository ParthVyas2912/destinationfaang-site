# Design Uber — Ride-Hailing System Design

| | |
|---|---|
| **Publish order** | 013 |
| **Course #** | 101 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~45 min |
| **Primary search keyword** | `design uber` |
| **Demand** | Very High |

**Thumbnail text idea:** MATCH RIDES
**One-line hook (first 15s):** Uber's hard problem is matching moving drivers and riders under seconds of latency while prices and locations change.

## Learning objectives
- Model riders, drivers, trips, locations, pricing, and dispatch.
- Design real-time location ingestion and nearby-driver matching.
- Explain consistency boundaries for trip state and payments.

## Topics & items to cover
- Requirements: request ride, track drivers, match driver, ETA, pricing, trip lifecycle, payment, cancellations.
- Estimation: drivers send location every few seconds; matching latency should be seconds; reads/writes are geographically local.
- API/Data model: `POST /rides`, `PATCH /drivers/{id}/location`, `POST /rides/{id}/accept`; `DriverLocation(driver_id, geohash, lat,lng, updated_at)`, `Trip(trip_id, rider_id, driver_id, state, fare)`; shard active locations by geohash/region, trips by `trip_id`.
- High-level design: mobile clients hit regional gateway, location stream updates in-memory geospatial index, dispatch service queries nearby available drivers, trip state machine persists transitions, payment service charges after completion.
- Deep dives/bottlenecks: matching avoids race conditions with driver reservation TTL; ETA uses map/traffic service not straight-line distance; surge pricing aggregates supply/demand by cell and time window.
- Wrap-up: emphasize regional isolation and state machines.

## Anecdotes & war stories to use
- Uber engineering has written extensively about geospatial indexing, dispatch, and moving services toward domain-oriented architectures.
- Ride-hailing systems use marketplace dynamics: supply/demand imbalance directly affects price and user experience.
- Google S2 and geohash-style spatial cells are commonly used in industry to bucket nearby points.

## Things to mention / interview tips
- Say: "Active driver location is ephemeral; trip state is durable and strongly controlled."
- Use geohash/S2 cells plus neighboring cells for nearby search.
- Include idempotent state transitions for accept/cancel/complete.
- Discuss stale location filtering by timestamp.

## Common mistakes to call out
- Scanning all drivers by distance.
- Treating driver acceptance as a simple write without reservation races.
- Ignoring regional partitioning and traffic conditions.
- Letting payment drive the trip state machine.

## Diagrams / visuals to draw on screen
- Location ingestion stream to geospatial index.
- Dispatch sequence: request, reserve, notify, accept, confirm.
- Trip state machine from requested to completed/cancelled.

## Series glue
- Reference video/CDN regional thinking and preview load balancing next. CTA: subscribe and find the geohash diagrams in the GitHub repo.
