# Scalable Inference & GPU Autoscaling

| | |
|---|---|
| **Publish order** | 115 |
| **Course #** | 87 |
| **Module** | M08 — Data Engineering & AI Systems |
| **Type** | concept |
| **Target length** | ~18 min |
| **Primary search keyword** | `llm inference scaling` |
| **Demand** | High |

**Thumbnail text idea:** GPU BOTTLENECK
**One-line hook (first 15s):** LLM autoscaling is weird because one request can hold GPU memory for hundreds of generated tokens.
## Learning objectives
- Explain why LLM inference bottlenecks are GPU memory, KV cache, and token scheduling.
- Estimate capacity using prompt tokens, output tokens, and latency targets.
- Compare batching, quantization, model routing, and autoscaling triggers.
- Design graceful degradation for overload.

## Topics & items to cover
- Hook: QPS alone is the wrong metric; tokens per second and active sequences matter.
- Definition: scalable inference is the serving layer that routes model requests to accelerators while meeting latency and cost SLOs.
- How it works: assume 100 req/s, 1K input tokens, 300 output tokens; the prefill phase consumes big matrix work up front, decode emits one token per sequence repeatedly; continuous batching mixes active requests so the GPU stays full.
- Tradeoffs: larger batches improve throughput but hurt tail latency; quantization lowers cost but may reduce quality; smaller fallback models protect availability; CPU autoscaling signals are misleading.
- Real-world usage: NVIDIA Triton, Ray Serve, KServe, vLLM, TensorRT-LLM, managed endpoints.
- Interview sentence: “I’ll scale on queued tokens, GPU utilization, KV-cache pressure, and first-token latency — not just HTTP request count.”
- Recap: capacity plan around TTFT, output tokens/sec, and dollars per thousand tokens.

## Anecdotes & war stories to use
- vLLM’s PagedAttention addressed KV-cache fragmentation, a real serving bottleneck for variable-length requests.
- ChatGPT-like launches showed that product virality can turn inference capacity into the limiting factor overnight.
- Cloud GPU shortages have been widely reported during AI booms, forcing teams to use model routing and quotas.
- Many providers expose streaming because perceived latency improves even when total generation time stays similar.

## Things to mention / interview tips
- Distinguish prefill from decode phases.
- Include admission control: max context, max output tokens, per-user queues.
- Mention warm pools because cold GPU model load can be minutes.
- Track cost per successful answer, not just uptime.

## Common mistakes to call out
- Autoscaling GPUs on CPU utilization.
- Ignoring long prompts that consume KV cache.
- Assuming Kubernetes HPA reacts fast enough for sudden spikes.
- Forgetting noisy-neighbor isolation for enterprise tenants.

## Diagrams / visuals to draw on screen
- Prefill/decode timeline for three requests.
- Router choosing small, large, or fallback model.
- GPU pool with queue depth, KV cache, and autoscaler.

## Series glue
- Builds on the ChatGPT design video; next guardrails explain quality/safety after serving. CTA: subscribe and check the repo’s inference sizing worksheet.
