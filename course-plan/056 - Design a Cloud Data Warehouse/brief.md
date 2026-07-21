# Design a Cloud Data Warehouse (Snowflake-Style)

| | |
|---|---|
| **Publish order** | 056 |
| **Course #** | 109 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~30 min |
| **Primary search keyword** | `design data warehouse` |
| **Demand** | Moderate |

**Thumbnail text idea:** WAREHOUSE DESIGN
**One-line hook (first 15s):** Snowflake’s magic idea is separating storage from compute—let’s design why that matters.

## Learning objectives
- Design a cloud data warehouse for SQL analytics over large data.
- Separate ingestion, object storage, metadata, compute, and query planning.
- Explain columnar files, pruning, caching, isolation, governance, and cost controls.

## Topics & items to cover
- Requirements: ingest batch/streaming data, run BI SQL, isolate finance/marketing workloads, retain years of data, enforce RBAC/audit.
- Estimation: petabytes stored, tens of TB/day ingest, 1K analysts. Immutable columnar files partitioned by table/date; micro-partition metadata stores min/max stats for pruning.
- API/Data model: `CREATE TABLE`, `COPY INTO`, `SELECT`, `CREATE WAREHOUSE`; entities: Table, MicroPartition, Catalog, WarehouseCluster, Query, Role.
- High-level design: ingestion writes columnar files to object storage; catalog tracks schema/stats; coordinator plans SQL; elastic compute warehouses read columns, shuffle joins, cache hot data; result cache serves repeated BI queries.
- Deep dives/bottlenecks: small-file compaction after streaming; workload isolation with separate virtual warehouses; optimizer uses column pruning, predicate pushdown, and stats.
- Wrap-up: object storage is durable truth; compute is disposable and independently scalable.

## Anecdotes & war stories to use
- Snowflake popularized independent storage/compute scaling.
- BigQuery showed serverless columnar analytics can hide cluster management.
- The move from HDFS clusters to object-storage lakehouses explains immutable columnar files.

## Things to mention / interview tips
- Say “metadata is the control plane.”
- Include auto-suspend, query limits, and workload queues.
- Explain why OLTP row stores are wrong for BI scans.

## Common mistakes to call out
- Coupling every query to one shared cluster.
- Ignoring small-file problems.
- Forgetting permissions and audit logs.

## Diagrams / visuals to draw on screen
- Storage, metadata, and multiple compute warehouses.
- Query reading only selected columns/partitions.
- Ingest → compact → optimize lifecycle.

## Series glue
- Connects analytics platforms and ETL. Next: cache write policies. Subscribe and use GitHub diagrams.
