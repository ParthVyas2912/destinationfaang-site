# Write-Through vs Write-Back Caching

| | |
|---|---|
| **Publish order** | 057 |
| **Course #** | 33 |
| **Module** | M03 — Data, Storage & Caching |
| **Type** | concept |
| **Target length** | ~12 min |
| **Primary search keyword** | `write through vs write back` |
| **Demand** | Moderate |

**Thumbnail text idea:** CACHE WRITES
**One-line hook (first 15s):** A cache can make reads fast—but the write policy decides whether your data disappears during a crash.

## Learning objectives
- Compare write-through, write-around, write-back, and cache-aside writes.
- Choose a policy for catalogs, counters, sessions, and money-like state.
- Explain durability, latency, consistency, queues, retries, and recovery.

## Topics & items to cover
- Hook: same Redis cache, different correctness depending on write path.
- Definition: write-through synchronously updates cache and database; write-back updates cache first and flushes later.
- Worked example: product price update must be durable, so write DB then update/purge cache or use write-through. Page-view counter can use write-back: increment Redis shard, flush every few seconds to Cassandra/S3. If Redis dies before flush, increments vanish unless a durable log/AOF/replication captures them.
- Tradeoffs: write-through has higher latency and simpler recovery; write-back batches writes but risks data loss and replay complexity; write-around avoids polluting cache but causes cold first reads.
- Real usage: CPU caches, Redis-backed counters, app cache-aside patterns.
- Interview sentence: “For durable user state I won’t acknowledge until the DB or durable log has the write; for high-volume counters I may use write-back with bounded loss and reconciliation.”
- Recap: pick write policy from correctness first, latency second.

## Anecdotes & war stories to use
- Write-ahead logs exist because acknowledging before durable storage is dangerous.
- Redis RDB/AOF modes illustrate durability versus throughput.
- Social counters tolerate eventual consistency; account balances cannot.

## Things to mention / interview tips
- Ask “can we lose this write?” early.
- Name the source of truth.
- Use idempotent flush records and version numbers.

## Common mistakes to call out
- Using write-back for money or inventory.
- Dual-writing cache and DB without failure handling.
- Forgetting read-your-writes expectations.

## Diagrams / visuals to draw on screen
- Write-through vs write-back sequence.
- Crash window before async flush.
- Policy matrix: latency/durability/complexity.

## Series glue
- Follows layered caching and prepares for feature flags. Subscribe and see GitHub examples.
