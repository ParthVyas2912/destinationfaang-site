# Distributed Tracing & Root-Cause Analysis

| | |
|---|---|
| **Publish order** | 107 |
| **Course #** | 67 |
| **Module** | M06 — Security, Observability & FinOps |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `distributed tracing` |
| **Demand** | High |

**Thumbnail text idea:** FIND THE SLOW HOP
**One-line hook (first 15s):** Metrics tell you checkout is slow; tracing tells you the slowness is one payment call, one shard, or one retry loop.

## Learning objectives
- Explain traces, spans, trace IDs, parent-child relationships, and context propagation.
- Instrument HTTP, queues, databases, and async workflows.
- Use sampling without losing the traces needed for incidents.
- Combine traces with logs and metrics for root cause analysis.

## Topics & items to cover
- Hook: in microservices, the broken component is often three hops away from the failing API.
- Definition: distributed tracing records the path and timing of one request across service boundaries.
- Worked example: checkout trace has spans: API 220ms, inventory 35ms, tax 40ms, payment 900ms with two retries, DB write 20ms; the waterfall reveals payment provider latency, not checkout CPU.
- How it works: create trace/span IDs at ingress -> propagate `traceparent` headers/messages -> auto/manual instrumentation emits spans -> backend indexes and visualizes waterfall/service map.
- Tradeoffs: full tracing is expensive; head sampling can miss rare errors; tail sampling catches slow/error traces but needs buffering; async queues require explicit links.
- Real-world usage: OpenTelemetry, Jaeger, Zipkin, Honeycomb, Datadog, service dependency maps, canary comparison.
- Interview sentence: “I would propagate W3C trace context through sync and async calls, sample intelligently, and correlate trace IDs into structured logs.”
- Recap: traces explain causality across hops.

## Anecdotes & war stories to use
- Google’s Dapper paper established many core tracing ideas used by Zipkin, Jaeger, and OpenTelemetry.
- Twitter’s Zipkin helped engineers see cross-service latency in a large service graph.
- OpenTelemetry became the vendor-neutral standard because teams wanted instrumentation not locked to one backend.
- Async systems often lose trace context unless message headers carry it explicitly.

## Things to mention / interview tips
- Propagate context through queues, not just HTTP.
- Add attributes like route, region, shard, retry count; avoid PII.
- Use exemplars to jump from metrics to traces.
- Prefer tail/error sampling for rare high-value failures.

## Common mistakes to call out
- Logging trace IDs but not emitting spans.
- Breaking context at message queues or background jobs.
- Adding user emails/order contents as span attributes.
- Sampling away all errors.

## Diagrams / visuals to draw on screen
- Trace waterfall for checkout.
- Service dependency map with hot edge.
- Context propagation through HTTP and queue headers.
- Metrics -> exemplar -> trace -> logs workflow.

## Series glue
- Build on RED/USE dashboards: metrics detect, traces localize. Next: scalable logging keeps evidence searchable without runaway cost. CTA: subscribe and clone GitHub OpenTelemetry snippets.
