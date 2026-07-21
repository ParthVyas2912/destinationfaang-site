# Zero-Downtime Database Migrations

| | |
|---|---|
| **Publish order** | 085 |
| **Course #** | 13 |
| **Module** | M01 — Scalability Foundations |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `zero downtime migration` |
| **Demand** | High |

**Thumbnail text idea:** MIGRATE LIVE
**One-line hook (first 15s):** The safest database migration is boring: expand, backfill, dual-write, verify, contract.

## Learning objectives
- Apply expand-and-contract migrations for live services.
- Design backfills, dual writes, and read cutovers safely.
- Avoid locks, long transactions, and incompatible schema changes.
- Build rollback plans for each phase.

## Topics & items to cover
- Hook: adding `NOT NULL` to a huge table at noon can become a production incident.
- Definition: zero-downtime migration changes schema/data while old and new app versions keep serving traffic.
- Worked example: split `users.full_name` into `first_name` and `last_name`: add nullable columns, deploy dual-write, backfill chunks of 5,000 rows, read behind flag, validate counts, remove old column later.
- How it works: backward-compatible schema, online DDL, chunked backfill, idempotent jobs, dual-write or CDC, shadow reads, feature flags, delayed cleanup.
- Tradeoffs: multiple deploys and temporary complexity; dual-write can diverge; online indexes consume resources; rollback gets harder after destructive steps.
- Real-world usage: GitHub online migration tooling, gh-ost/pt-online-schema-change, Rails strong_migrations, expand/contract playbooks.
- Interview sentence: "I’ll never make schema and code incompatible in the same deploy; I’ll expand first, migrate safely, then contract after verification."
- Recap: compatibility across versions is the trick.

## Anecdotes & war stories to use
- GitHub has written publicly about online schema migrations for large MySQL tables.
- GitHub’s gh-ost popularized triggerless online MySQL migrations.
- Rails communities adopted strong migration checks after teams locked production tables.
- Etsy-style continuous delivery emphasized small reversible deploys over big-bang releases.

## Things to mention / interview tips
- Name phases: expand, migrate/backfill, switch reads, contract.
- Use chunking with sleep/throttle and checkpoints.
- Validate with row counts, checksums, and shadow reads.
- Defer destructive cleanup until old code is gone.

## Common mistakes to call out
- Dropping or renaming a column used by old app instances.
- Running one massive backfill transaction.
- Assuming rollback after destructive data transformation.
- Forgetting indexes before switching read paths.

## Diagrams / visuals to draw on screen
- Expand-contract timeline across deploys.
- Dual-write and shadow-read path.
- Chunked backfill progress with checkpoints.

## Series glue
- Builds on connection pooling and backfill safety; next module turns to networking fundamentals. CTA: subscribe and grab the migration checklist from GitHub.
