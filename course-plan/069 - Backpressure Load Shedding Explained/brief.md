# Backpressure & Load Shedding Explained

| | |
|---|---|
| **Publish order** | 069 |
| **Course #** | 49 |
| **Module** | M05 — Microservices & Reliability |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `backpressure load shedding` |
| **Demand** | Moderate |

**Thumbnail text idea:** SHED LOAD
**One-line hook (first 15s):** A system that refuses work carefully is healthier than a system that accepts everything and times out everything.

## Learning objectives
- Explain backpressure, load shedding, admission control, and graceful degradation.
- Design overload handling for APIs, queues, and stream processors.
- Choose signals and priorities for slowing producers or rejecting work.

## Topics & items to cover
- Hook: under overload, the worst answer is often “queue everything.”
- Definition: backpressure tells upstream producers to slow down; load shedding intentionally drops or rejects lower-priority work to preserve core functionality.
- Worked example: API gets 20K RPS but handles 10K. Use token buckets per tenant, bounded queues, `429` with `Retry-After`, prioritize checkout over recommendations, degrade homepage to cached content. In streams, consumer lag triggers source throttling or dropping debug events.
- Tradeoffs: protects latency and availability for important traffic; some work is delayed/lost; product must define priority.
- Real usage: TCP flow control, reactive streams demand signals, overload protection in large services.
- Interview sentence: “I’ll use bounded queues and admission control; when overloaded, I prefer fast rejection or degraded responses over unbounded latency.”
- Recap: overload strategy is part of the API contract.

## Anecdotes & war stories to use
- TCP sliding windows are the foundational backpressure example.
- Netflix and other platforms discuss graceful degradation for non-critical features.
- Queue buildup causing latency collapse appears in many outage postmortems.

## Things to mention / interview tips
- Define what gets dropped first.
- Use bounded queues everywhere.
- Measure queue depth, lag, saturation, and tail latency.

## Common mistakes to call out
- Adding an infinite queue to “solve” overload.
- Treating all requests as equal priority.
- Assuming autoscaling is the only strategy.

## Diagrams / visuals to draw on screen
- Producer/consumer with bounded queue and signal.
- Priority load-shedding ladder.
- Latency collapse curve.

## Series glue
- Follows retries/backoff and prepares for active-active availability. Subscribe and use GitHub diagrams.
