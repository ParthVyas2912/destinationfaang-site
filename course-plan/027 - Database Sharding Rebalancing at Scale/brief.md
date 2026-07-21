# Database Sharding & Rebalancing at Scale

| | |
|---|---|
| **Publish order** | 027 |
| **Course #** | 22 |
| **Module** | M03 — Data, Storage & Caching |
| **Type** | concept |
| **Target length** | ~18 min |
| **Primary search keyword** | `database sharding` |
| **Demand** | High |

**Thumbnail text idea:** SHARD OR DIE
**One-line hook (first 15s):** If one database can’t hold your users anymore, the interview is really asking: what key do you split on, and how do you move data without taking the app down?

## Learning objectives
- Choose range, hash, directory, and geo sharding strategies for a concrete workload.
- Explain virtual shards, consistent hashing, and online rebalancing without downtime.
- Spot hot partitions and pick mitigation: split, replicate, cache, or change the key.
- Describe how queries, indexes, and transactions change after sharding.

## Topics & items to cover
- **Hook:** a single `users` table works until one tenant, celebrity, or region dominates the box.
- **Definition:** sharding horizontally partitions rows across database nodes by a shard key.
- **Worked example:** 200M users, 2KB profile rows = ~400GB before indexes. Use 4096 virtual shards mapped to 16 physical nodes. `hash(user_id) % 4096` chooses a virtual shard; a lookup table maps virtual shard → node. To add 4 nodes, move selected virtual shards, dual-read during copy, then flip ownership.
- **Tradeoffs:** hash sharding balances writes but hurts range queries; range sharding helps scans but creates hot new ranges; directory sharding is flexible but the directory becomes critical infrastructure.
- **Real-world usage:** user timelines, order tables by merchant, chat messages by conversation, geo data by H3/S2 cell.
- **Interview sentence:** “I’ll start with virtual shards so the logical partition count is stable even when physical nodes change.”
- **Recap:** shard key choice is an access-pattern decision, not just a storage decision.

## Anecdotes & war stories to use
- Discord publicly described moving message storage from MongoDB to Cassandra, then later to ScyllaDB, with partition design around channel/message access patterns.
- Instagram engineering has discussed sharding Postgres early with IDs that carried shard information to keep routing simple.
- Vitess came from YouTube’s need to shard MySQL while preserving operational control over tablets and resharding.
- MongoDB chunk migration is a useful caution: automatic balancing helps, but bad shard keys still create jumbo chunks and hotspots.

## Things to mention / interview tips
- Say the exact query first: “get user by id” and “list orders for merchant” imply different keys.
- Mention cross-shard joins become application-level fanout or denormalized read models.
- Add a shard map cache with strongly consistent updates and safe fallback.
- Explain rebalancing as copy, verify, dual-write/redirect, cutover, cleanup.

## Common mistakes to call out
- Sharding by auto-increment ID and putting all fresh writes on the last shard.
- Ignoring secondary indexes that now need local plus global index strategy.
- Assuming distributed transactions remain cheap after splitting data.
- Rebalancing by “just moving rows” without dual-write and verification.

## Diagrams / visuals to draw on screen
- Logical virtual shards mapped many-to-one onto physical database nodes.
- Rebalancing timeline: snapshot copy → change stream catch-up → ownership flip.
- Hot-key heatmap showing one shard overloaded.

## Series glue
- Reference Consistent Hashing and SQL vs NoSQL from earlier videos; tease Multi-Region Database Replication next. CTA: subscribe and grab the GitHub diagrams/checklists.
