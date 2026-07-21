# Design Twitter / X — System Design Interview

| | |
|---|---|
| **Publish order** | 006 |
| **Course #** | 94 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~35 min |
| **Primary search keyword** | `design twitter` |
| **Demand** | Very High |

**Thumbnail text idea:** FANOUT HELL
**One-line hook (first 15s):** Twitter is not a post table; it is a fan-out, ranking, and celebrity hot-key problem disguised as a feed.

## Learning objectives
- Separate tweet creation, social graph storage, timeline fan-out, and ranking.
- Explain fan-out-on-write versus fan-out-on-read with celebrity exceptions.
- Design a feed path that tolerates hot users, media, and eventual consistency.

## Topics & items to cover
- Requirements: post tweets, follow/unfollow, home timeline, user timeline, likes/retweets, media attachments, low-latency reads.
- Estimation: reads dominate writes; tweets are small but timelines and media fan-out create huge derived data.
- API/Data model: `POST /tweets`, `GET /timeline/home`, `POST /follows`; entities `Tweet(tweet_id, author_id, text, media_ids)`, `Follow(follower_id, followee_id)`, `HomeTimeline(user_id, tweet_id, score, created_at)`; shard tweets by `author_id` or `tweet_id`, timelines by `user_id`.
- High-level design: write service stores tweet, publishes event, fan-out workers push to follower timeline caches, read service merges cached timeline with ads/ranking.
- Deep dives/bottlenecks: celebrity fan-out should be pull/merge at read time; timeline ranking needs precomputed candidates plus online features; media upload uses separate object storage/CDN pipeline.
- Wrap-up: justify eventual consistency for feeds but stronger consistency for follow state and deletes.

## Anecdotes & war stories to use
- Twitter's classic celebrity fan-out problem is often explained with accounts like Justin Bieber creating huge follower fan-out spikes.
- Twitter created Snowflake IDs to generate ordered unique IDs without central database coordination.
- Twitter moved through multiple timeline architectures as read volume, ranking, and real-time expectations changed.

## Things to mention / interview tips
- Say: "For normal users I fan out on write; for celebrities I fan out on read."
- Always ask if the timeline is reverse chronological or ranked.
- Mention tombstones/delete propagation for compliance and user trust.
- Keep social graph queries off the feed read path where possible.

## Common mistakes to call out
- Recomputing the home timeline from the follow graph on every request.
- Treating all users the same despite extreme follower skew.
- Forgetting media, deletes, blocks, and privacy.
- Over-indexing on perfect consistency for a feed.

## Diagrams / visuals to draw on screen
- Tweet write event feeding fan-out workers.
- Home timeline read path merging precomputed and celebrity tweets.
- Social graph storage versus timeline storage boundaries.

## Series glue
- Reference TinyURL for ID generation and hot-key thinking; point forward to consistent hashing and Instagram feeds. CTA: subscribe and use the GitHub repo templates.
