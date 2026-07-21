# RDBMS Internals: Indexes, B-Trees & ACID

| | |
|---|---|
| **Publish order** | 045 |
| **Course #** | 19 |
| **Module** | M03 — Data, Storage & Caching |
| **Type** | concept |
| **Target length** | ~20 min |
| **Primary search keyword** | `database indexing` |
| **Demand** | High |

**Thumbnail text idea:** B-TREE TO ACID
**One-line hook (first 15s):** Indexes are not magic lookup tables—every faster read is paid for with writes, pages, locks, and transaction guarantees under the hood.

## Learning objectives
- Explain B-tree/B+tree indexes, page reads, composite indexes, and covering indexes.
- Describe ACID properties with practical database mechanisms.
- Connect indexes to query plans, write amplification, and locking.
- Use interview examples to choose correct indexes for access patterns.

## Topics & items to cover
- **Hook:** `WHERE user_id=42 ORDER BY created_at DESC LIMIT 20` is either milliseconds or a table scan depending on one index.
- **Definition:** an index is an auxiliary data structure, commonly a B+tree, that keeps sorted keys pointing to rows/pages so queries avoid scanning everything.
- **Worked example:** 100M orders. Composite index `(user_id, created_at DESC)` lets the DB seek to user 42 and read the newest 20 entries. Index `(created_at, user_id)` is wrong for this query because the leftmost prefix is time, not user.
- **Tradeoffs:** indexes speed reads and constraints but slow writes, consume storage, and can cause lock/contention. ACID uses WAL/redo logs for durability, locks/MVCC for isolation, and constraints/transactions for consistency.
- **Real-world usage:** Postgres/MySQL OLTP, InnoDB clustered primary keys, secondary indexes, transaction logs.
- **Interview sentence:** “I’ll design indexes from the exact query shape, especially equality filters before range/order columns.”
- **Recap:** database internals explain why schema design is performance design.

## Anecdotes & war stories to use
- InnoDB’s clustered primary key design is a classic example: secondary indexes point through the primary key, so PK choice matters.
- PostgreSQL’s MVCC vacuum behavior is a real operational story for long transactions and table bloat.
- The ARIES recovery algorithm is foundational for write-ahead logging and crash recovery in relational databases.
- GitHub and many large Rails/MySQL apps have public stories about online schema changes and index creation risk.

## Things to mention / interview tips
- Say “leftmost prefix” for composite B-tree indexes.
- Explain read committed vs serializable only as deep as needed.
- Mention `EXPLAIN`/query plans as the validation tool.
- For pagination, prefer seek pagination over large offset scans.

## Common mistakes to call out
- Adding indexes to every column without write/storage cost.
- Thinking indexes help low-selectivity boolean columns by default.
- Confusing durability with availability.
- Ignoring transaction isolation anomalies like lost update or phantom reads.

## Diagrams / visuals to draw on screen
- B+tree root/internal/leaf pages pointing to rows.
- Composite index ordering example for orders query.
- WAL commit path: write log, flush, then data pages later.

## Series glue
- Connect to SQL vs NoSQL and Replication; next API Gateway moves from storage internals to traffic control. CTA: subscribe and get index examples in GitHub.
