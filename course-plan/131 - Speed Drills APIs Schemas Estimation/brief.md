# Speed Drills: APIs, Schemas & Estimation

| | |
|---|---|
| **Publish order** | 131 |
| **Course #** | MOCK4 |
| **Module** | M10 — Mock Interview & Practice |
| **Type** | mock |
| **Target length** | ~30 min |
| **Primary search keyword** | `system design estimation practice` |
| **Demand** | High |

**Thumbnail text idea:** SPEED DRILLS
**One-line hook (first 15s):** This video is your interview gym: short reps for APIs, schemas, and estimates until the basics become automatic.
## Learning objectives
- Practice fast, structured answers for common design subproblems.
- Produce APIs, schemas, and estimates in minutes.
- Learn what interviewers look for in intermediate artifacts.
- Build confidence before full mocks.

## Topics & items to cover
- 0-3 min setup: explain the drill format and scoring: clear assumptions, units, and tradeoffs beat false precision.
- 3-10 API drills: design endpoints for URL shortener, notification preferences, file upload, feed page; scoring callout: resource nouns, pagination, idempotency, auth context.
- 10-18 schema drills: model orders/payments, chat messages, follows, document chunks; call out primary keys, secondary indexes, TTLs, and shard keys.
- 18-25 estimation drills: DAU → QPS, storage/day, bandwidth, cache size; use powers of ten and peak multiplier; scoring: sanity checks and bottleneck identification.
- 25-30 recap: turn rough numbers into architecture decisions: queue size, partition count, DB choice, cache capacity.
- Capstone-style mini rubric: 4 points requirements, 4 APIs/data, 4 estimates, 4 bottlenecks, 4 communication.

## Anecdotes & war stories to use
- Real system design interviews often spend only a few minutes on estimates, but those minutes steer the whole architecture.
- API clarity is a strong signal because production systems are contracts between teams.
- Senior candidates are expected to name shard keys, not merely tables.
- Many failed interviews come from jumping to diagrams before defining operations and scale.

## Things to mention / interview tips
- Say assumptions aloud and keep numbers round.
- Tie every estimate to a decision: memory, partitions, workers, or cost.
- Prefer simple schemas with explicit indexes over vague “NoSQL table.”
- Include pagination and idempotency by default where relevant.

## Common mistakes to call out
- Calculating precise numbers that do not affect design.
- Forgetting read/write ratio.
- Missing indexes for the query path just described.
- Designing APIs with verbs everywhere and no resource model.

## Diagrams / visuals to draw on screen
- One-page drill worksheet: requirements → API → schema → estimate.
- QPS/storage calculation ladder.
- Schema cards with PK, SK, indexes, shard key.

## Series glue
- Pulls patterns from all earlier case studies; next video teaches storytelling tactics. CTA: subscribe and download printable drill sheets from GitHub.
