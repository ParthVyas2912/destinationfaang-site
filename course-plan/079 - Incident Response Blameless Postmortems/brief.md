# Incident Response & Blameless Postmortems

| | |
|---|---|
| **Publish order** | 079 |
| **Course #** | 58 |
| **Module** | M05 — Microservices & Reliability |
| **Type** | concept |
| **Target length** | ~12 min |
| **Primary search keyword** | `blameless postmortem` |
| **Demand** | Moderate |

**Thumbnail text idea:** NO BLAME
**One-line hook (first 15s):** A postmortem that finds a guilty engineer but no system fix is just an incident waiting to repeat.

## Learning objectives
- Run an incident with roles, severity, timeline, and communication.
- Write a blameless postmortem focused on contributing factors.
- Convert incidents into prioritized corrective actions.
- Explain how SLOs guide urgency and customer messaging.

## Topics & items to cover
- Hook: the outage is over only when learning is captured and fixes are owned.
- Definition: incident response coordinates mitigation; a blameless postmortem explains what happened without punishing good-faith actions.
- Worked example: API errors jump at 10:05; commander declares SEV2, comms posts every 15 minutes, ops rolls back deploy, scribe records timeline, postmortem creates canary and alert actions.
- How it works: detection, triage, roles, mitigation, customer comms, timeline, contributing causes, owners and deadlines.
- Tradeoffs: fast mitigation may sacrifice diagnosis; too many actions dilute follow-through; psychological safety must coexist with accountability.
- Real-world usage: Google SRE practices, Etsy blameless culture writing, PagerDuty-style incident command, status pages.
- Interview sentence: "I’d separate mitigation from analysis, assign incident roles early, and make the postmortem produce tracked system changes."
- Recap: incidents are operational data.

## Anecdotes & war stories to use
- Etsy engineering popularized public discussion of blameless postmortems.
- Google SRE books describe postmortems as reliability improvement, not paperwork.
- PagerDuty and similar platforms formalized commander, scribe, and comms roles.
- Public cloud status pages show the difficulty of timely customer communication.

## Things to mention / interview tips
- Use "contributing factors," not one magical root cause.
- Include exact timestamps and decision points.
- Track action items like product work with owners and due dates.
- Describe customer impact in user terms, not CPU graphs.

## Common mistakes to call out
- Waiting too long to declare an incident.
- Combining debugging and customer comms in one chaotic channel.
- Writing vague fixes like "be more careful."
- Letting postmortem actions rot.

## Diagrams / visuals to draw on screen
- Incident role board: commander, tech lead, comms, scribe.
- Timeline from alert to mitigation to resolution.
- Postmortem template: impact, causes, actions.

## Series glue
- Completes the reliability arc after chaos engineering; next shifts to event data replays and backfills. CTA: subscribe and grab templates from GitHub.
