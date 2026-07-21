# Time-Series Databases & Scalable Counters

| | |
|---|---|
| **Publish order** | 053 |
| **Course #** | 26 |
| **Module** | M03 — Data, Storage & Caching |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `time series database` |
| **Demand** | Moderate |

**Thumbnail text idea:** TIME BUCKETS
**One-line hook (first 15s):** A counter sounds trivial until Black Friday turns ‘increment likes’ into your hottest database row.

## Learning objectives
- Explain metric, tags, timestamp, value, and time-bucketed storage.
- Design scalable counters with sharding, rollups, and compaction.
- Discuss retention, downsampling, cardinality, and clock skew.

## Topics & items to cover
- Hook: one `likes_count` row melts when a celebrity post goes viral.
- Definition: a time-series database optimizes append-heavy measurements and range scans over time.
- Worked example: 1M devices emit CPU every 10s = 100K points/sec. Store `(metric=cpu, tags={device_id,region}, ts, value)`, partition by `series_hash + day`, keep raw 7 days, 1-minute rollups 90 days, hourly rollups 2 years. For viral counters, write to 128 shards `post_id:shard_id`; read sums shards or compact periodically.
- Tradeoffs: great compression/range queries; high-cardinality tags hurt; exact global counters cost more than eventual sharded counters.
- Real-world usage: Prometheus/Thanos, InfluxDB, OpenTSDB, CloudWatch metrics, IoT telemetry.
- Interview sentence: “I’ll avoid a single hot counter by striping writes and serving from pre-aggregated time buckets.”
- Recap: optimize for append + time range, not joins.

## Anecdotes & war stories to use
- Prometheus popularized labels and also warns strongly about high cardinality.
- OpenTSDB on HBase is a classic wide-row time-series design.
- Social platforms use sharded counters because celebrity traffic creates hot keys.

## Things to mention / interview tips
- State retention and resolution requirements.
- Name the partition key.
- Store device timestamp and ingestion timestamp when clocks may skew.

## Common mistakes to call out
- Updating one hot counter row.
- Treating tags as free.
- Keeping raw high-resolution data forever.

## Diagrams / visuals to draw on screen
- Metric/tag/time/value row layout.
- 128-shard counter read/write flow.
- Retention pyramid: raw → minute → hour.

## Series glue
- Connect to analytics rollups; next is IoT telemetry. Subscribe and grab GitHub diagrams.
