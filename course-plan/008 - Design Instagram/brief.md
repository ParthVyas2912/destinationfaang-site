# Design Instagram — System Design Interview

| | |
|---|---|
| **Publish order** | 008 |
| **Course #** | 92 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~40 min |
| **Primary search keyword** | `design instagram` |
| **Demand** | Very High |

**Thumbnail text idea:** PHOTO FEED
**One-line hook (first 15s):** Instagram is three systems at once: media upload, social graph fan-out, and a feed that must feel instant.

## Learning objectives
- Design upload, storage, feed generation, and engagement paths for Instagram.
- Choose data models for posts, followers, likes, comments, and media metadata.
- Explain fan-out, CDN delivery, and image/video processing bottlenecks.

## Topics & items to cover
- Requirements: upload photo/video, follow users, home feed, profile grid, likes/comments, stories optional, privacy and deletes.
- Estimation: media dominates storage/bandwidth; feed reads dominate writes; thumbnails and multiple resolutions multiply objects.
- API/Data model: `POST /media`, `POST /posts`, `GET /feed`, `POST /posts/{id}/likes`; `Post(post_id, author_id, media_ids, caption)`, `Follow(follower_id, followee_id)`, `FeedItem(user_id, post_id, score)`; shard posts by `author_id/post_id`, feed by `user_id`.
- High-level design: upload service writes to object storage, processing workers create renditions, metadata DB stores posts, fan-out service populates feed cache, CDN serves media.
- Deep dives/bottlenecks: large media processing is async with status states; feed fan-out handles celebrity accounts via hybrid pull; counters/likes use denormalized counters with eventual correction.
- Wrap-up: clarify consistency choices for new post visibility, deletes, and private accounts.

## Anecdotes & war stories to use
- Instagram famously scaled rapidly on a small engineering team before the Facebook acquisition, relying heavily on pragmatic Postgres, caching, and operational discipline.
- Instagram engineering has discussed feed ranking and machine learning replacing purely chronological feeds.
- Facebook/Meta's photo infrastructure and CDN investments show why media delivery is a separate system from metadata.

## Things to mention / interview tips
- Say: "Media bytes go to object storage/CDN; relational metadata is not the media store."
- Treat upload completion and post publication as two different states.
- Ask whether the feed is ranked, chronological, or mixed.
- Include privacy, blocks, and delete propagation.

## Common mistakes to call out
- Storing image blobs in the main database.
- Generating thumbnails synchronously in the request.
- Ignoring celebrity fan-out and private-account filtering.
- Counting likes with a single hot row.

## Diagrams / visuals to draw on screen
- Upload pipeline: client to object store to processing queue.
- Feed generation with fan-out workers and CDN media fetch.
- Metadata tables and counter aggregation path.

## Series glue
- Reference Twitter for feed fan-out and consistent hashing for cache/storage distribution; point forward to WhatsApp's real-time delivery. CTA: subscribe and use the GitHub repo brief templates.
