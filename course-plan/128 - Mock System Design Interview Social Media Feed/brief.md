# Mock System Design Interview: Social Media Feed

| | |
|---|---|
| **Publish order** | 128 |
| **Course #** | MOCK1 |
| **Module** | M10 — Mock Interview & Practice |
| **Type** | mock |
| **Target length** | ~55 min |
| **Primary search keyword** | `mock system design interview` |
| **Demand** | Very High |

**Thumbnail text idea:** FEED INTERVIEW
**One-line hook (first 15s):** In this mock, watch how a strong candidate turns ‘design a social feed’ into requirements, fanout tradeoffs, ranking, and reliability without panicking.
## Learning objectives
- Practice a complete 55-minute feed design interview.
- Compare fanout-on-write, fanout-on-read, and hybrid timelines.
- Discuss ranking, freshness, celebrity users, and read latency.
- Use rubric language to self-score.

## Topics & items to cover
- Opening 0-5 min: clarify feed type, followers vs friends, posts/media, ranking vs chronological, scale; scoring callout: asks product constraints before drawing boxes.
- Requirements 5-10: create post, follow/unfollow, home timeline, notifications optional; non-functional p95 under 200 ms for feed reads, eventual consistency acceptable.
- Estimation 10-15: DAU, posts/day, fanout volume, media stored separately; rubric: estimates identify read-heavy workload.
- APIs/data 15-23: `POST /posts`, `GET /feed`, `POST /follow`; tables `User`, `Post`, `FollowEdge`, `TimelineEntry`; shard by `user_id`, post IDs time-sortable.
- Design 23-38: write path stores post then queue fanout workers to timeline cache; read path merges precomputed timeline, ads, ranking features; media via object store/CDN.
- Deep dives 38-50: celebrity fanout switch to pull; ranking features and impression logging; cache invalidation and backpressure.
- Wrap 50-55: summarize tradeoffs and metrics: feed latency, fanout lag, freshness, engagement, error rate.

## Anecdotes & war stories to use
- Twitter/X timeline discussions popularized fanout tradeoffs for celebrity accounts.
- Facebook/Meta feed ranking shows feeds evolved from chronological delivery to ML ranking.
- LinkedIn engineering has described feed systems combining candidate generation and ranking.
- Interviewers often reward candidates who explicitly handle “Lady Gaga problem” celebrity fanout.

## Things to mention / interview tips
- Say “I’ll optimize for feed reads because users read far more than they post.”
- Draw separate post storage and timeline materialization.
- Explain why ranking needs exposure logging.
- Call out eventual consistency for new posts in followers’ feeds.

## Common mistakes to call out
- Fully normalizing the feed and joining follows/posts at read time for every request.
- Fanout-on-write for celebrities without fallback.
- Ignoring media/CDN and treating posts as only text.
- Forgetting deletes/privacy changes in cached timelines.

## Diagrams / visuals to draw on screen
- Write fanout pipeline with queue workers.
- Read path merging timeline cache and ranking service.
- Hybrid fanout decision for normal vs celebrity users.

## Series glue
- References earlier cache, queue, ranking, and personalization videos; next mock is file sync. CTA: subscribe and use the GitHub rubric to score yourself.
