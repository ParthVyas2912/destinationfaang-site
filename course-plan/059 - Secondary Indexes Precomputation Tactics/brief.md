# Secondary Indexes & Precomputation Tactics

| | |
|---|---|
| **Publish order** | 059 |
| **Course #** | 23 |
| **Module** | M03 — Data, Storage & Caching |
| **Type** | concept |
| **Target length** | ~12 min |
| **Primary search keyword** | `secondary index` |
| **Demand** | Moderate |

**Thumbnail text idea:** PRECOMPUTE IT
**One-line hook (first 15s):** If your query is slow enough, the answer is often: build the read path before the user asks.

## Learning objectives
- Explain secondary indexes, materialized views, denormalized tables, and search indexes.
- Choose precomputation tactics from access patterns.
- Design update, delete, backfill, and staleness handling for derived data.

## Topics & items to cover
- Hook: `WHERE status='open' AND assignee_id=7 ORDER BY created_at` is fast only if data is laid out for it.
- Definition: a secondary index is a derived structure keyed by a non-primary access pattern; precomputation stores answers ahead of reads.
- Worked example: Tasks primary key is `task_id`, but product needs open tasks by assignee. Build index table keyed `assignee_id#status`, sort `created_at#task_id`. On status change, delete old index row and insert new one, in transaction or via outbox. For analytics, materialize daily counts by `team_id,status,day`.
- Tradeoffs: faster reads and predictable latency; more writes, storage, consistency bugs, and backfill complexity.
- Real usage: DynamoDB GSIs, Cassandra query tables, database materialized views, Elasticsearch, feed fanout tables.
- Interview sentence: “I’ll design storage around access patterns; if the primary key can’t serve one, I’ll maintain a secondary index or materialized view with an explicit staleness contract.”
- Recap: every fast read has write-time cost.

## Anecdotes & war stories to use
- DynamoDB pushes engineers to model GSIs around access patterns up front.
- Cassandra query-first modeling is a classic denormalization-at-scale example.
- Search engines are giant secondary indexes maintained from source-of-truth data.

## Things to mention / interview tips
- State the exact query and exact index key.
- Explain update/delete consistency.
- Mention backfills when adding indexes to existing data.

## Common mistakes to call out
- Saying “add an index” without columns/order/cardinality.
- Indexing every possible filter.
- Ignoring dual-write failure modes.

## Diagrams / visuals to draw on screen
- Primary table plus index table.
- Update flow through outbox to index worker.
- Read latency vs write amplification chart.

## Series glue
- Connects Elasticsearch to ETL derived datasets. Subscribe and use GitHub templates.
