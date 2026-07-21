# Design a Document Vector Search System

| | |
|---|---|
| **Publish order** | 126 |
| **Course #** | VS |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~28 min |
| **Primary search keyword** | `document vector search` |
| **Demand** | High |

**Thumbnail text idea:** VECTOR SEARCH
**One-line hook (first 15s):** Vector search is not magic similarity — it is an indexing system with chunking, embeddings, filters, and painful recall-latency tradeoffs.
## Learning objectives
- Design document ingestion, chunking, embedding, indexing, and query flows.
- Choose metadata filters and tenant-aware sharding.
- Explain ANN tradeoffs: recall, latency, freshness, cost.
- Handle updates, deletes, and permissions.

## Topics & items to cover
- **Requirements:** upload docs, search semantically, filter by tenant/ACL/type/date, return snippets with source links; support incremental updates.
- **Estimation:** 10M docs, 50 chunks/doc, 768-dim embeddings; vector storage and ANN index memory dominate; query target under 200 ms.
- **API/Data model:** `POST /documents`, `POST /search`, `DELETE /documents/{id}`; `Document`, `Chunk`, `Embedding`, `Metadata`, `AclEntry`; shard by `tenant_id`, then collection/index partition; store text in object store and metadata in Postgres/NoSQL.
- **High-level design:** ingestion parser → chunker → embedding workers → vector DB/ANN index → query embedding → metadata pre/post-filter → reranker → results.
- **Deep dives/bottlenecks:** chunk size/overlap affects recall; HNSW/IVF indexing trades memory for latency; ACL filtering must happen before returning results; deletes need tombstones plus background compaction.
- **Wrap-up:** metrics: recall@k, p95 latency, indexing lag, stale/deleted result rate.

## Anecdotes & war stories to use
- Pinecone, Weaviate, Milvus, and pgvector adoption grew with RAG use cases.
- HNSW is widely used because it gives strong approximate nearest neighbor performance for many workloads.
- Enterprises often discover that metadata filtering and permissions are harder than computing embeddings.
- PostgreSQL pgvector became popular for teams that wanted vector search near relational metadata.

## Things to mention / interview tips
- Ask whether filters are mandatory security filters or optional ranking filters.
- Specify re-embedding strategy when the embedding model changes.
- Include a lexical fallback/hybrid search for exact terms and IDs.
- Mention reranking top 50-100 candidates with a cross-encoder/LLM.

## Common mistakes to call out
- Embedding whole PDFs as one vector.
- Applying ACL filters after showing snippets.
- Ignoring updates/deletes and stale indexes.
- Assuming higher cosine similarity always means better answer usefulness.

## Diagrams / visuals to draw on screen
- Document-to-chunks-to-vectors pipeline.
- Query path with ANN search, filters, and reranker.
- HNSW-style graph intuition diagram.

## Series glue
- Builds on embeddings, storage, and data quality; next is full production RAG. CTA: subscribe and use the repo’s vector-search schema.
