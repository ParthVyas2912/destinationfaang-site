# Design a Logistics & Fleet Tracking System

| | |
|---|---|
| **Publish order** | 048 |
| **Course #** | 107 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~30 min |
| **Primary search keyword** | `design fleet tracking` |
| **Demand** | Moderate |

**Thumbnail text idea:** TRACK THE FLEET
**One-line hook (first 15s):** Fleet tracking is not just dots on a map—it is noisy GPS, geofences, ETA, dispatch, offline devices, and millions of location writes.

## Learning objectives
- Design vehicle telemetry ingestion, latest-location reads, history storage, and alerts.
- Use geo indexing for nearby vehicles and geofence detection.
- Handle offline devices, out-of-order GPS pings, and high write volume.
- Separate real-time operational state from analytical trip history.

## Topics & items to cover
- **Step 1 — Requirements:** ingest GPS every few seconds, show live vehicle map, query history/trips, geofence alerts, dispatch nearest driver, device health. Exclude full route optimization unless asked. Low-latency latest location; durable history.
- **Step 2 — Estimation:** 100k vehicles × ping every 5s = 20k writes/sec. Latest reads for dispatch/maps; history append volume large but compressible. Mobile networks cause gaps/out-of-order points.
- **Step 3 — API/Data model:** `POST /telemetry {vehicle_id, lat,lng,ts,speed}`, `GET /vehicles/{id}/location`, `GET /nearby?lat,lng`, `GET /vehicles/{id}/trips`. Stores: LatestLocation, TelemetryEvent, Trip, Geofence.
- **Step 4 — HLD:** device → ingest gateway/MQTT/HTTP → stream processor → latest-location Redis/kv + time-series/object store → geofence alert service → map/API clients.
- **Step 5 — Deep dives:** 1) Geo queries: index latest locations by H3/geohash cell, search neighboring cells. 2) Ordering/noise: accept only newer timestamp for latest; keep raw events for audit; smooth impossible jumps. 3) Geofences: stream processor checks cell candidates and emits enter/exit events with debounce.
- **Step 6 — Wrap-up:** latest location is mutable cache; telemetry history is append-only truth.

## Anecdotes & war stories to use
- Uber’s H3 library is a strong public reference for hexagonal spatial indexing and aggregation.
- Google S2 is another well-known geometry/indexing system used for global spatial cells.
- Kafka/Kinesis-style streams are common for IoT telemetry because ingestion and downstream consumers scale independently.
- MQTT is widely used in IoT/fleet scenarios because devices often operate on unreliable networks.

## Things to mention / interview tips
- Distinguish “where is vehicle now?” from “show me last month’s route.”
- Use device timestamp plus server receive timestamp to handle clock/network issues.
- Add backpressure and sampling if maps cannot consume every ping.
- Mention privacy/data retention for driver location history.

## Common mistakes to call out
- Writing every GPS ping into a relational hot row table.
- Doing radius queries by scanning all vehicles.
- Trusting GPS order and accuracy blindly.
- Forgetting offline buffering and duplicate upload from devices.

## Diagrams / visuals to draw on screen
- Telemetry ingestion pipeline with stream processor and two stores.
- H3/geohash cells around a query point.
- Geofence enter/exit state machine with debounce.

## Series glue
- Reference Uber, Food Delivery dispatch, and Pub/Sub; forward to HyperLogLog and analytics for counting telemetry at scale. CTA: subscribe and use GitHub for schemas and diagrams.
