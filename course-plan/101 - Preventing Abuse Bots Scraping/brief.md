# Preventing Abuse, Bots & Scraping

| | |
|---|---|
| **Publish order** | 101 |
| **Course #** | 64 |
| **Module** | M06 — Security, Observability & FinOps |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `bot prevention system design` |
| **Demand** | Moderate |

**Thumbnail text idea:** STOP BAD TRAFFIC
**One-line hook (first 15s):** Abuse prevention is not one CAPTCHA; it is a risk engine that chooses friction based on identity, behavior, and impact.

## Learning objectives
- Design layered defenses for stuffing, scraping, fake signups, and inventory hoarding.
- Combine rate limits, device signals, reputation, challenges, and behavior models.
- Explain false-positive tradeoffs and progressive friction.
- Build feedback loops from reports, chargebacks, and takedowns.

## Topics & items to cover
- Hook: blocking every suspicious request breaks users; challenging none gives attackers the cheapest path.
- Definition: abuse prevention scores requests/accounts, then allows, throttles, challenges, shadow-bans, or blocks.
- Worked example: login sees 50 attempts/minute from one ASN across many accounts; limit by IP, account, device, and credential pair; require WebAuthn/OTP when risk >80; send confirmed stuffing patterns to reputation lists.
- How it works: edge collector -> features -> rules/ML risk score -> decision service -> CDN/API/app enforcement -> analyst feedback.
- Tradeoffs: friction reduces fraud but hurts conversion/accessibility; fingerprinting helps but raises privacy issues; scraper blocking is adversarial.
- Real-world usage: ticketing queues, sneaker drops, login protection, marketplace spam, API scraping, free-trial abuse.
- Interview sentence: “Use layered risk-based controls and measure both attack reduction and false-positive harm to legitimate users.”
- Recap: make abuse expensive while real users keep moving.

## Anecdotes & war stories to use
- Ticketmaster-style high-demand sales show queues, bot detection, and purchase limits must work together.
- Cloudflare/Akamai bot management uses network, browser, and behavioral signals, not one rule.
- PayPal/Stripe-like fraud systems need feedback from disputes and chargebacks.
- robots.txt is voluntary; malicious scrapers ignore it, so enforcement needs technical controls.

## Things to mention / interview tips
- Rate limit by IP, account, device, payment instrument, route, and ASN.
- Use progressive friction: throttle, challenge, step-up, block.
- Include analyst tools and appeals for false positives.
- Log decisions with reason codes.

## Common mistakes to call out
- Relying only on IP limits behind proxies/mobile carriers.
- CAPTCHA everywhere, hurting conversion/accessibility.
- Blocking without false-positive monitoring.
- Expecting ML labels that arrive weeks later to be instantly accurate.

## Diagrams / visuals to draw on screen
- Risk scoring pipeline to enforcement.
- Multi-key rate limiter table.
- Progressive action ladder.
- Feedback loop from fraud reports to rules/models.

## Series glue
- Connect to auth: strong identity reduces cheap abuse. Next: PII/PCI handling protects sensitive signals collected here. CTA: subscribe and use the GitHub abuse checklist.
