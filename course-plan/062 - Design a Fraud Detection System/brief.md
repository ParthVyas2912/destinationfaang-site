# Design a Fraud Detection System

| | |
|---|---|
| **Publish order** | 062 |
| **Course #** | 122 |
| **Module** | M09 — System Design Case Studies |
| **Type** | case |
| **Target length** | ~32 min |
| **Primary search keyword** | `design fraud detection` |
| **Demand** | Moderate |

**Thumbnail text idea:** CATCH FRAUD FAST
**One-line hook (first 15s):** Fraud detection is a race: approve good users instantly while stopping bad transactions before money leaves.

## Learning objectives
- Design real-time and offline fraud detection for payments/marketplaces.
- Combine rules, features, ML models, graph signals, and human review.
- Handle latency, false positives, feedback labels, and adversarial behavior.

## Topics & items to cover
- Requirements: score card transactions under 100ms, block high-risk, challenge medium-risk, analyst review, learn from chargebacks, explain decisions.
- Estimation: 5K tx/sec average, 50K peak, hundreds of features. Shard online feature store by `account_id`; stream by `user_id/card_hash` for velocity features.
- API/Data model: `POST /transactions/{id}/score`, `POST /reviews/{id}/decision`; entities: Transaction, User, Merchant, DeviceFingerprint, FeatureVector, Rule, ModelVersion, Case.
- High-level design: payment service → fraud scoring API → online feature store + rules + ML model → decision; Kafka events feed feature aggregation, graph analysis, model training, and case management.
- Deep dives/bottlenecks: fresh velocity features like “5 cards in 10 minutes”; model/rule versioning with shadow evaluation; false-positive control via reason codes and review queue.
- Wrap-up: optimize risk-adjusted decisioning, not raw model accuracy.

## Anecdotes & war stories to use
- PayPal’s early fraud systems are often cited as essential to its survival.
- Card networks perform authorization-time risk scoring before approval.
- Marketplaces use device and graph signals because identity fields are easy to fake.

## Things to mention / interview tips
- Ask for latency and false-positive tolerance.
- Separate online scoring from offline training.
- Log model version and reason codes for every decision.

## Common mistakes to call out
- Designing only an offline batch model.
- Ignoring chargeback labels arriving weeks later.
- Optimizing AUC while blocking good users.

## Diagrams / visuals to draw on screen
- Real-time scoring path with feature store.
- Chargeback/review feedback loop.
- User-device-card graph for fraud rings.

## Series glue
- Combines streams and feature stores. Next: outbox/exactly-once. Subscribe and use GitHub diagrams.
