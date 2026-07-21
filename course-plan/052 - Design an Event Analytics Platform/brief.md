# Design an Event Analytics Platform (Mixpanel-Style)

| | |
|---|---|
| **Publish order** | 052 |
| **Course #** | 110 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~30 min |
| **Primary search keyword** | `design analytics platform` |
| **Demand** | Moderate |

**Thumbnail text idea:** MIXPANEL DESIGN
**One-line hook (first 15s):** Mixpanel looks simple—track events, draw funnels—but the hard part is answering arbitrary product questions fast.

## Learning objectives
- Design event analytics for funnels, cohorts, retention, and segmentation.
- Model events, users, properties, and identity merges.
- Choose raw storage, columnar OLAP, and pre-aggregation paths.

## Topics & items to cover
- Requirements: SDK ingest, funnel queries like signup→invite→purchase, retention cohorts, 30-90 day hot queries, tenant isolation, raw export.
- Estimation: hundreds of billions of events/month; partition raw by `tenant_id + event_date`, cluster by `event_name` and `user_id`.
- API/Data model: `POST /track`, `POST /identify`, `GET /query/funnel`; entities: Project, Event, UserProfile, IdentityGraph, Cohort, QueryJob. Event has `event_id`, `distinct_id`, `timestamp`, `properties`.
- High-level design: SDK → ingest API → Kafka → validation/enrichment → object storage + columnar OLAP (ClickHouse/Druid/BigQuery-style) → query planner/cache → UI. Offline jobs build cohort tables.
- Deep dives/bottlenecks: anonymous-to-known identity merge via mapping table; high-cardinality properties with dictionaries/limits; funnel queries scan sorted `user_id,timestamp` data plus cached popular segments.
- Wrap-up: immutable event log enables replay; serving layer optimizes common product questions.

## Anecdotes & war stories to use
- Segment popularized separating event collection from downstream tools.
- Mixpanel and Amplitude made funnel/retention queries core product analytics workflows.
- ClickHouse is widely used for fast columnar event analytics.

## Things to mention / interview tips
- Ask whether queries are interactive or async.
- Use `event_id` for dedupe.
- Say “schema-on-write for reserved fields, schema-on-read for custom properties.”

## Common mistakes to call out
- Storing only arbitrary JSON in a row store.
- Ignoring anonymous user merges.
- Indexing every custom property without guardrails.

## Diagrams / visuals to draw on screen
- Track/identify ingestion pipeline.
- Per-user funnel timeline.
- Hot OLAP plus cold object-storage replay path.

## Series glue
- Builds on dashboards/search. Next: time-series DBs and counters. Subscribe and use the GitHub repo.
