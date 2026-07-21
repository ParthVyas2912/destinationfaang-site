# How to Choose a Database (Decision Matrix)

| | |
|---|---|
| **Publish order** | 088 |
| **Course #** | 21 |
| **Module** | M03 — Data, Storage & Caching |
| **Type** | concept |
| **Target length** | ~16 min |
| **Primary search keyword** | `how to choose a database` |
| **Demand** | High |

**Thumbnail text idea:** DATABASE MATRIX
**One-line hook (first 15s):** The wrong database choice usually starts with asking “SQL or NoSQL?” instead of “what queries must be fast?”

## Learning objectives
- Choose databases by access pattern, consistency, scale, and operations.
- Compare relational, key-value, document, wide-column, search, graph, time-series, and object storage.
- Build a decision matrix for interview requirements.
- Explain polyglot persistence without overengineering.

## Topics & items to cover
- Hook: profiles, full-text search, metrics, and graph traversals are different problems.
- Definition: database selection maps workload requirements to storage/query models and guarantees.
- Worked example: ecommerce uses Postgres for orders/payments, Redis for carts/sessions, Elasticsearch/OpenSearch for product search, S3 for images, warehouse/lake for analytics.
- How it works: query patterns, transactions, primary keys, secondary indexes, read/write ratio, consistency, replication, partitioning, managed-service maturity.
- Tradeoffs: relational systems give constraints; NoSQL scales specific access paths; search indexes are derived; graph DBs help traversals but add operational specialization.
- Real-world usage: DynamoDB/Cassandra for key access, Postgres/MySQL for OLTP, Elasticsearch for search, BigQuery/Snowflake for analytics.
- Interview sentence: "I’ll start from access patterns and correctness requirements, choose one source of truth, then add derived stores only for specific queries."
- Recap: database choice is workload fit, not brand loyalty.

## Anecdotes & war stories to use
- Amazon Dynamo inspired highly available key-value systems and DynamoDB’s lineage.
- Elasticsearch became common because relational `LIKE` does not replace inverted indexes.
- Postgres gained JSON and extensions, showing relational databases cover more than candidates assume.
- Warehouses like BigQuery/Snowflake separated OLTP from analytics to protect production DBs.

## Things to mention / interview tips
- Ask for top 3 queries and write patterns first.
- Name source of truth and derived indexes.
- Consider backups, migrations, observability, and team familiarity.
- Avoid adding five databases in the first pass.

## Common mistakes to call out
- Choosing NoSQL just because scale is mentioned.
- Using search as source of truth.
- Ignoring transactions for money/order workflows.
- Letting analytical queries crush OLTP stores.

## Diagrams / visuals to draw on screen
- Database decision matrix by workload.
- Ecommerce polyglot persistence map.
- Source-of-truth DB feeding derived stores via events.

## Series glue
- Follows networking protocols by focusing on data storage choices; next covers data formats and compression. CTA: subscribe and use the GitHub matrix.
