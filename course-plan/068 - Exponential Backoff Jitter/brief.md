# Exponential Backoff & Jitter (Retry Storms)

| | |
|---|---|
| **Publish order** | 068 |
| **Course #** | 48 |
| **Module** | M05 — Microservices & Reliability |
| **Type** | concept |
| **Target length** | ~10 min |
| **Primary search keyword** | `exponential backoff jitter` |
| **Demand** | Moderate |

**Thumbnail text idea:** ADD JITTER
**One-line hook (first 15s):** If ten thousand clients all retry at exactly one second, your outage just scheduled its own sequel.

## Learning objectives
- Explain exponential backoff, jitter, retry budgets, and retry storms.
- Calculate retry timing for a concrete client fleet.
- Choose safe retry policies for APIs, queues, mobile apps, and IoT devices.

## Topics & items to cover
- Hook: synchronized clients can turn a 30-second blip into minutes of overload.
- Definition: exponential backoff increases delay after each failure; jitter randomizes delay so clients don’t retry in lockstep.
- Worked example: 10K mobile clients fail. Bad: retry at exactly 1s, 2s, 4s, creating spikes of 10K. Better: cap at 30s, max 3 attempts, full jitter chooses random delay between 0 and cap. Retry only 5xx/429/network errors, not 400s; honor `Retry-After`.
- Tradeoffs: protects servers and recovery; increases individual completion latency. Use retry budgets so retries don’t exceed a safe share of traffic.
- Real usage: AWS guidance recommends jittered backoff; IoT reconnect storms need it.
- Interview sentence: “I’ll use capped exponential backoff with jitter and a retry budget, and honor server-side rate-limit hints.”
- Recap: retries are load; randomize and cap them.

## Anecdotes & war stories to use
- AWS’s “Exponential Backoff and Jitter” article is the canonical reference.
- IoT and mobile fleets commonly need jitter after network outages.
- `Retry-After` exists because servers need client cooperation during overload.

## Things to mention / interview tips
- Say which errors are retryable.
- Keep retries inside end-to-end latency budget.
- Use idempotency keys for state-changing retries.

## Common mistakes to call out
- Retrying every error.
- Infinite retries from all clients.
- Deterministic schedules with no jitter.

## Diagrams / visuals to draw on screen
- Synchronized spikes vs jitter-smoothed retries.
- Backoff formula with cap.
- Retry budget chart.

## Series glue
- Zooms in from circuit breakers and leads into backpressure/load shedding. Subscribe and find sample policies in GitHub.
