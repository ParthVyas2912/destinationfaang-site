# SQL vs NoSQL — When to Use Which (Deep Dive)

| | |
|---|---|
| **Publish order** | 024 |
| **Course #** | 20 |
| **Module** | M03 — Data, Storage & Caching |
| **Type** | concept |
| **Target length** | ~22 min |
| **Primary search keyword** | `sql vs nosql` |
| **Demand** | Very High |

**Thumbnail text idea:** DATA MODEL
**One-line hook (first 15s):** SQL versus NoSQL is not a popularity contest; it is about access patterns, invariants, and scale shape.

## Learning objectives
- Choose SQL or NoSQL from access patterns and invariants.
- Compare relational, key-value, document, wide-column, and graph models.
- Explain tradeoffs in schema, joins, transactions, scaling, and operations.

## Topics & items to cover
- Hook: the wrong database choice is usually not about syntax; it is about forcing the database to answer the wrong questions.
- Definition: SQL systems use relational tables and declarative queries; NoSQL covers non-relational models optimized for specific access patterns or scaling shapes.
- How it works: orders need transactionally consistent `Order`, `Payment`, and `LedgerEntry` rows, so SQL is strong; timeline reads need `user_id -> list of tweet_ids` at massive scale, so a wide-column/key-value projection works.
- Tradeoffs: SQL gives joins, constraints, and ACID transactions; NoSQL gives flexible models and horizontal partitioning but often requires denormalization and app-managed invariants.
- Real-world usage: PostgreSQL/MySQL for payments and admin data; DynamoDB/Cassandra for high-scale key-value/wide-column; MongoDB for document-shaped data; Elasticsearch for search indexes.
- Exact interview sentence: "I start from queries and invariants: if I need multi-row transactions and ad-hoc joins, SQL; if I need predictable key-based access at huge scale, denormalized NoSQL."
- Recap: many real systems use both, with source-of-truth and derived stores.

## Anecdotes & war stories to use
- Instagram scaled early with Postgres plus pragmatic sharding/caching, proving SQL can go far.
- Discord publicly described moving message storage from MongoDB to Cassandra and later ScyllaDB as access patterns and scale changed.
- Amazon DynamoDB reflects Dynamo paper ideas for key-value availability and partitioning.

## Things to mention / interview tips
- Name the exact access patterns before choosing.
- Identify source of truth versus derived index/cache.
- Mention migrations and operational maturity.
- Avoid saying NoSQL means no schema; schemas move into application code.

## Common mistakes to call out
- Choosing NoSQL automatically for "scale".
- Modeling relational transactions in a store with no transaction support.
- Forgetting secondary indexes can be expensive or limited.
- Ignoring query evolution and reporting needs.

## Diagrams / visuals to draw on screen
- Decision matrix: invariants, query shape, scale, schema volatility.
- Same feature modeled relationally and denormalized.
- Polyglot architecture: SQL source, search index, cache.

## Series glue
- Reference web crawler storage choices; point forward to proximity services where geospatial access patterns drive the model. CTA: subscribe and use repo decision worksheets.
