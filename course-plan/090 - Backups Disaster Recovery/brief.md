# Backups & Disaster Recovery (RPO / RTO)

| | |
|---|---|
| **Publish order** | 090 |
| **Course #** | 29 |
| **Module** | M03 — Data, Storage & Caching |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `backup disaster recovery` |
| **Demand** | Moderate |

**Thumbnail text idea:** RESTORE FIRST
**One-line hook (first 15s):** A backup strategy is not real until someone has restored from it under pressure.

## Learning objectives
- Define RPO and RTO with business examples.
- Design backup, replication, and restore for databases and object stores.
- Choose hot, warm, and cold disaster-recovery architectures.
- Explain validation, drills, and ransomware-resistant backups.

## Topics & items to cover
- Hook: "we have backups" is weak; "we restored last Tuesday in 37 minutes" is strong.
- Definition: RPO is acceptable data loss; RTO is acceptable recovery time.
- Worked example: payments DB requires RPO under 1 minute and RTO under 30 minutes, so use near-sync replica plus point-in-time recovery; analytics lake can tolerate daily snapshots.
- How it works: snapshots, WAL/binlog archiving, point-in-time restore, cross-region replication, object versioning, immutable backups, runbooks, drills.
- Tradeoffs: lower RPO/RTO costs more; sync replication can add latency; active-active is complex; backups can copy corrupted data.
- Real-world usage: cloud database PITR, S3 versioning/object lock, multi-region failover, ransomware recovery playbooks.
- Interview sentence: "I’ll set RPO/RTO per data class, then prove the design with automated restore tests, not just backup creation."
- Recap: recovery objectives drive architecture.

## Anecdotes & war stories to use
- GitLab’s 2017 database incident is a public reminder that restore procedures matter.
- Cloud providers emphasize point-in-time recovery because snapshots alone may lose recent writes.
- Ransomware incidents pushed organizations toward immutable or offline backup copies.
- Multi-region outages show failover runbooks must be practiced before the region is unavailable.

## Things to mention / interview tips
- Ask separate RPO/RTO for payments, user content, logs, and analytics.
- Include restore testing in operations calendars.
- Protect backups from deletion by compromised production credentials.
- Consider dependency order during regional recovery.

## Common mistakes to call out
- Equating replication with backup.
- Never testing restores.
- Using one RPO/RTO for all data.
- Forgetting schema/app version compatibility during restore.

## Diagrams / visuals to draw on screen
- Timeline showing backup, failure, RPO loss, RTO recovery.
- Hot/warm/cold DR comparison.
- Backup pipeline: snapshot, WAL, immutable copy, restore test.

## Series glue
- Follows storage formats because durable bytes still need recovery; next covers data lake governance. CTA: subscribe and use the GitHub DR worksheet.
