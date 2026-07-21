"""Write a structured baseline brief.md into every course-plan video folder.

Reads manifest.json (produced by generate.py) and creates a type-aware brief
(case study / concept / mock) for each video. Content is intentionally structured
so it is useful as-is and easy to enrich later.

Run:  python course-plan/write_briefs.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "manifest.json"), encoding="utf-8") as f:
    MANIFEST = json.load(f)


def system_name(youtube_title):
    """Extract the target system/topic from a title."""
    return youtube_title.split(" — ")[0].split(" (")[0].strip()


def case_body(m):
    name = system_name(m["youtube_title"])
    return f"""## Topics & items to cover  (follow the 6-step template)

**Step 1 — Requirements (≈4 min)**
- Functional requirements: list the 3-5 core features of {name}. Explicitly say what you are *not* building.
- Non-functional requirements: availability target, latency budget, consistency needs, durability, scale.
- Ask/state clarifying questions out loud — model the interview behavior.

**Step 2 — Back-of-the-envelope estimation (≈4 min)**
- DAU / MAU assumption and read:write ratio.
- QPS (average and peak = 2-3x average), storage/year, bandwidth.
- Call back to video #4 (Capacity Planning) — link it as a card.

**Step 3 — API / data model (≈4 min)**
- Define the key endpoints (REST/gRPC) with request/response shapes.
- Core entities + which store each lives in (SQL vs NoSQL vs blob vs cache).

**Step 4 — High-level design (≈6 min)**
- Draw the boxes: clients → LB/gateway → services → datastores → async workers.
- Walk one write path and one read path end-to-end.

**Step 5 — Deep dives / bottlenecks (≈8-10 min)** — this is where interviews are won
- Identify the 2-3 hardest sub-problems specific to {name} and solve each.
- Discuss sharding/partitioning key, caching strategy, and the main scaling wall.
- Talk through a failure scenario and how the system degrades gracefully.

**Step 6 — Wrap-up (≈2 min)**
- Recap tradeoffs, name what you'd improve with more time, connect to real companies.

## Anecdotes & war stories to use
- Open with a real interview framing ("this exact question was asked at ___").
- Reference how a real company solved this at scale (papers, eng blogs) — one concrete story.
- Share a "candidate mistake I've seen" moment to make it memorable.
- (Enrich: add 2-3 specific, verifiable stories — company names, numbers, outages.)

## Things to mention / interview tips
- Say the tradeoff *out loud* every time you make a choice — interviewers score reasoning, not the diagram.
- Start simple, then scale. Don't jump to the final architecture.
- Tie every component back to a requirement from Step 1.

## Common mistakes to call out
- Skipping requirements/estimation and jumping to boxes.
- Over-engineering before establishing scale.
- Ignoring the read:write ratio when choosing storage + caching.

## Diagrams / visuals to draw on screen
- The 6-step template as a persistent sidebar.
- HLD box diagram; one animated request path.
- A "deep dive" zoom-in for the hardest sub-problem.

## GitHub resource idea
- A repo with the diagram (excalidraw/mermaid), the estimation spreadsheet, and a 1-page cheat sheet for `{m['primary_keyword']}`.
"""


def concept_body(m):
    name = system_name(m["youtube_title"])
    return f"""## Topics & items to cover
- **Hook / why it matters (≈1 min):** where {name} shows up in real interviews and systems.
- **The core idea in one sentence** — define it plainly before any jargon.
- **How it works:** build it up from first principles with a worked example.
- **Tradeoffs:** what you gain, what you pay, and when NOT to use it.
- **Real-world usage:** 2-3 systems/companies that rely on this.
- **Interview angle:** the exact sentence to say when this comes up in a design.
- **Recap + one-line takeaway.**

## Anecdotes & war stories to use
- A concrete real-world example where this concept was the deciding factor.
- A famous outage or scaling story tied to getting this right/wrong.
- (Enrich: add 2-3 specific, verifiable stories — company names, numbers, dates.)

## Things to mention / interview tips
- The exact phrasing to drop in an interview to show mastery of `{m['primary_keyword']}`.
- The one number or rule-of-thumb worth memorizing.
- How this connects to the case-study videos that use it.

## Common mistakes / misconceptions to correct
- The most common wrong mental model people have about {name}.
- The edge case interviewers probe to test depth.

## Diagrams / visuals to draw on screen
- One clear animated diagram that makes the mechanism obvious.
- A before/after or with/without comparison.

## GitHub resource idea
- A minimal runnable demo or diagram illustrating `{m['primary_keyword']}`.
"""


def mock_body(m):
    return f"""## Format
- Two-person mock ({m['length_min']} min): one interviewer, one candidate. If solo, narrate both roles.
- Use a real whiteboard/excalidraw and a running clock on screen.

## Topics & items to cover
- Show the *full* interview arc: requirements → estimation → API → HLD → deep dive → wrap-up.
- Pause at decision points and explain the scoring rubric ("here's what a strong answer looks like").
- Show at least one recovery from a stumble — how to handle being stuck live.

## Anecdotes & war stories to use
- Real interviewer signals: what makes them lean in vs check out.
- A "this candidate failed because…" story and a "this candidate aced it because…" story.
- (Enrich: add specific hiring-bar observations and phrasing.)

## Things to mention / interview tips
- Time management: how many minutes to spend per phase.
- How to drive the conversation instead of waiting to be asked.
- Communication and storytelling tactics (ties to the Storytelling video).

## Common mistakes to call out
- Going silent while thinking.
- Diving into deep dives before agreeing on scope.
- Not stating tradeoffs.

## Deliverable
- End with a filled-out scorecard so viewers can self-assess.
"""


BODY = {"case": case_body, "concept": concept_body, "mock": mock_body, "intro": concept_body}


def build(m):
    demand_stars = "🔥" * m["demand"]
    header = f"""# {m['youtube_title']}

> Baseline content brief — enrich with specific anecdotes, numbers, and diagrams before filming.

| | |
|---|---|
| **Publish order** | {m['publish_order']:03d} |
| **Course #** | {m['course_num']} |
| **Module** | {m['module']} — {m['module_name']} |
| **Type** | {m['type']} |
| **Target length** | ~{m['length_min']} min |
| **Primary search keyword** | `{m['primary_keyword']}` |
| **Demand** | {m['demand_label']} {demand_stars} |

**Thumbnail text idea:** _{system_name(m['youtube_title']).upper()}_
**One-line hook (first 15s):** State the problem + payoff, then promise the outcome.

"""
    body = BODY[m["type"]](m)
    footer = f"""
## Series glue
- **Reference back to:** earlier prerequisite videos (link as cards + in description).
- **Point forward to:** the next video in the series and the full playlist.
- **CTA:** subscribe for the full System Design Interview course; link the GitHub repo.

---
_Every video has 3 jobs: rank in search (`{m['primary_keyword']}`), teach a reusable concept, and pull viewers into the playlist._
"""
    return header + body + footer


def main():
    for m in MANIFEST:
        path = os.path.join(HERE, m["folder"], "brief.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(build(m))
    print(f"Wrote {len(MANIFEST)} brief.md files.")


if __name__ == "__main__":
    main()
