# Search Architecture: Elasticsearch Fundamentals

| | |
|---|---|
| **Publish order** | 051 |
| **Course #** | 27 |
| **Module** | M03 — Data, Storage & Caching |
| **Type** | concept |
| **Target length** | ~18 min |
| **Primary search keyword** | `elasticsearch system design` |
| **Demand** | High |

**Thumbnail text idea:** SEARCH THAT SCALES
**One-line hook (first 15s):** When a user types ‘wireless noise cancelling headphones,’ your database index is the wrong tool—here’s why.

## Learning objectives
- Explain inverted indexes, analyzers, segments, and ranking.
- Design document ingestion and query flow for search.
- Identify shard sizing, refresh latency, mapping, and reindexing tradeoffs.

## Topics & items to cover
- Hook: SQL B-trees handle exact/prefix lookup; search needs tokenization, relevance, filters, and typo tolerance.
- Definition: Elasticsearch is a distributed Lucene-based search engine using inverted indexes and near-real-time immutable segments.
- Worked example: 10M product docs. Analyzer lowercases “Noise-Cancelling Headphones” into tokens; inverted index maps `headphones → doc IDs`; query combines BM25 score with filters like `brand=Sony` and `in_stock=true`. Refresh exposes new segments after a short delay, so search is not strictly read-after-write.
- Tradeoffs: fast full-text and aggregations; operationally heavy, eventually consistent, mapping-sensitive, not a transactional source of truth.
- Real-world usage: product catalogs, logs, knowledge-base search, security events.
- Interview sentence: “I’ll keep canonical data in the primary DB, stream changes into Elasticsearch, and treat the index as rebuildable serving infrastructure.”
- Recap: search is indexing plus ranking, not just a SQL query.

## Anecdotes & war stories to use
- Lucene underpins Elasticsearch, Solr, and many internal search systems.
- The ELK stack made log search mainstream and taught teams about shard discipline.
- Dynamic mapping explosions in log pipelines are a well-known Elasticsearch ops failure mode.

## Things to mention / interview tips
- Say “analyzer” before “index” for full-text requirements.
- Use CDC/events from the source of truth.
- Mention aliases for zero-downtime reindexing.

## Common mistakes to call out
- Making Elasticsearch the transactional database.
- Ignoring mappings until fields explode.
- Expecting immediate read-after-write consistency.

## Diagrams / visuals to draw on screen
- Document → analyzer → tokens → inverted index.
- DB + CDC → index workers → search cluster.
- Query parse/filter/score/merge flow.

## Series glue
- Connect back to secondary indexes later. Next: Mixpanel-style analytics. Subscribe and check GitHub diagrams.
