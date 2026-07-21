# Consistent Hashing — The #1 Concept Interviewers Love

| | |
|---|---|
| **Publish order** | 007 |
| **Course #** | 11 |
| **Module** | M01 — Scalability Foundations |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `consistent hashing` |
| **Demand** | Very High |

**Thumbnail text idea:** HASH RINGS
**One-line hook (first 15s):** If one cache node dies, should 25% of keys move or almost all of them? That is why consistent hashing exists.

## Learning objectives
- Explain why normal modulo hashing causes massive key movement.
- Use a hash ring with virtual nodes and replicas.
- Apply consistent hashing to caches, databases, and stream partitions.

## Topics & items to cover
- Hook: cache node 3 dies; with `hash(key) % N`, most keys remap and the database melts.
- Definition: consistent hashing maps both keys and servers onto a ring so only neighboring key ranges move when membership changes.
- How it works: hash `user:42` to position 730; walk clockwise to the first virtual node, say cache B. With 4 caches and 100 virtual nodes each, adding cache E should move roughly 20% of keys, not nearly everything.
- Tradeoffs: virtual nodes smooth imbalance; replication improves availability; membership changes need gossip/config propagation; hot keys still need separate mitigation.
- Real-world usage: Dynamo-style systems, Cassandra token ranges, CDN/cache clusters, and sharded key-value stores.
- Exact interview sentence: "I would use consistent hashing with virtual nodes so adding or removing a node only remaps a bounded fraction of keys."
- Recap: consistent hashing solves rebalancing pain, not hot-key or consistency problems by itself.

## Anecdotes & war stories to use
- Amazon's Dynamo paper made consistent hashing central to highly available key-value storage.
- Cassandra uses token ranges inspired by Dynamo-style partitioning, with operational work around rebalancing and repair.
- Memcached/Redis client libraries often use consistent hashing so cache expansion does not invalidate the whole fleet.

## Things to mention / interview tips
- Draw the ring; interviewers love seeing key movement visually.
- Mention virtual nodes before the interviewer asks about uneven machines.
- Separate partitioning from replication and quorum consistency.
- Say what happens during node failure and recovery.

## Common mistakes to call out
- Saying consistent hashing means no keys move.
- Ignoring virtual nodes and ending with uneven load.
- Using it to solve celebrity hot keys.
- Forgetting clients/services need the same membership view.

## Diagrams / visuals to draw on screen
- Ring with servers, virtual nodes, and sample keys.
- Before/after adding a node with only adjacent ranges moving.
- Replicas on next clockwise nodes.

## Series glue
- Reference URL shortener sharding and Twitter timeline caches; point forward to Instagram media/feed storage. CTA: subscribe and check the GitHub repo for ring diagrams.
