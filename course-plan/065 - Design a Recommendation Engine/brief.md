# Design a Recommendation Engine (Netflix / YouTube)

| | |
|---|---|
| **Publish order** | 065 |
| **Course #** | 119 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~35 min |
| **Primary search keyword** | `design recommendation system` |
| **Demand** | High |

**Thumbnail text idea:** RECOMMEND THIS
**One-line hook (first 15s):** The Netflix row of thumbnails is not one algorithm—it’s a serving system, feedback loop, and ranking factory.

## Learning objectives
- Design recommendations with candidate generation, ranking, and feedback loops.
- Model users, items, interactions, embeddings, features, and experiments.
- Separate offline training, nearline updates, online serving, and evaluation.

## Topics & items to cover
- Requirements: recommend videos/products under 100ms, personalize, handle cold start, support A/B tests, filter unsafe/unavailable content.
- Estimation: 200M users, 100M items, billions of interactions/day. Shard feature stores by `user_id`; partition item/vector indexes by embedding space/category.
- API/Data model: `GET /recommendations?user_id&surface=home`, `POST /events`; entities: UserProfile, Item, Interaction, CandidateSet, FeatureVector, ModelVersion, Experiment.
- High-level design: event collection → lake/warehouse → training pipeline creates embeddings/models → candidate indexes → online service fetches user features, generates thousands of candidates, ranks top N, applies filters/diversity, logs impressions/clicks.
- Deep dives/bottlenecks: cold start using popularity/content features; feedback loops managed with exploration and diversity constraints; freshness via nearline stream updates for “watched five minutes ago.”
- Wrap-up: collect, train, serve, measure, retrain.

## Anecdotes & war stories to use
- The Netflix Prize made collaborative filtering famous, while production systems need ranking and operations.
- YouTube’s public recommendation papers describe candidate generation followed by ranking.
- TikTok-style feeds highlight rapid feedback loops shaping user experience.

## Things to mention / interview tips
- Split candidate generation from ranking.
- Log impressions, not just clicks.
- Include experiment assignment and model version in logs.

## Common mistakes to call out
- Running one model over all items online.
- Ignoring cold start.
- Training on clicks without exposure data.

## Diagrams / visuals to draw on screen
- Offline/nearline/online architecture.
- Candidate → ranker → re-ranker/filter funnel.
- A/B feedback loop.

## Series glue
- Uses streams, analytics, and feature-store ideas. Next: microservice boundaries. Subscribe and use GitHub resources.
