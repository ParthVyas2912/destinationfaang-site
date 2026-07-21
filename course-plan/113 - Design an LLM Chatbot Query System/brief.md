# Design an LLM Chatbot & Query System (ChatGPT-Style)

| | |
|---|---|
| **Publish order** | 113 |
| **Course #** | 120 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~35 min |
| **Primary search keyword** | `design chatgpt` |
| **Demand** | Very High |

**Thumbnail text idea:** CHATGPT DESIGN
**One-line hook (first 15s):** If an interviewer says 'design ChatGPT,' they are not asking you to train GPT-5 — they want the serving, memory, safety, and retrieval system around the model.
## Learning objectives
- Separate model training, inference serving, conversation storage, and retrieval-augmented answering.
- Design streaming chat APIs with session memory, rate limits, and safety filters.
- Estimate token throughput, GPU capacity, and storage for conversations.
- Explain latency/cost tradeoffs: caching, batching, routing, and context trimming.

## Topics & items to cover
- **Requirements:** multi-turn chat, streamed tokens, auth, history, optional file/search retrieval, abuse controls; exclude training a foundation model.
- **Estimation:** 1M DAU, 5 prompts/day, 800 input + 500 output tokens means billions of daily tokens; peak QPS drives GPU replicas, not DB size.
- **API/Data model:** `POST /v1/chat/sessions`, `POST /sessions/{id}/messages`, SSE/WebSocket stream; `User`, `Session`, `Message`, `ToolCall`, `SafetyDecision`; shard by `user_id` with hot-account throttles.
- **High-level design:** API gateway → auth/rate limiter → chat orchestrator → prompt builder → safety precheck → model router/GPU inference → stream aggregator → conversation store; optional vector retrieval/tool executor.
- **Deep dives/bottlenecks:** GPU saturation solved with continuous batching and token-level scheduling; context-window explosion solved with summarization + pinned facts; hallucination/tool errors handled with RAG citations, constrained tool schemas, and post-generation checks.
- **Wrap-up:** call out SLOs: first-token latency, tokens/sec, cost per answer, unsafe-response rate.

## Anecdotes & war stories to use
- OpenAI publicly described ChatGPT's viral launch as creating intense scaling pressure around serving and reliability, not just model quality.
- vLLM popularized PagedAttention to reduce KV-cache waste during high-throughput LLM serving.
- Anthropic/OpenAI both expose streaming APIs because users perceive first-token latency differently from total completion latency.
- Enterprise chatbots often fail on permissions: retrieval must filter documents before generation, not after.

## Things to mention / interview tips
- Say: “I’ll design the product system around a hosted LLM; model training is out of scope unless requested.”
- Always ask about streaming, tools, retention, privacy, and safety requirements.
- Name concrete metrics: TTFT, tokens/sec/GPU, context length, cache hit rate.
- Mention graceful degradation: smaller model fallback, queueing, or shorter context under load.

## Common mistakes to call out
- Treating the LLM as a stateless HTTP call with no orchestration layer.
- Storing raw prompts forever without retention/privacy controls.
- Ignoring KV-cache memory and assuming CPU-style autoscaling.
- Adding RAG but forgetting document ACL filtering.

## Diagrams / visuals to draw on screen
- Sequence diagram from user prompt to streamed tokens.
- GPU inference pool with batch scheduler and KV cache.
- Conversation memory: recent turns, summary, pinned user facts, retrieved docs.
- Safety pipeline before and after generation.

## Series glue
- Reference earlier API, caching, queues, and vector search videos; preview feature stores, inference scaling, guardrails, and RAG. CTA: subscribe and grab diagrams/checklists from the GitHub repo.
