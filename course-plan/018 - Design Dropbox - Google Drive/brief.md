# Design Dropbox / Google Drive — File Sync System

| | |
|---|---|
| **Publish order** | 018 |
| **Course #** | 90 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~35 min |
| **Primary search keyword** | `design dropbox` |
| **Demand** | Very High |

**Thumbnail text idea:** SYNC FILES
**One-line hook (first 15s):** Dropbox is not upload-download; it is change detection, chunking, conflict handling, and cross-device sync.

## Learning objectives
- Design file upload, metadata, sync, versioning, and conflict resolution.
- Explain chunking, deduplication, and resumable transfer.
- Model client sync across offline devices.

## Topics & items to cover
- Requirements: upload/download files, folders, sharing, sync across devices, offline edits, version history, large files, permissions.
- Estimation: large blob storage, metadata reads frequent, only changed chunks should upload.
- API/Data model: `POST /files/{id}/chunks`, `GET /sync?cursor=...`, `POST /shares`; `File(file_id, owner_id, parent_id, name, version)`, `FileVersion(version_id, file_id, chunk_hashes)`, `Chunk(hash, size, object_key)`; shard metadata by `owner_id`/namespace, chunks by hash.
- High-level design: desktop client watches filesystem, chunks file, uploads missing chunks to object storage, metadata service commits new version, sync service streams changes via cursor.
- Deep dives/bottlenecks: content-defined chunking improves dedupe for shifted edits; conflict handling creates "conflicted copy" when versions diverge; sync cursor must be durable and ordered per namespace.
- Wrap-up: blobs are immutable; metadata versions create the user-visible filesystem.

## Anecdotes & war stories to use
- Dropbox's public engineering writing highlights block-level sync and LAN sync as important product differentiators.
- Google Drive and Dropbox both expose version history, showing deletes and overwrites are metadata changes, not immediate blob deletion.
- Git's content-addressed object model is a helpful analogy for immutable chunks and hashes.

## Things to mention / interview tips
- Say: "Commit metadata only after chunks are durably uploaded."
- Use hashes for dedupe and integrity checks.
- Include sync cursors rather than asking clients to diff everything.
- Treat sharing/permissions as metadata checked on every read.

## Common mistakes to call out
- Re-uploading entire large files after tiny edits.
- Overwriting conflicting offline edits silently.
- Storing folder paths as the only identity.
- Deleting chunks immediately while versions still reference them.

## Diagrams / visuals to draw on screen
- Chunk upload and metadata commit two-phase flow.
- Sync cursor timeline across two devices.
- File/version/chunk data model.

## Series glue
- Reference caching and media storage; point forward to payments where idempotent commits become even stricter. CTA: subscribe and download repo diagrams.
