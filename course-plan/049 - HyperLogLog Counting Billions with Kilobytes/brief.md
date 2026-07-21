# HyperLogLog: Counting Billions with Kilobytes

| | |
|---|---|
| **Publish order** | 049 |
| **Course #** | 25 |
| **Module** | M03 — Data, Storage & Caching |
| **Type** | concept |
| **Target length** | ~12 min |
| **Primary search keyword** | `hyperloglog` |
| **Demand** | Moderate |

**Thumbnail text idea:** BILLIONS, KILOBYTES
**One-line hook (first 15s):** What if I told you Redis can count roughly a billion unique users without storing a billion user IDs?

## Learning objectives
- Explain HyperLogLog as probabilistic cardinality estimation, not membership testing.
- Choose approximate distinct counts for analytics, ad reach, and unique visitors.
- Describe hashing, registers, mergeability, and where approximation is unsafe.

## Topics & items to cover
- Hook: exact `COUNT(DISTINCT user_id)` requires storing or sorting huge sets; HLL stores a fixed-size sketch.
- Definition: HyperLogLog estimates cardinality by hashing each value and recording rare leading-zero patterns across registers.
- Worked example: hash 100M impression user IDs; first bits choose one of 16K registers, remaining bits count leading zeros. A register seeing 17 leading zeros implies a rare event and a large population. Merge `us-east` and `us-west` by taking max per register; no raw IDs replayed.
- Tradeoffs: tiny memory, mergeable, fast; approximate, no deletion, no member listing, depends on good hashes.
- Real-world usage: Redis `PFADD/PFCOUNT/PFMERGE`, Presto/BigQuery approximate distincts, ad reach, unique visitors.
- Interview sentence: “I’d use HyperLogLog for approximate distinct cardinality because the sketch is fixed-size and mergeable, but not for billing or compliance.”
- Recap: exact set for correctness; HLL for cheap, scalable estimates.

## Anecdotes & war stories to use
- Philippe Flajolet’s HyperLogLog paper refined earlier LogLog counting into a practical sketch.
- Redis made HLL accessible with simple `PF*` commands.
- Ad-tech reach reports often rely on sketches because cross-shard exact user sets are expensive and privacy-sensitive.

## Things to mention / interview tips
- Use the words “cardinality,” “mergeable sketch,” and “bounded approximation.”
- Say duplicates collapse because identical IDs hash to the same pattern.
- Validate sketches periodically against exact counts on samples.

## Common mistakes to call out
- Confusing HLL with a Bloom filter.
- Using it when deletes or exact membership are required.
- Reporting approximate numbers as billing truth.

## Diagrams / visuals to draw on screen
- ID → hash → register index → leading-zero count.
- Two sketches merging with per-register max.
- Cost curve: exact set vs bitmap vs HLL.

## Series glue
- Reference earlier storage tradeoff videos; next, apply approximate analytics to dashboards. Subscribe and grab the GitHub repo.
