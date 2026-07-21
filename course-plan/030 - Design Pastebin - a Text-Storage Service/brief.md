# Design Pastebin / a Text-Storage Service

| | |
|---|---|
| **Publish order** | 030 |
| **Course #** | 89 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~22 min |
| **Primary search keyword** | `design pastebin` |
| **Demand** | High |

**Thumbnail text idea:** PASTE AT SCALE
**One-line hook (first 15s):** Pastebin looks tiny: save text, return a short link. The interview gets interesting when links are hot, abusive, expiring, and must never lose data.

## Learning objectives
- Design create/read flows for immutable text blobs with short URLs.
- Choose storage layout, ID generation, caching, expiration, and abuse controls.
- Estimate storage and bandwidth for paste workloads.
- Explain consistency and deletion behavior for public links.

## Topics & items to cover
- **Step 1 — Requirements:** create paste, read by alias, optional custom alias, TTL/private flag, size limit, delete/report abuse. Exclude collaborative editing. Reads must be low-latency; writes durable.
- **Step 2 — Estimation:** assume 10M pastes/day average 5KB = ~50GB/day raw; reads 10x writes, with viral hot pastes. TTL reduces long-term storage; compression helps text.
- **Step 3 — API/Data model:** `POST /pastes {content, ttl, visibility, custom_alias}`, `GET /{code}`, `DELETE /pastes/{id}`. Metadata table keyed by `code`; blob/object storage for larger content; indexes on owner and expiry.
- **Step 4 — HLD:** API gateway → paste service → ID generator → metadata DB → object store; Redis/CDN for popular public pastes; async scanner for malware/PII/abuse; expiry sweeper.
- **Step 5 — Deep dives:** 1) ID generation: base62 random 7-10 chars, reserve custom aliases with uniqueness constraint. 2) Hot links: cache immutable content with TTL; purge on deletion/abuse. 3) Abuse/privacy: size limits, rate limits, scanning pipeline, private unguessable links.
- **Step 6 — Wrap-up:** choose simplicity: immutable blobs avoid edit conflicts; explain deletion propagation tradeoff.

## Anecdotes & war stories to use
- TinyURL/bit.ly-style designs show why random short codes need collision handling and abuse prevention.
- GitHub Gist is a good contrast: versioned, user-owned snippets are more complex than anonymous immutable pastes.
- Cloudflare and CDN cache-purge discussions illustrate that removing public cached content is harder than serving it.
- Public paste sites have long been used for credential leaks, so scanning and takedown flows are product requirements.

## Things to mention / interview tips
- Say “metadata in DB, content in object storage” unless small-content inline storage is justified.
- Treat custom aliases as scarce names requiring reservation and normalization.
- Use immutable content hashes for dedupe only if privacy/abuse implications are acceptable.
- Mention soft delete plus asynchronous hard delete from object storage and CDN.

## Common mistakes to call out
- Storing large blobs in a hot relational row without size limits.
- Sequential IDs that make private pastes enumerable.
- Forgetting TTL expiry indexes and background cleanup.
- Caching private pastes in shared CDN paths.

## Diagrams / visuals to draw on screen
- Create/read sequence with metadata DB and object store.
- Base62 code generation and collision retry loop.
- Hot paste served from CDN while origin remains source of truth.

## Series glue
- Reference TinyURL, Caching, and Rate Limiter; next CDN videos expand the edge-serving part. CTA: subscribe and grab API/schema files on GitHub.
