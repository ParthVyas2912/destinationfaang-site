# Design a Web Crawler (Google-Scale)

| | |
|---|---|
| **Publish order** | 023 |
| **Course #** | 112 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~35 min |
| **Primary search keyword** | `design web crawler` |
| **Demand** | High |

**Thumbnail text idea:** CRAWL THE WEB
**One-line hook (first 15s):** A web crawler is a polite distributed scheduler before it is a downloader.

## Learning objectives
- Design a distributed crawler with frontier scheduling, politeness, and dedupe.
- Model URL discovery, fetch, parse, and indexing pipelines.
- Handle robots.txt, canonicalization, and freshness recrawl.

## Topics & items to cover
- Requirements: crawl public web pages, respect robots.txt, avoid duplicate URLs/content, prioritize freshness/importance, feed indexer.
- Estimation: billions of URLs, network-bound fetchers, per-host politeness limits dominate throughput.
- API/Data model: internal `UrlTask(url, host, priority, next_fetch_at)`, `Page(url_hash, content_hash, fetched_at, status)`, link graph edges; shard frontier by host hash so politeness is enforceable.
- High-level design: URL frontier schedules tasks, fetchers download pages, parser extracts links/content, dedupe service canonicalizes URLs and hashes content, index pipeline stores documents.
- Deep dives/bottlenecks: per-host queues and delay prevent hammering sites; canonicalization normalizes schemes/trailing slashes/query params; recrawl priority uses change frequency and page importance.
- Wrap-up: crawler quality is scheduling quality, not just more fetch threads.

## Anecdotes & war stories to use
- Google's original architecture separated crawling, indexing, and PageRank/link analysis, making the web graph central.
- robots.txt is an industry convention crawlers are expected to respect, even though enforcement is voluntary.
- Search engines fight duplicate content and canonical URLs constantly because the same page can appear under many URLs.

## Things to mention / interview tips
- Say: "The frontier is partitioned by host so I can enforce politeness locally."
- Always include robots.txt caching and user-agent rules.
- Separate URL dedupe from content dedupe.
- Mention backoff for errors and crawl traps/calendars.

## Common mistakes to call out
- Using one global FIFO queue with no per-host limits.
- Crawling before checking robots.txt.
- Treating URL strings as unique pages without canonicalization.
- Recrawling everything at the same frequency.

## Diagrams / visuals to draw on screen
- Frontier to fetcher to parser to indexer pipeline.
- Per-host priority queues with next-fetch time.
- URL/content dedupe flow.

## Series glue
- Reference consistency for stale indexes; point forward to SQL vs NoSQL when choosing stores for frontier, pages, and indexes. CTA: subscribe and see repo diagrams.
