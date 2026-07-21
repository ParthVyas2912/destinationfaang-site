# Threat Modeling with STRIDE

| | |
|---|---|
| **Publish order** | 104 |
| **Course #** | 61 |
| **Module** | M06 — Security, Observability & FinOps |
| **Type** | concept |
| **Target length** | ~12 min |
| **Primary search keyword** | `stride threat modeling` |
| **Demand** | Moderate |

**Thumbnail text idea:** THINK LIKE ATTACKERS
**One-line hook (first 15s):** Threat modeling is not paranoia; it is a structured way to find the expensive security bugs before production finds them for you.

## Learning objectives
- Use STRIDE: spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege.
- Build a data-flow diagram with trust boundaries.
- Convert threats into mitigations and owners.
- Apply STRIDE to a concrete API design in an interview.

## Topics & items to cover
- Hook: a secure architecture starts by asking what can go wrong at each boundary.
- Definition: STRIDE is a threat-modeling checklist for categories of attacker goals against system components and data flows.
- Worked example: file-upload service with browser, API, object storage, malware scanner, metadata DB, and admin UI; spoofing via stolen session, tampering with object key, repudiation without audit logs, disclosure through public bucket, DoS through huge files, privilege escalation in admin role.
- How it works: draw DFD -> mark trust boundaries -> enumerate STRIDE per flow/store/process -> rank likelihood/impact -> choose mitigations -> track as engineering work.
- Tradeoffs: lightweight models find design flaws early, but can become check-the-box if not tied to decisions; depth should match risk.
- Real-world usage: design reviews, compliance evidence, payment flows, account recovery, admin tooling, data pipelines.
- Interview sentence: “I would draw trust boundaries first, then run STRIDE against each data flow and turn the top threats into concrete controls.”
- Recap: threat modeling makes security review systematic.

## Anecdotes & war stories to use
- Microsoft popularized STRIDE and data-flow threat modeling in its Security Development Lifecycle.
- Public cloud breaches often involve misconfigured storage or IAM, mapping cleanly to disclosure/elevation threats.
- Account-recovery attacks are spoofing/elevation examples because the “forgot password” flow becomes the real login.
- Upload pipelines have a long history of malware and decompression-bomb issues; DoS and tampering are practical, not theoretical.

## Things to mention / interview tips
- Start with assets and trust boundaries, not tool names.
- Use mitigations that map directly: mTLS for spoofing, signatures for tampering, audit logs for repudiation.
- Include abuse cases and insider/admin paths.
- Re-run the model after major architecture changes.

## Common mistakes to call out
- Listing generic threats without tying them to flows.
- Ignoring admin panels and batch jobs.
- Treating HTTPS as a complete mitigation for all categories.
- Not assigning owners to mitigations.

## Diagrams / visuals to draw on screen
- Data-flow diagram with trust boundaries.
- STRIDE matrix per component.
- Threat-to-mitigation table.
- Risk ranking grid: likelihood versus impact.

## Series glue
- Reference auth, PII, and secrets videos as mitigation building blocks. Next: zero-downtime patching shows how to fix discovered vulnerabilities safely. CTA: subscribe and use the GitHub STRIDE worksheet.
