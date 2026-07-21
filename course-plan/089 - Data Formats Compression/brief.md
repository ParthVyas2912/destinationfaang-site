# Data Formats & Compression (Protobuf, Avro)

| | |
|---|---|
| **Publish order** | 089 |
| **Course #** | 28 |
| **Module** | M03 — Data, Storage & Caching |
| **Type** | concept |
| **Target length** | ~12 min |
| **Primary search keyword** | `protobuf avro parquet` |
| **Demand** | Moderate |

**Thumbnail text idea:** FORMAT MATTERS
**One-line hook (first 15s):** A data format decision can determine whether your pipeline is evolvable, cheap to scan, or painful forever.

## Learning objectives
- Compare JSON, Protobuf, Avro, Parquet, and compression codecs.
- Explain row-oriented versus columnar storage with query behavior.
- Design schema evolution for streams and analytics files.
- Choose compression by CPU, latency, and storage tradeoffs.

## Topics & items to cover
- Hook: raw JSON analytics events are convenient until every query scans fields it does not need.
- Definition: formats encode records; compression reduces bytes with CPU/latency tradeoffs.
- Worked example: service `GetUser` uses Protobuf; Kafka `OrderCreated` uses Avro with schema registry; warehouse partitions use Parquet so a query for `date,total_cents` skips other columns.
- How it works: schemas, field IDs/names, compatibility, row vs column layout, predicate pushdown, dictionary encoding, Snappy/Zstd/Gzip tradeoffs.
- Tradeoffs: JSON is debuggable but verbose; Protobuf is fast but needs generated code; Avro fits registry-driven streams; Parquet is great for analytics, poor for single-record updates.
- Real-world usage: gRPC/Protobuf, Kafka/Avro, Spark/Parquet, lakehouse tables, log compression.
- Interview sentence: "I’ll choose row formats for transactional messages and columnar Parquet for analytical scans, with compatibility checks in CI."
- Recap: match format to access pattern.

## Anecdotes & war stories to use
- Google created Protocol Buffers for efficient structured data exchange across services.
- Avro became popular in Kafka ecosystems because schemas can live centrally and evolve.
- Parquet emerged from Hadoop/Spark analytics to optimize columnar scans.
- Zstandard adoption grew because it often balances compression strength with practical speed.

## Things to mention / interview tips
- Mention schema registry for event compatibility.
- Explain compression can increase CPU while reducing storage/network.
- Use column pruning and predicate pushdown for Parquet.
- Keep human-readable JSON where debugging matters.

## Common mistakes to call out
- Using Parquet for low-latency point updates.
- Assuming smaller bytes always means faster end-to-end.
- Changing field meanings without schema versioning.
- Compressing already-compressed media files.

## Diagrams / visuals to draw on screen
- Row vs column layout for three fields.
- Event pipeline: Protobuf/Avro to Parquet lake.
- Compression tradeoff curve: size vs CPU.

## Series glue
- Builds on database selection by choosing how bytes are stored and moved; next is backups and disaster recovery. CTA: subscribe and see examples in GitHub.
