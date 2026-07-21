# Schema Management & API Versioning

| | |
|---|---|
| **Publish order** | 075 |
| **Course #** | 50 |
| **Module** | M05 — Microservices & Reliability |
| **Type** | concept |
| **Target length** | ~12 min |
| **Primary search keyword** | `api versioning` |
| **Demand** | Moderate |

**Thumbnail text idea:** DON'T BREAK API
**One-line hook (first 15s):** A perfect new API version is useless if yesterday’s mobile app crashes the moment you deploy it.

## Learning objectives
- Compare URL, header, and schema-evolution versioning.
- Design backward-compatible changes for REST, gRPC, and streams.
- Explain consumer-driven contracts and deprecation windows.
- Avoid breaking mobile, partner, and async consumers.

## Topics & items to cover
- Hook: mobile clients update slowly; servers must support old request shapes.
- Definition: API versioning and schema management let producers evolve without breaking consumers.
- Worked example: `OrderCreated` v1 has `order_id` and `total_cents`; v2 adds optional `currency` and `items[]`. Old consumers ignore new fields; new ones default missing currency.
- How it works: additive fields, reserved Protobuf numbers, Avro compatibility checks, endpoint routing, contract tests, deprecation telemetry.
- Tradeoffs: many versions increase maintenance; forced migrations break clients; strict schemas catch errors but slow evolution.
- Real-world usage: Stripe API version pinning, Confluent Schema Registry, GraphQL deprecation, Protobuf/gRPC.
- Interview sentence: "I’ll prefer additive compatible changes, automate compatibility checks in CI, and track per-consumer adoption before removing fields."
- Recap: versioning is an operational lifecycle, not a URL suffix.

## Anecdotes & war stories to use
- Stripe is known for pinning API behavior by account/version to avoid surprising integrations.
- Protobuf reserved tags exist because reusing field numbers can corrupt interpretation.
- Confluent Schema Registry popularized compatibility gates for Kafka producers.
- GraphQL’s deprecate-in-place model shows why removing fields is harder than adding them.

## Things to mention / interview tips
- Say "additive changes are safe; renames and type changes are not."
- Mention unknown-field handling for Protobuf and JSON clients.
- Include producer and consumer contract tests.
- Track traffic by version before deletion.

## Common mistakes to call out
- Creating `/v2` for every optional field.
- Renaming event fields without a compatibility plan.
- Assuming all clients deploy together.
- Forgetting async consumers replay old events.

## Diagrams / visuals to draw on screen
- Timeline: v1, additive v2, dual support, deprecation, removal.
- Event schema evolution with optional field and default.
- CI gate calling schema registry compatibility check.

## Series glue
- Builds on service communication and discovery; next applies evolution pressure to multi-tenant SaaS. CTA: subscribe and see sample schemas in GitHub.
