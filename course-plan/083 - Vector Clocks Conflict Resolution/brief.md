# Vector Clocks & Conflict Resolution

| | |
|---|---|
| **Publish order** | 083 |
| **Course #** | 7 |
| **Module** | M01 — Scalability Foundations |
| **Type** | concept |
| **Target length** | ~12 min |
| **Primary search keyword** | `vector clocks` |
| **Demand** | Moderate |

**Thumbnail text idea:** WHO WON?
**One-line hook (first 15s):** When two replicas both accept writes offline, a timestamp cannot always tell you which update should survive.

## Learning objectives
- Explain vector clocks and why wall-clock timestamps are insufficient.
- Detect concurrent writes versus causally ordered writes.
- Choose conflict strategies for carts, documents, and profiles.
- State when CRDTs or app merges beat last-write-wins.

## Topics & items to cover
- Hook: Alice updates a cart on her phone while Bob updates it on the web; both replicas later sync.
- Definition: a vector clock records each replica’s known update counter to compare causality.
- Worked example: A writes `{A:1,B:0}`; B independently writes `{A:0,B:1}`. Neither dominates, so writes are concurrent. Later `{A:2,B:1}` dominates both.
- How it works: increment local counter, attach vector to object, compare component-wise, store siblings, merge or prompt user, compact vectors.
- Tradeoffs: preserves concurrency but metadata grows; resolution moves to application logic; LWW is simple but loses data.
- Real-world usage: Dynamo/Riak sibling versions, distributed document sync, shopping carts, CRDT collaboration.
- Interview sentence: "I’ll use version vectors to detect concurrent updates, then resolve with domain-specific merge instead of trusting wall-clock time."
- Recap: vector clocks answer "happened before?" not "what is semantically correct?"

## Anecdotes & war stories to use
- Amazon Dynamo used vector clocks to expose conflicting object versions to applications.
- Riak made "siblings" visible when conflicts could not be automatically resolved.
- Collaborative editing systems inspired CRDT/OT because concurrent edits are normal.
- Clock-skew bugs across distributed systems show why physical time alone is dangerous.

## Things to mention / interview tips
- Use "dominates" and "concurrent" precisely.
- Give domain merges: cart union, field precedence, document CRDT.
- Mention metadata cleanup for many writers.
- Clarify whether users can tolerate surfaced conflicts.

## Common mistakes to call out
- Saying latest timestamp always wins.
- Thinking vector clocks resolve conflicts automatically.
- Forgetting deletes need tombstones or versioning.
- Letting vector metadata grow unbounded.

## Diagrams / visuals to draw on screen
- Two-replica timeline with concurrent vectors.
- Component-wise vector comparison table.
- Conflict flow: detect, store siblings, merge, write new vector.

## Series glue
- Builds on consistency/tradeoff videos; next covers connection pooling, a practical scaling bottleneck. CTA: subscribe and use repo examples.
