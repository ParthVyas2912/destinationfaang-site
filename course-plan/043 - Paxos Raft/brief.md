# Paxos & Raft — Distributed Consensus Explained

| | |
|---|---|
| **Publish order** | 043 |
| **Course #** | 54 |
| **Module** | M05 — Microservices & Reliability |
| **Type** | concept |
| **Target length** | ~20 min |
| **Primary search keyword** | `raft consensus` |
| **Demand** | High |

**Thumbnail text idea:** CONSENSUS CLEAR
**One-line hook (first 15s):** Consensus is how a cluster chooses one truth even while machines crash, messages delay, and everyone is tempted to become leader.

## Learning objectives
- Explain why consensus is needed for leader election and replicated logs.
- Describe Raft terms: leader, follower, candidate, term, log index, commit index.
- Compare Paxos and Raft at interview depth without drowning in proofs.
- Apply quorum reasoning to configuration, locks, and metadata services.

## Topics & items to cover
- **Hook:** if two schedulers both believe they are leader, they can run the same job twice.
- **Definition:** consensus lets distributed nodes agree on a value or ordered log despite failures, as long as a quorum can communicate.
- **Worked example:** 5-node Raft cluster. Leader appends `set owner=worker7` at log index 42. Once 3 of 5 nodes persist it, entry is committed. If leader dies, a candidate with the most up-to-date log wins election from a majority, preserving committed entries.
- **Tradeoffs:** strong coordination is simple for clients but adds latency and reduced availability during partitions. Use consensus for metadata/control planes, not every high-volume data write.
- **Real-world usage:** etcd and Consul use Raft; ZooKeeper uses Zab; Spanner uses Paxos-family replication with TrueTime for transactions.
- **Interview sentence:** “I’ll put small critical metadata behind a quorum system, but keep bulk data paths partitioned and asynchronous.”
- **Recap:** consensus buys one agreed log at the cost of quorum latency.

## Anecdotes & war stories to use
- The Raft paper was designed for understandability compared with Paxos and is used by etcd, Consul, and many databases.
- Paxos is associated with Leslie Lamport and underpins many production replicated systems despite being famously hard to explain.
- Google Spanner combines Paxos replication with TrueTime to provide externally consistent distributed transactions.
- ZooKeeper/Chubby-style systems show consensus is often the hidden backbone of leader election and distributed locks.

## Things to mention / interview tips
- Use quorum math: majority of 5 is 3; losing 2 nodes still works, losing 3 does not.
- Say what data belongs in consensus: config, leadership, small metadata.
- Mention fencing tokens for locks so old leaders cannot keep writing.
- Avoid claiming consensus solves high-volume data scaling by itself.

## Common mistakes to call out
- Treating Raft as just heartbeats without the replicated log.
- Allowing split brain by accepting writes without majority.
- Using Redis locks for correctness that needs fencing/quorum.
- Forgetting network partitions are not the same as node crashes.

## Diagrams / visuals to draw on screen
- Raft election timeline with terms and votes.
- Log replication: leader appends, followers ack, majority commit.
- Majority quorum overlap diagram.

## Series glue
- Builds on Job Scheduler and Consistency; next Multi-Region Replication shows where consensus gets expensive across distance. CTA: subscribe and get Raft visuals on GitHub.
