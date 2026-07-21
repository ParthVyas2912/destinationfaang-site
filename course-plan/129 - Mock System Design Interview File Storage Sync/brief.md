# Mock System Design Interview: File Storage & Sync

| | |
|---|---|
| **Publish order** | 129 |
| **Course #** | MOCK2 |
| **Module** | M10 — Mock Interview & Practice |
| **Type** | mock |
| **Target length** | ~55 min |
| **Primary search keyword** | `mock system design interview` |
| **Demand** | High |

**Thumbnail text idea:** SYNC FILES
**One-line hook (first 15s):** File sync interviews are won by talking about chunks, versions, conflicts, and watches — not by saying ‘upload to S3.’
## Learning objectives
- Practice a full file storage and sync interview arc.
- Design metadata, blob storage, chunking, and device sync.
- Handle conflicts, offline edits, deduplication, and large files.
- Self-score using interview rubric signals.

## Topics & items to cover
- 0-5 min clarify: Dropbox/Drive style? files/folders, sharing, offline sync, version history, max file size.
- 5-10 requirements: upload/download, list folders, sync across devices, share links; p95 metadata reads fast, blob transfer resumable.
- 10-15 estimation: active users, files/user, average file/chunk size, metadata QPS, object storage growth; rubric: separates metadata from blob bytes.
- 15-23 APIs/data: `POST /files/init`, `PUT /chunks/{hash}`, `POST /files/commit`, `GET /changes?cursor`; `FileNode`, `FileVersion`, `Chunk`, `DeviceCursor`, `ShareAcl`; shard metadata by `user_id`/namespace.
- 23-38 design: client watcher → sync engine → metadata service → object store → change log; clients poll/stream changes with cursors.
- 38-50 deep dives: content-defined chunking and hash dedupe; conflict resolution with version vectors/last-writer plus conflicted copy; resumable upload and idempotent commits.
- 50-55 wrap: metrics: sync lag, conflict rate, chunk reuse, metadata latency, durability.

## Anecdotes & war stories to use
- Dropbox famously used block-level sync and LAN sync ideas to improve user-perceived performance.
- Git-style content addressing is a useful mental model for deduplicated immutable chunks.
- Cloud drives often surface “conflicted copy” rather than silently overwriting offline edits.
- Large object stores provide durability, but the hard product behavior lives in metadata and sync clients.

## Things to mention / interview tips
- Say “metadata DB is strongly consistent; blobs are immutable in object storage.”
- Use a monotonically increasing change log cursor per namespace.
- Include checksums for every chunk.
- Discuss ACL changes and shared folder propagation.

## Common mistakes to call out
- Re-uploading whole multi-GB files for tiny edits.
- Ignoring offline concurrent edits.
- Storing file bytes in the relational metadata DB.
- Forgetting deletion tombstones for sync.

## Diagrams / visuals to draw on screen
- Client sync state machine.
- File version mapped to ordered chunk hashes.
- Change log and device cursor diagram.

## Series glue
- Builds on object storage, hashing, consistency, and queues; next mock is checkout. CTA: subscribe and use the repo checklist while practicing.
