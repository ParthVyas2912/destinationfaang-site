# Design an Image CDN (Pinterest-Style)

| | |
|---|---|
| **Publish order** | 032 |
| **Course #** | 91 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~28 min |
| **Primary search keyword** | `design image cdn` |
| **Demand** | Moderate |

**Thumbnail text idea:** IMAGE EDGE
**One-line hook (first 15s):** Pinterest-style image delivery is a CDN problem plus resizing, metadata, hot pins, copyright takedowns, and billions of tiny variants.

## Learning objectives
- Design upload, transform, store, and serve paths for image-heavy products.
- Choose URL structure, cache keys, variants, and object storage layout.
- Handle hot images, resizing queues, metadata, moderation, and deletion.
- Explain CDN invalidation and origin protection for media.

## Topics & items to cover
- **Step 1 — Requirements:** upload image, generate thumbnails/sizes, serve by device, metadata/pin association, delete/report. Exclude full social feed ranking. Low latency global reads; durable originals.
- **Step 2 — Estimation:** 100M images/day at compressed MB scale implies object storage first. Reads dwarf writes; popular pins create extreme edge-cache skew. Derivatives multiply storage by variant count.
- **Step 3 — API/Data model:** `POST /images`, `GET /images/{id}?w=600&format=webp`, `DELETE /images/{id}`. `Image(id, owner, original_uri, status, checksum)`, `Variant(image_id,width,format,uri)`, `Pin` references image.
- **Step 4 — HLD:** upload service → object store original → metadata DB → transform queue/workers → derivative bucket → CDN; moderation scanner async; signed upload URLs for large files.
- **Step 5 — Deep dives:** 1) Variant explosion: allow fixed width ladder, normalize params, cache key includes width/format. 2) Hot images: CDN + origin shield + precompute popular variants. 3) Deletion/takedown: mark unavailable in metadata, purge CDN by surrogate key, async delete objects.
- **Step 6 — Wrap-up:** originals are source of truth; derived images are reproducible cache.

## Anecdotes & war stories to use
- Pinterest engineering has written about image-heavy infrastructure and efficient media serving for discovery products.
- Facebook/Meta’s Haystack photo storage paper is a classic story about reducing metadata overhead for massive photo storage.
- Cloudinary/imgproxy-style services show how dynamic transformations can become expensive without normalized variants.
- CDN purge stories from Fastly/Cloudflare demonstrate why deletion workflows need metadata gating, not only cache purge.

## Things to mention / interview tips
- State that user-supplied width/height must be quantized to approved variants.
- Use content hashes for dedupe only after considering privacy and ownership semantics.
- Discuss EXIF stripping, malware scanning, and moderation as part of upload.
- Make CDN cache key explicit: path + normalized dimensions + format + version.

## Common mistakes to call out
- Generating every possible crop synchronously during upload.
- Letting arbitrary query params create unbounded CDN/object variants.
- Treating derived thumbnails as irreplaceable primary data.
- Forgetting takedown consistency at edge caches.

## Diagrams / visuals to draw on screen
- Upload pipeline from signed URL to transform workers.
- Variant ladder table and cache-key normalization.
- CDN miss path with origin shield and derivative generation.

## Series glue
- Builds directly on CDN and Pastebin storage patterns; forward to Message Queues because transforms are async. CTA: subscribe and get image URL examples in GitHub.
