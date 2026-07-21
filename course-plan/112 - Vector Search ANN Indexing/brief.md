# Vector Search & ANN Indexing (HNSW) Explained

| | |
|---|---|
| **Publish order** | 112 |
| **Course #** | 83 |
| **Module** | M08 — Data Engineering & AI Systems |
| **Type** | concept |
| **Target length** | ~20 min |
| **Primary search keyword** | `vector search ann` |
| **Demand** | Very High |

**Thumbnail text idea:** NEAREST NEIGHBORS FAST
**One-line hook (first 15s):** Vector search is easy at 10,000 items; the interview starts when you need good nearest neighbors across millions under latency and memory limits.

## Learning objectives
- Explain embeddings, similarity metrics, nearest-neighbor search, and ANN.
- Describe HNSW intuition: layered navigable small-world graph.
- Tune recall, latency, memory, filtering, and freshness.
- Decide when to use vector search, keyword search, or hybrid retrieval.

## Topics & items to cover
- Hook: a brute-force dot product over every document is accurate but too slow at scale.
- Definition: vector search finds items with embeddings close to a query vector; ANN trades exactness for speed.
- Worked example: 10M document chunks with 768-dim embeddings; exact scan is billions of multiplications per query, so HNSW keeps graph neighbors, searches from sparse top layer down to dense layer, and returns top 20 candidates in milliseconds with tunable recall.
- How it works: embed query -> choose metric cosine/dot/L2 -> traverse HNSW using `efSearch` candidate list -> optional metadata filter -> rerank exact distances -> return IDs/chunks.
- Tradeoffs: higher `M` and `efConstruction` improve recall but increase memory/build time; higher `efSearch` improves recall but raises latency; metadata filters can break recall if applied naively; updates/deletes require maintenance.
- Real-world usage: semantic search, recommendations, image similarity, deduplication, anomaly search, RAG retrieval.
- Interview sentence: “I would use ANN like HNSW for candidate generation, measure recall@K against an exact baseline, and combine it with filters/reranking for correctness.”
- Recap: ANN is controlled approximation with measured recall.

## Anecdotes & war stories to use
- Spotify/Netflix-style recommenders rely on embedding-like representations and candidate generation before ranking.
- FAISS from Meta made large-scale similarity search practical for many ML teams.
- HNSW became popular because graph traversal offers strong recall/latency tradeoffs for in-memory search.
- Production RAG systems often add BM25 hybrid search because vectors alone miss exact product names, codes, or error strings.

## Things to mention / interview tips
- Define the metric and normalize vectors if using cosine/dot product.
- Measure recall@K, p95 latency, memory per vector, and index build time.
- Discuss deletes, re-embedding, versioned indexes, and backfills.
- Use hybrid search for exact terms and semantic meaning.

## Common mistakes to call out
- Assuming vector search replaces keyword search.
- Ignoring metadata filters and tenant isolation.
- Not benchmarking against exact nearest neighbors.
- Forgetting embedding model changes require re-indexing.

## Diagrams / visuals to draw on screen
- 2D embedding space with nearest neighbors.
- HNSW layered graph search from top to bottom.
- Recall-latency knob for `efSearch`.
- Hybrid retrieval: BM25 + vector + reranker.

## Series glue
- Follow directly from RAG architecture: this is the retrieval engine. Forward to future AI/data videos on ML serving and feature stores. CTA: subscribe and use the GitHub ANN benchmark notebook.
