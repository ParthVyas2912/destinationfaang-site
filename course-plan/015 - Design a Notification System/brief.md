# Design a Notification System (Push / SMS / Email)

| | |
|---|---|
| **Publish order** | 015 |
| **Course #** | 96 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~30 min |
| **Primary search keyword** | `design notification system` |
| **Demand** | High |

**Thumbnail text idea:** SEND RELIABLY
**One-line hook (first 15s):** Notifications fail in boring ways: duplicates, provider outages, user preferences, and retry storms.

## Learning objectives
- Design push, email, and SMS notifications with preferences and retries.
- Separate notification intent from provider delivery attempts.
- Handle dedupe, rate limits, templates, and provider outages.

## Topics & items to cover
- Requirements: send transactional and marketing notifications, user preferences, templates, multiple channels, retries, audit logs, unsubscribe compliance.
- Estimation: bursts after product events; SMS/email providers have quotas; push tokens churn.
- API/Data model: `POST /notifications`, `PUT /users/{id}/preferences`; `Notification(id, user_id, type, template_id, dedupe_key, state)`, `DeliveryAttempt(notification_id, channel, provider, status)`; shard by `user_id` or notification time buckets.
- High-level design: product emits intent event, notification service resolves preferences/templates, queue per channel, workers call APNs/FCM/Twilio/SendGrid, status callbacks update attempts.
- Deep dives/bottlenecks: idempotency via dedupe keys prevents duplicate receipts; retry with exponential backoff and DLQ handles provider failures; channel fallback rules must respect consent.
- Wrap-up: delivery is at-least-once, user-visible duplicates are prevented by idempotency and collapse keys.

## Anecdotes & war stories to use
- APNs and FCM push ecosystems show why device tokens expire and delivery is not guaranteed.
- Twilio/SendGrid-style providers expose rate limits and webhooks, forcing queue-based integration.
- Large incidents often create notification storms; status pages and incident tools throttle and batch updates.

## Things to mention / interview tips
- Say: "A notification intent is not the same as a provider attempt."
- Always include user preferences, quiet hours, and unsubscribe rules.
- Use per-provider circuit breakers and queues.
- Make templates versioned so audits can reproduce what was sent.

## Common mistakes to call out
- Calling SMS/email providers synchronously from product services.
- Retrying forever without dedupe or DLQ.
- Ignoring consent and unsubscribe laws.
- Treating push as guaranteed delivery.

## Diagrams / visuals to draw on screen
- Intent event to preference resolver to channel queues.
- Retry/DLQ state machine.
- Provider callback updating delivery attempts.

## Series glue
- Reference load-balancer health and retry lessons; point forward to autocomplete's low-latency read path. CTA: subscribe and get the repo templates.
