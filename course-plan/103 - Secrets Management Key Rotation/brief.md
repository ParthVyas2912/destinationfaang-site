# Secrets Management & Key Rotation

| | |
|---|---|
| **Publish order** | 103 |
| **Course #** | 60 |
| **Module** | M06 — Security, Observability & FinOps |
| **Type** | concept |
| **Target length** | ~12 min |
| **Primary search keyword** | `secrets management` |
| **Demand** | Moderate |

**Thumbnail text idea:** ROTATE THE KEYS
**One-line hook (first 15s):** A secret is not secure because it is hidden in an environment variable; it is secure when issuance, access, rotation, and revocation are designed.

## Learning objectives
- Distinguish secrets, keys, certificates, tokens, and configuration.
- Design storage, access, audit, rotation, and emergency revocation.
- Explain envelope encryption and KMS-backed workflows.
- Avoid secret leaks in logs, images, repos, and CI systems.

## Topics & items to cover
- Hook: if a leaked database password requires redeploying 80 services, the rotation design failed.
- Definition: secrets management centrally stores or brokers sensitive credentials with policy, audit, and lifecycle control.
- Worked example: API service uses workload identity to request a short-lived DB credential valid 15 minutes; credential is never committed, is cached in memory, and rotation overlaps old/new users before revocation.
- How it works: app authenticates to vault/KMS -> policy checks role -> returns secret or decrypts data key -> audit log records access -> rotation job creates new version -> consumers reload safely.
- Tradeoffs: central vault improves control but becomes a dependency; dynamic secrets reduce blast radius but add integration complexity; frequent rotation improves safety but can cause outages if clients cannot reload.
- Real-world usage: HashiCorp Vault, AWS Secrets Manager/KMS, GCP Secret Manager/KMS, Kubernetes sealed/external secrets.
- Interview sentence: “I prefer workload identity plus short-lived dynamic credentials, audited access, and dual-version rotation with automatic rollback.”
- Recap: secrets need lifecycle, not hiding places.

## Anecdotes & war stories to use
- Public GitHub secret leaks led platforms to add secret scanning and push protection.
- HashiCorp Vault popularized dynamic database credentials that expire automatically.
- Cloud KMS envelope encryption is common because data keys can be rotated without re-encrypting every object immediately.
- Kubernetes Secrets are only base64 by default; production clusters rely on encryption at rest and external secret controllers.

## Things to mention / interview tips
- Never store secrets in source code, container images, or long-lived CI logs.
- Use identity-based access instead of distributing master credentials.
- Rotate with overlap: publish new, reload clients, verify, revoke old.
- Include break-glass access with audit and expiration.

## Common mistakes to call out
- Treating environment variables as a complete secrets system.
- Rotating only the stored value but not restarting/reloading clients.
- Giving every service access to the same database password.
- Logging decrypted secrets during debug.

## Diagrams / visuals to draw on screen
- App -> vault/KMS access flow with audit log.
- Envelope encryption: master key, data key, ciphertext.
- Rotation timeline old/new credential overlap.
- Secret leak path from repo/image/log to attacker.

## Series glue
- Connect back to PII token vaults and auth keys. Next: STRIDE threat modeling finds where secrets and trust boundaries fail. CTA: subscribe and get the rotation runbook template in GitHub.
