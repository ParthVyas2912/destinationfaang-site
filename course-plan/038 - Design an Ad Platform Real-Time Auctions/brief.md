# Design an Ad Platform & Real-Time Auctions (RTB)

| | |
|---|---|
| **Publish order** | 038 |
| **Course #** | 100 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~35 min |
| **Primary search keyword** | `design ad system` |
| **Demand** | Moderate |

**Thumbnail text idea:** 100MS AUCTION
**One-line hook (first 15s):** An ad auction is a tiny stock exchange inside a web page load: request, bid, rank, fraud-check, and log before the user scrolls past.

## Learning objectives
- Design real-time bidding request flow under strict latency budgets.
- Model campaigns, creatives, targeting, budgets, bids, impressions, and clicks.
- Explain pacing, frequency caps, auction ranking, and event pipelines.
- Handle fraud, reporting, and consistency for budgets.

## Topics & items to cover
- **Step 1 — Requirements:** receive ad request, select eligible ads, run auction, return creative, track impression/click/conversion, enforce budgets/frequency caps. Exclude full ML training. P99 latency tight; billing/audit must be accurate.
- **Step 2 — Estimation:** millions of QPS globally, each request fans out to candidate campaigns. Logs are append-heavy; reporting is eventually consistent. Budget spend updates are high-contention.
- **Step 3 — API/Data model:** `POST /adrequest`, `GET /creative/{id}`, tracking pixels `/impression`, `/click`. Entities: Campaign, AdGroup, Creative, TargetingRule, Bid, Budget, UserFrequency, AuctionLog.
- **Step 4 — HLD:** edge ad server → targeting index/cache → auction/ranking service → budget/frequency service → creative CDN; Kafka logs to billing, reporting, fraud, ML.
- **Step 5 — Deep dives:** 1) Latency: precompute targeting indexes in memory; local budget caches with async reconciliation. 2) Pacing/frequency: token buckets by campaign/user segment; approximate counters. 3) Event integrity: dedupe impression/click ids, fraud scoring, immutable logs for billing.
- **Step 6 — Wrap-up:** trade exact global budget for low-latency local decisions plus reconciliation guardrails.

## Anecdotes & war stories to use
- Google’s ad systems and papers around large-scale auctions/ranking are the canonical industry backdrop.
- OpenRTB is a real industry protocol for bid requests/responses in programmatic advertising.
- Facebook/Meta and Google public materials emphasize auction ranking using bid plus predicted quality/action rates.
- Kafka-style immutable logs are common in ad tech because billing, reporting, and ML all consume the same events differently.

## Things to mention / interview tips
- Put a concrete latency budget on each stage: network, targeting, ranking, creative response.
- Say “auction log is append-only and is the source for billing/reporting.”
- Budget enforcement can be approximate in serving but exact in reconciliation.
- Discuss privacy/consent and regional targeting constraints briefly.

## Common mistakes to call out
- Doing database joins in the live auction path.
- Ignoring frequency caps and budget overspend.
- Counting client clicks without dedupe/fraud filtering.
- Treating reporting dashboards as strongly consistent with live serving.

## Diagrams / visuals to draw on screen
- Real-time ad request path with millisecond budget labels.
- Candidate filtering funnel: targeting → pacing → auction → creative.
- Event pipeline from impression/click logs to billing/reporting/ML.

## Series glue
- Reference caching, event streams, and API Gateway; next cache-stampede video explains a failure mode ad systems must avoid. CTA: subscribe and get the auction schema on GitHub.
