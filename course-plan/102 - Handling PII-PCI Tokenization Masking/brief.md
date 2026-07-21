# Handling PII/PCI: Tokenization & Masking

| | |
|---|---|
| **Publish order** | 102 |
| **Course #** | 63 |
| **Module** | M06 — Security, Observability & FinOps |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `pii tokenization` |
| **Demand** | Moderate |

**Thumbnail text idea:** PROTECT THE DATA
**One-line hook (first 15s):** The best way to secure sensitive data is to make sure most of your system never sees the real value.

## Learning objectives
- Distinguish PII, PCI, tokenization, masking, hashing, and encryption.
- Design a token vault for cards, SSNs, or phone numbers.
- Explain least privilege, redaction, retention, and audit trails.
- Avoid leaks through logs, analytics, search indexes, and support tools.

## Topics & items to cover
- Hook: encrypting a card in every microservice still puts every microservice in scope.
- Definition: tokenization replaces sensitive values with surrogate tokens; masking hides display; encryption protects recoverable data.
- Worked example: checkout posts PAN to PCI vault; vault returns `tok_card_abc`, brand, and last4; order service stores token/last4; support sees `****4242`; only payment service can detokenize for charge/refund.
- How it works: classify data -> minimize collection -> vault/KMS -> token references in DBs -> redaction in logs/events -> retention/deletion workflow.
- Tradeoffs: vault reduces blast radius but adds latency/dependency; hashing helps lookup but not display; masking protects UI but not storage.
- Real-world usage: payment processors, healthcare identifiers, CRM phone/email, data warehouses, support consoles.
- Interview sentence: “Minimize collection, tokenize at the boundary, keep raw values in a hardened vault, and propagate only tokens plus safe display fields.”
- Recap: sensitive-data design reduces scope.

## Anecdotes & war stories to use
- PCI DSS pushed merchants toward hosted payment fields/tokenization so core apps avoid PAN handling.
- Stripe documents tokenized payment methods so merchants charge without storing card numbers.
- Debug logging incidents often expose PII because request bodies are captured before redaction.
- Warehouses become accidental PII sinks when events include emails, phone numbers, or free text.

## Things to mention / interview tips
- Classify data before choosing controls.
- Audit who detokenized, why, when, and from where.
- Redact at SDK/collector level, not only dashboards.
- Discuss retention/deletion workflows without pretending to give legal advice.

## Common mistakes to call out
- Confusing masking with security while raw data remains accessible.
- Hashing low-entropy phone numbers without salt/pepper and rate limits.
- Sending PII to logs, metrics labels, traces, or analytics.
- Giving support tools unrestricted detokenization.

## Diagrams / visuals to draw on screen
- Token vault boundary with app storing token + last4.
- Data-flow map highlighting PII sinks.
- Logging pipeline with redaction before ingestion.
- Detokenization approval/access path.

## Series glue
- Reference abuse prevention because risk systems collect sensitive signals. Next: secrets and key rotation protect vaults and services. CTA: subscribe and check GitHub for the sensitive-data checklist.
