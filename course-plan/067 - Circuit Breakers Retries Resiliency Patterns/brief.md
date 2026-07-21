# Circuit Breakers, Retries & Resiliency Patterns

| | |
|---|---|
| **Publish order** | 067 |
| **Course #** | 47 |
| **Module** | M05 — Microservices & Reliability |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `circuit breaker pattern` |
| **Demand** | High |

**Thumbnail text idea:** STOP CASCADES
**One-line hook (first 15s):** The retry that saves one request can also take down the whole fleet if every client does it at once.

## Learning objectives
- Explain timeouts, retries, circuit breakers, bulkheads, and fallbacks.
- Design resilient service calls with bounded failure impact.
- Choose retry policies based on idempotency, latency budget, and error type.

## Topics & items to cover
- Hook: one slow dependency can exhaust every thread in a healthy service.
- Definition: resiliency patterns limit failure propagation: timeouts stop waiting, retries handle transient failures, circuit breakers stop calling known-bad dependencies, bulkheads isolate resources.
- Worked example: Checkout calls Payment. Timeout 300ms; retry idempotent `authorize` only with idempotency key, max 2 attempts with jitter. Circuit opens after high failure rate over rolling window, half-open probes recovery. Fallback marks order “payment pending” or asks user to retry.
- Tradeoffs: better availability and latency isolation; risk of hiding errors, stale fallbacks, retry amplification.
- Real usage: Netflix Hystrix popularized circuit breakers/bulkheads; service meshes now expose similar policies.
- Interview sentence: “Every remote call gets a timeout, bounded retries with jitter only when safe, and a circuit breaker so one dependency cannot consume all caller resources.”
- Recap: resilience limits blast radius.

## Anecdotes & war stories to use
- Netflix Hystrix and Simian Army made failure isolation mainstream.
- AWS reliability guidance warns about retries without backoff.
- Many postmortems cite retry storms and thread-pool exhaustion.

## Things to mention / interview tips
- Start with timeouts.
- Tie retries to idempotency keys.
- Use separate connection/thread pools per dependency.

## Common mistakes to call out
- Retrying non-idempotent payment captures.
- Letting retries exceed user latency budget.
- Using one shared worker pool for all downstream calls.

## Diagrams / visuals to draw on screen
- Cascading failure call graph.
- Circuit breaker closed/open/half-open state machine.
- Retry timeline with timeout and jitter.

## Series glue
- Builds on microservice boundaries. Next: backoff and jitter. Subscribe and use GitHub templates.
