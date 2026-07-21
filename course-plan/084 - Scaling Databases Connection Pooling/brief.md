# Scaling Databases: Connection Pooling

| | |
|---|---|
| **Publish order** | 084 |
| **Course #** | 12 |
| **Module** | M01 — Scalability Foundations |
| **Type** | concept |
| **Target length** | ~12 min |
| **Primary search keyword** | `database connection pooling` |
| **Demand** | Moderate |

**Thumbnail text idea:** POOL CONNECTIONS
**One-line hook (first 15s):** Your database can be healthy and still go down because your app opened too many connections.

## Learning objectives
- Explain why database connections are expensive and finite.
- Size pools from concurrency and latency targets.
- Compare app pools, PgBouncer-style poolers, and serverless proxies.
- Diagnose pool exhaustion versus slow query problems.

## Topics & items to cover
- Hook: 200 pods each open 20 Postgres connections; the database sees 4,000 clients before work begins.
- Definition: connection pooling reuses a bounded set of database sessions instead of opening one per request.
- Worked example: API needs 1,000 req/s; DB query averages 20ms. Little’s Law suggests about 20 concurrent DB operations, so start near 30-50 and load test.
- How it works: checkout/checkin, max pool, wait queue, idle timeout, transaction pooling, prepared-statement caveats, backpressure.
- Tradeoffs: too small increases waiting; too large overloads DB memory/context switching; transaction poolers break session-state assumptions.
- Real-world usage: PgBouncer, RDS Proxy for Lambda, HikariCP, Prisma/data proxy patterns.
- Interview sentence: "I’d bound database concurrency with a pool and treat pool wait time as backpressure, not let every request create a connection."
- Recap: pool size protects the database.

## Anecdotes & war stories to use
- PgBouncer is widely deployed because Postgres backends are heavier than app threads.
- Serverless adoption exposed connection storms, leading to managed connection proxies.
- Java services often standardize on HikariCP because pool behavior affects tail latency.
- Many outage writeups include "max connections reached" as an unbounded scaling symptom.

## Things to mention / interview tips
- Use Little’s Law: concurrency ≈ throughput × latency.
- Monitor pool wait, active connections, idle connections, and DB CPU.
- Put a queue/timeouts before the DB to fail gracefully.
- Mention transaction versus session pooling.

## Common mistakes to call out
- Increasing pool size whenever requests time out.
- Giving every microservice a huge pool.
- Forgetting long transactions pin connections.
- Using session variables with transaction pooling unknowingly.

## Diagrams / visuals to draw on screen
- App requests queueing into bounded pool to DB.
- Pool sizing calculation with Little’s Law.
- PgBouncer between many app pods and fewer DB sessions.

## Series glue
- Follows conflict/consistency with a concrete database bottleneck; next shows zero-downtime migrations. CTA: subscribe and see GitHub sizing worksheet.
