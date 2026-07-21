# Design YouTube / Netflix — Video Streaming System

| | |
|---|---|
| **Publish order** | 012 |
| **Course #** | 93 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~45 min |
| **Primary search keyword** | `design youtube` |
| **Demand** | Very High |

**Thumbnail text idea:** VIDEO PIPELINE
**One-line hook (first 15s):** YouTube is less about storing videos and more about turning one upload into thousands of watchable chunks worldwide.

## Learning objectives
- Design upload, transcoding, storage, metadata, and playback for video.
- Explain adaptive bitrate streaming, manifests, chunks, and CDN caching.
- Handle recommendations/search lightly while focusing on streaming core.

## Topics & items to cover
- Requirements: upload video, process into formats, watch with seek, comments/likes optional, creator dashboard, copyright/moderation hooks.
- Estimation: video bytes dwarf metadata; playback traffic is globally CDN-heavy; upload processing is compute-intensive.
- API/Data model: `POST /uploads`, `GET /videos/{id}/manifest`, `GET /watch/{id}`; `Video(video_id, owner_id, status, title)`, `Rendition(video_id, codec, resolution, bitrate, object_key)`, comments/counters separate; shard metadata by `video_id`.
- High-level design: resumable upload to object storage, queue transcode jobs, workers create HLS/DASH chunks and manifests, CDN serves chunks, metadata service powers watch page.
- Deep dives/bottlenecks: adaptive bitrate chooses chunk quality per bandwidth; transcode pipeline must be idempotent/retryable; cache hit ratio and regional origin shielding control cost.
- Wrap-up: distinguish YouTube user-generated upload pipeline from Netflix licensed catalog but same chunk/CDN playback principles.

## Anecdotes & war stories to use
- Netflix Open Connect places appliances inside ISP networks to reduce latency and transit cost.
- YouTube's early scaling pushed heavy investment in transcoding, storage, and global delivery.
- Major CDN outages at providers such as Fastly have shown how much of the internet depends on edge delivery.

## Things to mention / interview tips
- Say: "Playback must never depend on transcode workers; it serves immutable chunks from CDN."
- Draw manifest plus 2-6 second chunks.
- Include upload status: uploaded, processing, ready, failed, blocked.
- Mention DRM/copyright only as extensions unless asked.

## Common mistakes to call out
- Serving videos directly from application servers.
- Blocking upload response until all renditions finish.
- Ignoring seek behavior and adaptive bitrate.
- Mixing metadata DB scaling with video object storage scaling.

## Diagrams / visuals to draw on screen
- Upload-to-transcode pipeline.
- HLS/DASH manifest pointing to chunk renditions.
- CDN edge cache with origin shielding.

## Series glue
- Reference Instagram media processing and rate limiting for upload protection; point forward to Uber's real-time geospatial matching. CTA: subscribe and download diagrams from GitHub.
