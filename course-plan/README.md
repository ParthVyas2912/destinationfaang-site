# System Design Mega Course — Production Plan

The build plan for the **System Design Interview** YouTube mega-course: 100+ videos that
eventually merge into a single 50–100 hour course. Videos **1–4 are already published**;
this folder plans the **129 remaining videos**.

## How this folder is organized

- **`SCHEDULE.md`** — the full publishing table (demand-led order, module, type, length, keyword, demand).
- **`manifest.json`** — machine-readable source of truth for the whole plan.
- **`NNN - <Video Title>/brief.md`** — one folder per video, in publish order. Each `brief.md` lists
  what to cover, real anecdotes/war-stories to use, interview tips, common mistakes, and diagrams to draw.
- **`generate.py`** — regenerates folders + `SCHEDULE.md` + `manifest.json` from the `PLAN` list.
- **`write_briefs.py`** — writes the baseline `brief.md` template into every folder.

## Publishing strategy (why the order looks like this)

YouTube discovery is **Search + Suggested**, which reward high-intent keywords. So the publish
order is **not** the final course order — it is demand-led:

1. **Front-load high-search case studies** (`Design TinyURL/Twitter/Instagram/WhatsApp…`). These are
   the traffic engines that people actually search for.
2. **Interleave ~2 case studies : 1 concept.** The concept videos (CAP, consistent hashing, Kafka…)
   are taught *inside* the case studies first, then reinforced as standalone explainers that get
   pulled in via Suggested.
3. **The AI-systems module (RAG, vector search, LLM serving) is the growth wedge** — trending and
   far less saturated than "Design Instagram."
4. **Mock interviews + capstone close the series.**

Every video has **3 jobs**: rank in search for its primary keyword, teach one reusable concept
(course glue), and pull viewers deeper into the playlist.

## Regenerating

```bash
python course-plan/generate.py     # rebuild folders + SCHEDULE.md + manifest.json
python course-plan/write_briefs.py # (re)write baseline briefs (overwrites brief.md)
```

> To reorder or add videos, edit the `PLAN` list in `generate.py` and re-run. `brief.md` files that
> were hand-enriched will be overwritten by `write_briefs.py`, so enrich after generating.
