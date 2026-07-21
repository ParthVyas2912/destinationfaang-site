# Design a Real-Time Analytics Dashboard

| | |
|---|---|
| **Publish order** | 050 |
| **Course #** | 111 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~30 min |
| **Primary search keyword** | `design analytics dashboard` |
| **Demand** | Moderate |

**Thumbnail text idea:** LIVE METRICS
**One-line hook (first 15s):** Let’s design the dashboard a CEO opens during a launch and asks: are signups broken right now?

## Learning objectives
- Convert “real-time dashboard” into freshness, query, and correctness requirements.
- Design ingestion, aggregation, hot storage, and browser push updates.
- Explain hot-tenant isolation, late events, and dashboard query fanout.

## Topics & items to cover
- Requirements: track `signup`, `checkout`, `api_error`; p50 freshness under 5s; 30-day lookback; multi-tenant RBAC; approximate live numbers acceptable.
- Estimation: 50K events/sec peak, 1KB/event, billions/day. Roll up by `tenant_id + metric_id + dimensions_hash + minute_bucket`; partition Kafka by `tenant_id:metric_id`.
- API/Data model: `POST /v1/events`, `GET /dashboards/{id}/tiles`, `WS /dashboards/{id}/stream`; entities: Tenant, Event, MetricDefinition, Tile, Rollup.
- High-level design: SDK/API gateway → Kafka/Pulsar → stream processor → hot OLAP store/Redis latest buckets → dashboard API → WebSocket/SSE. Raw events land in object storage for replay.
- Deep dives/bottlenecks: hot tenants need quotas and key salting; late events need watermark plus correction deltas; browser fanout needs tile cache/precomputed rollups, not direct OLAP queries per tab.
- Wrap-up: live view can be approximate; batch replay reconciles truth.

## Anecdotes & war stories to use
- LinkedIn’s Pinot was built for low-latency user-facing analytics.
- Apache Druid’s Metamarkets origin is a classic interactive event analytics story.
- Lambda Architecture debates show why teams split fast approximate views from corrected batch views.

## Things to mention / interview tips
- Ask “does real time mean 1s, 5s, or 1 minute?”
- Name the rollup key explicitly.
- Keep historical queries HTTP/cacheable; use WebSocket only for deltas.

## Common mistakes to call out
- Querying raw events for every chart refresh.
- Ignoring duplicate/late mobile events.
- Partitioning only by metric and creating noisy neighbors.

## Diagrams / visuals to draw on screen
- SDK → stream → rollup → dashboard pipeline.
- Rollup table keyed by tenant/metric/dimension/time.
- WebSocket delta fanout with cache.

## Series glue
- Builds on HyperLogLog and caching concepts. Next: Elasticsearch fundamentals. Subscribe and use the GitHub repo.
