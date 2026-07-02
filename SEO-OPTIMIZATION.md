# YouTube SEO Optimization — Titles & Descriptions

This document accompanies **[`seo-suggestions.csv`](./seo-suggestions.csv)**, which contains
SEO-optimized title and description suggestions for **all 413 videos** on the
[Destination FAANG](https://www.youtube.com/channel/UC49H999tjewVmrdLoCWCs4g) channel.

The goal is to increase **click-through rate (CTR)** and **search discoverability** so more
of the right viewers click and watch.

## The CSV

`seo-suggestions.csv` has one row per video with these columns:

| Column | Meaning |
| --- | --- |
| `video_id` | YouTube video ID |
| `url` | Direct link to the video |
| `category` | Site category (`dsa`, `system-design`, `behavioral`, `misc`) |
| `published_at` | Publish date |
| `current_title` | Existing title |
| `current_title_len` | Length of the existing title |
| `suggested_title` | New SEO-optimized title (≤ 70 chars) |
| `suggested_title_len` | Length of the suggested title |
| `suggested_description` | New optimized description (hook-first, keyword-rich, with hashtags) |
| `rationale` | One-line explanation of the key change |

Open it in Excel / Google Sheets and work top-to-bottom, pasting the suggested title and
description into YouTube Studio.

## Problems found in the current titles

1. **Too long — 181 of 413 titles (44%) exceeded 70 characters.** YouTube truncates long
   titles in search results, the Suggested sidebar, and mobile — so the payoff/keyword at the
   end gets cut off. Average title length was **68.5 chars**.
2. **Keyword buried at the end.** Many titles led with the problem, then trailed a long list
   like `- technical interview question @ google, apple, amazon, meta, microsoft`. That tail
   eats the visible space without adding search value (you can't realistically rank for every
   company on every problem), and pushes the real keyword out of view.
3. **Missing the terms people actually search.** Viewers search `"LeetCode 200"`,
   `"Number of Islands"`, `"sliding window"`, `"DP"`. Titles didn't consistently include the
   LeetCode number, the problem name, and the core technique together.
4. **Descriptions started with boilerplate.** The first line (the part shown before "…more",
   and heavily weighted by search) was often the "Join this channel…" perks line instead of a
   keyword-rich hook.

## What the suggestions do

**Titles** (now averaging **45.7 chars**, 0 over 70):
- Front-load the primary keyword (problem/topic) in the first ~40 chars.
- Use a clean, consistent DSA pattern: `Problem Name | LeetCode <num> (Difficulty)` or
  `Problem Name — <Technique> Explained`.
- Surface the core pattern/technique (Two Pointers, DFS, DP, Sliding Window, etc.) where clear.
- Drop the long company tag-lists from the title (they belong in the description/tags).

**Descriptions:**
- Open with a keyword-rich hook in the first 1–2 lines (the visible snippet).
- Explain what the viewer learns, the approach/pattern, and who it's for (FAANG/MAANG prep).
- End with a call-to-action and 3–6 relevant hashtags.
- Remove the leading "Join this channel…" boilerplate from the top (move it lower if desired).

## Before / after examples

```
CUR [78] Best Time to Buy and Sell Stock with Cooldown: 309 - google interview question
NEW [47] Stock With Cooldown | LeetCode 309 DP Explained

CUR [95] Daily Temperatures: 739 - technical interview question @ google, apple, amazon, meta, microsoft
NEW [33] Daily Temperatures | LeetCode 739

CUR [92] Min Stack: 155 - stack technical interview question @ google, apple, amazon, meta, microsoft
NEW [33] Min Stack | LeetCode 155 (Medium)
```

## How to roll it out

1. **Prioritize by impact.** Start with your highest-impression videos (check YouTube Studio →
   Analytics → Content, sort by impressions). A better title on a video already getting
   impressions moves the needle fastest.
2. **Don't over-edit at once.** Update in batches; changing a title can briefly reset how the
   algorithm tests it, so give each batch a couple of weeks and watch CTR.
3. **Keep thumbnails in sync.** Title + thumbnail work together — make sure the thumbnail
   reinforces the keyword/hook in the new title.
4. **Add tags too.** The company names removed from titles (Google, Amazon, Meta, etc.) are
   great as YouTube tags and inside the description body.

---

*Generated as an internal SEO resource. Suggestions are based on each video's existing title
and description; no fabricated facts, timestamps, or results were added.*
