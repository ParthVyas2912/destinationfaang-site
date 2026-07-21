# Database Replication & Partitioning Explained

| | |
|---|---|
| **Publish order** | 035 |
| **Course #** | 10 |
| **Module** | M01 — Scalability Foundations |
| **Type** | concept |
| **Target length** | ~18 min |
| **Primary search keyword** | `database replication` |
| **Demand** | High |

**Thumbnail text idea:** COPY VS SPLIT
**One-line hook (first 15s):** Replication makes copies for availability; partitioning splits data for scale. Mixing those up is one of the fastest ways to lose a system design round.

## Learning objectives
- Explain leader-follower, multi-leader, and leaderless replication.
- Distinguish replication from partitioning/sharding with concrete examples.
- Describe replication lag, read-your-writes, failover, and quorum tradeoffs.
- Combine replicas and partitions in a scalable database design.

## Topics & items to cover
- **Hook:** three database nodes can mean three copies of the same data or three different slices—very different guarantees.
- **Definition:** replication copies data across nodes; partitioning divides data across nodes.
- **Worked example:** Orders table has 900GB. Partition by `merchant_id` into 30 shards (~30GB each). Each shard has one leader and two followers across AZs. Writes route to the shard leader; reads may use followers unless user needs read-after-write, then read leader or use session token.
- **Tradeoffs:** async replication improves latency but risks lag/loss on failover; sync replication improves durability but adds latency. Partitioning scales capacity but complicates joins and transactions.
- **Real-world usage:** MySQL/Postgres read replicas, Cassandra/Dynamo leaderless replication, MongoDB replica sets plus shards.
- **Interview sentence:** “I’ll partition for capacity and replicate each partition for availability.”
- **Recap:** first decide data placement, then decide copy count and consistency.

## Anecdotes & war stories to use
- Amazon Dynamo’s paper popularized leaderless replication, quorums, and hinted handoff for highly available key-value storage.
- Cassandra inherited Dynamo-style replication and Bigtable-like data modeling, making partition key design central.
- GitHub has publicly discussed MySQL availability and failover engineering, useful for leader-follower realities.
- MongoDB’s replica sets and sharded clusters are a clear product example of replication and partitioning as separate axes.

## Things to mention / interview tips
- Use “replication factor” for copies and “partition count” for splits; don’t conflate terms.
- Name the consistency behavior of reads from followers.
- Explain failover: detect leader failure, elect/promote, route traffic, handle split brain.
- Mention per-shard replication, not one global replica after sharding.

## Common mistakes to call out
- Thinking read replicas increase write capacity.
- Ignoring replication lag in user-facing flows.
- Sharding before one primary with replicas is even saturated.
- Assuming multi-leader is easy without conflict resolution.

## Diagrams / visuals to draw on screen
- Matrix: partitions horizontally, replicas vertically.
- Leader-follower write/read path with replication lag.
- Quorum read/write example: R + W > N.

## Series glue
- Connect to Sharding/Rebalancing and Consistency; preview Multi-Region Replication. CTA: subscribe and use the GitHub cheat sheet for terminology.
