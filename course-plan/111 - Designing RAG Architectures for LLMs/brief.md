# Designing RAG Architectures for LLMs

| | |
|---|---|
| **Publish order** | 111 |
| **Course #** | 84 |
| **Module** | M08 — Data Engineering & AI Systems |
| **Type** | concept |
| **Target length** | ~24 min |
| **Primary search keyword** | `rag architecture` |
| **Demand** | Very High |

**Thumbnail text idea:** SEARCH BEFORE GENERATE
**One-line hook (first 15s):** RAG works when retrieval gives the model the right evidence at the right time; it fails when you treat a vector database as magic memory.

## Learning objectives
- Design ingestion, chunking, embedding, indexing, retrieval, reranking, prompting, and citation flow.
- Choose metadata filters, hybrid search, and freshness strategies.
- Evaluate grounding, answer quality, latency, and cost.
- Handle permissions, hallucinations, and stale documents.

## Topics & items to cover
- Hook: the LLM should answer from retrieved evidence, not from vibes.
- Definition: retrieval-augmented generation fetches relevant external context and supplies it to an LLM before generation.
- Worked example: support bot over 100k docs; ingest PDFs/HTML, chunk 500-800 tokens with overlap, embed chunks, store vector plus title/product/version/ACL, retrieve top 50 by hybrid search, rerank to top 8, prompt with citations, and refuse if evidence score is weak.
- How it works: connectors -> parser -> chunker -> embedding model -> vector/BM25 index -> query rewrite -> filter by user ACL -> ANN search -> reranker -> prompt builder -> LLM -> evaluation/logging.
- Tradeoffs: smaller chunks improve precision but lose context; larger chunks reduce fragmentation but waste tokens; hybrid search helps exact terms; reranking improves quality but adds latency/cost.
- Real-world usage: enterprise search, customer support, developer docs, legal/medical knowledge assistants, internal copilots.
- Interview sentence: “I would treat RAG as a search system with permission-aware retrieval, measured grounding, and explicit refusal when evidence is insufficient.”
- Recap: retrieval quality dominates generation quality.

## Anecdotes & war stories to use
- Early enterprise chatbots often failed because they ignored document ACLs; RAG must enforce permissions before the prompt.
- Search engines have long used lexical plus semantic ranking; RAG benefits from the same hybrid retrieval lesson.
- OpenAI, Anthropic, and Microsoft documentation all emphasize grounding/citations because users need verifiable answers.
- Many production teams add rerankers after discovering nearest-neighbor embeddings alone return plausible but wrong chunks.

## Things to mention / interview tips
- Include an offline evaluation set of real questions with expected citations.
- Use metadata filters for tenant, product, version, language, and freshness.
- Log retrieved document IDs, prompt version, model version, latency, and user feedback.
- Build refusal and escalation paths for low-confidence retrieval.

## Common mistakes to call out
- Stuffing entire documents into prompts.
- Ignoring ACLs and leaking private docs.
- Evaluating only “sounds good” rather than cited correctness.
- Updating documents without re-embedding or invalidating stale chunks.

## Diagrams / visuals to draw on screen
- Ingestion pipeline from document to chunk embeddings.
- Query-time retrieval/rerank/prompt/answer path.
- ACL filter before vector search.
- Evaluation loop with feedback and golden questions.

## Series glue
- Connect to search, caching, and observability modules. Next: vector search and HNSW, the indexing engine behind many RAG systems. CTA: subscribe and clone the GitHub RAG reference architecture.
