# Availability: SLA, SLO & SLI Explained (Nines)

| | |
|---|---|
| **Publish order** | 081 |
| **Course #** | 5 |
| **Module** | M01 — Scalability Foundations |
| **Type** | concept |
| **Target length** | ~14 min |
| **Primary search keyword** | `sla slo sli` |
| **Demand** | High |

**Thumbnail text idea:** COUNT THE NINES
**One-line hook (first 15s):** If you promise 99.9% availability, you just spent almost all of your outage budget before the quarter starts.

## Learning objectives
- Define SLI, SLO, SLA, error budget, and availability nines.
- Convert availability targets into downtime budgets.
- Pick user-centered SLIs for APIs, jobs, and streams.
- Use error budgets to balance shipping and reliability.

## Topics & items to cover
- Hook: "four nines" becomes real when translated into minutes.
- Definition: SLI is the measurement, SLO is the internal target, SLA is the external contract with consequences.
- Worked example: monthly 99.9% availability allows about 43 minutes of bad service; if checkout has 20 minutes of errors in week one, slow risky launches.
- How it works: request success ratio, latency threshold, freshness, correctness, burn-rate alerts, rolling windows, customer-impact weighting.
- Tradeoffs: stricter SLOs cost more; averages hide bad percentiles; SLAs should lag internal SLOs.
- Real-world usage: Google SRE error budgets, cloud SLAs, status pages, API dashboards.
- Interview sentence: "I’d define SLIs from the user journey, set an SLO tighter than the SLA, and use error-budget burn to govern releases."
- Recap: reliability is measured user happiness.

## Anecdotes & war stories to use
- Google’s SRE books made error budgets mainstream for balancing velocity and reliability.
- Cloud providers publish SLAs with service credits, showing legal promises differ from engineering goals.
- Teams learn uptime-only SLIs miss brownouts where the site is up but too slow.
- Status-page incidents often distinguish partial degradation from full outage.

## Things to mention / interview tips
- Use concrete SLIs: `successful checkout under 500ms`, not "CPU below 70%."
- Explain burn rate: consuming budget too fast triggers pages.
- Make SLAs less aggressive than internal SLOs.
- Include dependency SLOs in design risk.

## Common mistakes to call out
- Confusing SLA and SLO.
- Measuring server uptime instead of user-visible success.
- Promising 100% availability.
- Ignoring latency as availability degradation.

## Diagrams / visuals to draw on screen
- SLA/SLO/SLI pyramid.
- Error budget bar draining over a month.
- Burn-rate alert line for fast and slow windows.

## Series glue
- Ties incident response to measurable reliability; next synthesizes the major tradeoffs candidates must verbalize. CTA: subscribe and get the worksheet in GitHub.
