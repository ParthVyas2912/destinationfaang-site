# Leader Election & Quorum in Distributed Systems

| | |
|---|---|
| **Publish order** | 071 |
| **Course #** | 55 |
| **Module** | M05 — Microservices & Reliability |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `leader election` |
| **Demand** | Moderate |

**Thumbnail text idea:** ONE LEADER
**One-line hook (first 15s):** If two machines both think they are primary, your system does not get twice as fast — it gets corrupted.

## Learning objectives
- Explain why leader election exists and when leaderless designs are safer.
- Compute quorum for 3-node and 5-node replicated services.
- Describe terms, leases, and fencing tokens that prevent split brain.
- State the availability tradeoff when quorum cannot be reached.

## Topics & items to cover
- Hook: two primaries accept writes after a network partition.
- Definition: leader election chooses one coordinator; quorum requires majority agreement before committing decisions.
- Worked example: in a 5-node metadata cluster, quorum is 3. If A/B are isolated, they reject writes while C/D/E elect a leader.
- How it works: heartbeats, randomized election timeouts, term/epoch numbers, majority votes, commit index, leader lease, fencing token to storage.
- Tradeoffs: CP behavior under partition, election pause, clock-sensitive leases, odd-sized cluster cost.
- Real-world usage: database primaries, Kubernetes etcd, Kafka controller, lock services.
- Interview sentence: "I need majority quorum plus monotonic fencing tokens so an old leader cannot write after a new one is elected."
- Recap: no quorum means no safe writes.

## Anecdotes & war stories to use
- Google Chubby showed how consensus-backed locks simplified distributed systems.
- ZooKeeper became a standard coordination layer in Hadoop-era infrastructure.
- etcd/Raft underpins Kubernetes state; losing etcd quorum becomes a cluster-wide event.
- Split-brain database incidents often come from failover without fencing the old primary.

## Things to mention / interview tips
- Say "majority quorum," not "one replica acknowledged."
- Mention 3 nodes tolerate 1 failure; 5 tolerate 2.
- Pair leases with fencing tokens for external side effects.
- Clarify leader, quorum, and stale-follower read choices.

## Common mistakes to call out
- Treating heartbeat timeout as proof the leader is dead.
- Using two nodes and expecting safe automatic failover.
- Forgetting the old leader may still write externally.
- Optimizing election speed while ignoring correctness.

## Diagrams / visuals to draw on screen
- Five nodes split 2-vs-3 with only majority electing.
- Raft term timeline: follower, candidate, leader, higher-term rejection.
- Fencing-token flow from leader to shared storage.

## Series glue
- Reference earlier consistency and CAP videos; connect forward to stateful/stateless scaling next. CTA: subscribe and grab the GitHub repo diagrams.
