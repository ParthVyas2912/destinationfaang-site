# Design a Real-Time Personalization Engine

| | |
|---|---|
| **Publish order** | 118 |
| **Course #** | 124 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~32 min |
| **Primary search keyword** | `real time personalization` |
| **Demand** | Moderate |

**Thumbnail text idea:** PERSONALIZE NOW
**One-line hook (first 15s):** Personalization is not one model — it is a loop that captures behavior, scores candidates, and learns from what the user does next.
## Learning objectives
- Design a low-latency recommendation/personalization serving path.
- Separate candidate generation, ranking, feature retrieval, and feedback logging.
- Choose real-time features and sharding keys for user/item workloads.
- Explain exploration, cold start, and privacy constraints.

## Topics & items to cover
- **Requirements:** personalize homepage/feed/email in under 150 ms; support anonymous and logged-in users; log impressions/clicks; comply with privacy controls.
- **Estimation:** 50M users, 500M items/events/day; peak read QPS far exceeds write QPS; ranking needs top 100 candidates per request.
- **API/Data model:** `GET /v1/users/{user_id}/recommendations?surface=home`; `POST /v1/events`; entities `UserProfile`, `Item`, `FeatureVector`, `Impression`, `Click`; shard online user features by `user_id`, item features by `item_id`.
- **High-level design:** event collector → Kafka → stream features → feature store; candidate service from ANN/trending/social graph → ranker → business rules/diversity → response; feedback to training.
- **Deep dives/bottlenecks:** fresh intent from last clicks handled with streaming session features; cold start solved with popularity, content embeddings, and onboarding; filter bubbles managed with exploration quotas and diversity constraints.
- **Wrap-up:** metrics: CTR, conversion, dwell, long-term retention, latency, fairness, and guardrail violations.

## Anecdotes & war stories to use
- Netflix has publicly discussed recommendations as central to user experience, combining personalization with artwork and ranking.
- LinkedIn engineering has described feed ranking systems that blend candidate generation, ML ranking, and rule layers.
- TikTok-style feeds demonstrate the power and risk of rapid feedback loops from user behavior.
- E-commerce recommenders often need business constraints: inventory, margin, sponsored placements, and blocked categories.

## Things to mention / interview tips
- Say “candidate generation first, expensive ranking second.”
- Log impressions, not just clicks, or training labels are biased.
- Include exploration explicitly; otherwise the system never learns new items.
- Discuss privacy: consent, deletion, and sensitive-feature exclusion.

## Common mistakes to call out
- Ranking the entire catalog synchronously.
- Training only on clicks and ignoring non-click impressions.
- Ignoring cold-start users/items.
- Optimizing short-term CTR at the cost of user trust.

## Diagrams / visuals to draw on screen
- Two-stage recommendation pipeline.
- Real-time event-to-feature feedback loop.
- Candidate sources fan-in: ANN, trending, social, editorial.

## Series glue
- Builds on feature stores, streams, and A/B testing; next we contrast batch and streaming. CTA: subscribe and pull the recommender template from GitHub.
