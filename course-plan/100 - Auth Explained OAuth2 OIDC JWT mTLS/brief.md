# Auth Explained: OAuth2, OIDC, JWT & mTLS

| | |
|---|---|
| **Publish order** | 100 |
| **Course #** | 59 |
| **Module** | M06 — Security, Observability & FinOps |
| **Type** | concept |
| **Target length** | ~20 min |
| **Primary search keyword** | `oauth2 oidc jwt` |
| **Demand** | Very High |

**Thumbnail text idea:** TOKENS NOT PASSWORDS
**One-line hook (first 15s):** Most auth answers fail because candidates mix up who the user is, what the app can do, and how services prove identity.

## Learning objectives
- Separate authentication, authorization, OAuth2, OIDC, JWT, sessions, and mTLS.
- Walk through authorization-code flow with PKCE.
- Design token validation, refresh, revocation, scopes, and service identity.
- Avoid unsafe long-lived tokens in public clients.

## Topics & items to cover
- Hook: JWT is not an auth system; it is one token format inside a trust model.
- Definition: OAuth2 delegates authorization, OIDC adds user identity, JWT encodes signed claims, and mTLS authenticates machines via certificates.
- Worked example: mobile app redirects to IdP, gets auth code, exchanges with PKCE verifier for access token `aud=api`; API validates issuer, audience, expiry, signature `kid`, and `orders:read` scope; refresh token lives in OS keystore.
- How it works: app/browser -> IdP -> code -> token endpoint -> API gateway/resource server; service A to B uses mTLS/SPIFFE identity plus short-lived service token.
- Tradeoffs: JWT validation scales but revocation is harder; opaque tokens centralize control but require introspection; mTLS is strong but adds cert lifecycle.
- Real-world usage: SSO, partner APIs, microservice identity, admin consoles, audit trails.
- Interview sentence: “Use OIDC for login, OAuth scopes for delegated access, short-lived access tokens, refresh-token rotation, and mTLS/workload identity for service calls.”
- Recap: identity, permission, and transport trust are distinct.

## Anecdotes & war stories to use
- OAuth security guidance pushed PKCE widely because intercepted codes are a real public-client risk.
- Major IdPs rotate signing keys; production APIs must use JWKS and `kid`, not hard-coded keys.
- SPIFFE/SPIRE and service meshes grew because IP allowlists fail in dynamic clusters.
- Many API incidents involve over-scoped or long-lived tokens; least privilege and rotation matter.

## Things to mention / interview tips
- Validate `iss`, `aud`, `exp`, signature, and scopes.
- Do not put secrets in SPAs; use PKCE or backend-for-frontend.
- Explain refresh-token rotation and reuse detection.
- Mention step-up auth for payout or admin changes.

## Common mistakes to call out
- Saying OAuth2 is authentication; OIDC is the identity layer.
- Trusting decoded JWTs without verifying signature/audience.
- Putting roles in long-lived tokens without revocation.
- Treating mTLS identity as authorization without policy mapping.

## Diagrams / visuals to draw on screen
- Authorization-code-with-PKCE sequence.
- JWT header/payload/signature validation checklist.
- User-to-service token flow versus service-to-service mTLS.
- Token lifecycle: issue, refresh, rotate, revoke.

## Series glue
- Reference API gateway/rate-limiting videos. Next: abuse prevention and PII handling depend on strong identity boundaries. CTA: subscribe and grab the auth checklist from GitHub.
