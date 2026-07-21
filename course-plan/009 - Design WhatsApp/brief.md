# Design WhatsApp — Real-Time Chat System Design

| | |
|---|---|
| **Publish order** | 009 |
| **Course #** | 95 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~40 min |
| **Primary search keyword** | `design whatsapp` |
| **Demand** | Very High |

**Thumbnail text idea:** CHAT AT SCALE
**One-line hook (first 15s):** WhatsApp design is really about presence, ordering, offline delivery, and surviving mobile networks.

## Learning objectives
- Design one-to-one and group messaging with offline delivery.
- Explain ordering, acknowledgements, presence, and push notification boundaries.
- Pick storage and partitioning for conversation history.

## Topics & items to cover
- Requirements: send/receive messages, delivery/read receipts, groups, media, presence, offline sync, end-to-end encryption constraints.
- Estimation: many small writes, long-lived connections, mobile reconnects, group fan-out can dominate.
- API/Data model: persistent WebSocket/MQTT connection; `POST /messages` fallback; `Message(conversation_id, msg_id, sender_id, ciphertext, sent_at)`, `ConversationMember`; shard by `conversation_id` for ordering, with inbox indexes by `user_id`.
- High-level design: gateway maintains connections, message service persists append-only log, delivery service fans out to online devices or offline queues, push service wakes mobile apps.
- Deep dives/bottlenecks: per-conversation ordering via sequence numbers; offline delivery and multi-device ack state; group fan-out using member snapshots and batched delivery.
- Wrap-up: emphasize at-least-once delivery plus idempotent client dedupe rather than pretending exactly-once messaging.

## Anecdotes & war stories to use
- WhatsApp is well known for using Erlang/BEAM to handle huge numbers of concurrent connections with a relatively small team.
- Signal's end-to-end encryption model shows servers can route opaque ciphertext while still handling delivery metadata.
- Discord has publicly discussed evolving message storage from MongoDB to Cassandra and later ScyllaDB for scale and latency.

## Things to mention / interview tips
- Say: "The server guarantees durable, ordered append per conversation; clients dedupe by message ID."
- Separate presence from message storage; presence is soft state.
- Discuss reconnect sync: client sends last seen sequence per conversation.
- Mention encryption limits server-side search and moderation.

## Common mistakes to call out
- Claiming exactly-once delivery across mobile networks.
- Using one global message ordering sequence.
- Treating push notifications as message delivery.
- Forgetting group membership changes affect fan-out.

## Diagrams / visuals to draw on screen
- WebSocket gateway to message log to delivery workers.
- Offline queue and ack/read receipt state machine.
- Group message fan-out with conversation sequence numbers.

## Series glue
- Reference Instagram media handling for attachments and Twitter fan-out for groups; point forward to CAP tradeoffs during partitions. CTA: subscribe and check the GitHub repo.
