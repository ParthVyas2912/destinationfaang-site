# Design a Scalable Video Processing Pipeline

| | |
|---|---|
| **Publish order** | 125 |
| **Course #** | 126 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~32 min |
| **Primary search keyword** | `design video processing` |
| **Demand** | Moderate |

**Thumbnail text idea:** VIDEO FACTORY
**One-line hook (first 15s):** Video processing looks like upload-and-play, but behind the scenes it is a distributed factory for transcoding, thumbnails, captions, and CDN delivery.
## Learning objectives
- Design upload, transcoding, packaging, storage, and playback flows.
- Estimate storage and compute for multiple renditions.
- Handle retries, idempotency, and hot viral videos.
- Explain queues, chunking, and CDN strategy.

## Topics & items to cover
- **Requirements:** upload large videos, generate 240p-4K renditions, thumbnails, captions, DRM optional, playback via CDN; support resumable upload.
- **Estimation:** 100K uploads/day, average 500MB source, 5 renditions roughly multiplies storage; transcoding CPU/GPU is the bottleneck.
- **API/Data model:** `POST /videos/uploads`, `PUT /uploads/{id}/parts`, `POST /videos/{id}/publish`, `GET /videos/{id}/playback`; `Video`, `UploadPart`, `TranscodeJob`, `Rendition`, `Manifest`; shard metadata by `video_id`, store objects by content hash/path prefix.
- **High-level design:** upload service → object storage → metadata DB → job queue → transcode workers → packaging (HLS/DASH) → CDN → player analytics.
- **Deep dives/bottlenecks:** resumable multipart upload with checksums; idempotent transcode jobs and dead-letter queues; viral playback solved by CDN prewarm, adaptive bitrate manifests, and origin shielding.
- **Wrap-up:** metrics: processing time, failure rate, startup latency, rebuffering, CDN hit ratio.

## Anecdotes & war stories to use
- YouTube and Netflix engineering have long emphasized adaptive bitrate streaming to handle variable networks.
- FFmpeg is a standard building block across many video pipelines.
- Large platforms use CDNs because origin storage cannot serve viral playback directly.
- User-generated video sites commonly separate upload completion from “ready to watch” processing states.

## Things to mention / interview tips
- State that upload and processing are asynchronous.
- Include content validation: codec, duration, malware scan, policy checks.
- Use idempotency keys for upload completion and job retries.
- Mention HLS/DASH manifests and segment-based delivery.

## Common mistakes to call out
- Serving original uploads directly from object storage.
- Blocking the upload request until all transcodes finish.
- Retrying transcodes without dedupe, creating duplicate renditions.
- Ignoring playback QoE metrics.

## Diagrams / visuals to draw on screen
- Upload state machine.
- Queue-based transcode worker pool.
- HLS manifest pointing to bitrate segments on CDN.

## Series glue
- Connects queues, object storage, CDNs, and batch processing; next we use similar indexing ideas for vector search. CTA: subscribe and use the repo’s video pipeline checklist.
