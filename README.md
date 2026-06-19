# 🎬 Video Hub

A clean, fast, **static website** that organizes your YouTube channel's 400+ videos
into four browsable categories:

- **DSA** — Data Structures & Algorithms
- **System Design**
- **Behavioral** — interview questions
- **Miscellaneous** — everything else

Features: category tabs with live counts, **company filter** (Google / Amazon /
Microsoft / Meta / Apple), **difficulty filter** (Easy / Medium / Hard), instant
search, topic/company/difficulty badges on each card, responsive card grid, and
a dark theme. No framework, no build step — just HTML/CSS/JS plus a small Python
script that pulls and enriches your videos.

Each video in `videos.json` carries: `category`, `companies[]`, `difficulty`
(from `#easy/#medium/#hard` tags), and DSA `topics[]` (array, tree, graph, DP …).

---

## Quick start (view the sample site)

The repo ships with sample data so you can see it immediately. From this folder:

```powershell
python -m http.server 8000
```

Then open <http://localhost:8000>.

> Open it through the local server (not by double-clicking `index.html`) —
> browsers block `fetch()` of `videos.json` from `file://` URLs.

---

## Use your real videos

### 1. Get a YouTube Data API key (free, read-only)
- Go to <https://console.cloud.google.com/apis/credentials>
- Create a project, **enable "YouTube Data API v3"**, then create an API key.

### 2. Find your channel ID (starts with `UC...`)
- <https://www.youtube.com/account_advanced>

### 3. Fetch + categorize all your videos

```powershell
$env:YT_API_KEY="YOUR_API_KEY_HERE"
python fetch_videos.py --channel-id UCxxxxxxxxxxxxxxxxxxxxxx
```

This overwrites `videos.json` with every public upload, each tagged with a
category. The script prints a per-category count when it finishes. Re-run it any
time you upload new videos.

> Quota cost is tiny (~1 unit per 50 videos), well within the free daily quota.
> No YouTube Studio login / OAuth needed — only the public uploads playlist is read.

### 4. Refresh the page
That's it. The site reads the new `videos.json` automatically.

### Alternative: no API key (uses yt-dlp)

If you'd rather not create an API key, `yt-dlp` can list a whole channel:

```powershell
python -m pip install --upgrade yt-dlp
python -m yt_dlp --flat-playlist -J "https://www.youtube.com/channel/UC_YOUR_CHANNEL_ID/videos" > channel_raw.json
python build_from_ytdlp.py channel_raw.json videos.json
```

This categorizes by **title only** (flat dumps have no descriptions), so the
API-key path above produces slightly better results.

---

## How categorization works

`categorize.py` scores each video's **title (2×)** and **description** against
weighted keyword lists, and assigns the highest-scoring category (falling back to
*Miscellaneous* when nothing matches).

**Want to tune it?** Edit the `KEYWORDS` dictionary in `categorize.py` — add words
specific to your channel or bump weights. You can also hand-fix any individual
video by editing its `"category"` field directly in `videos.json` (values:
`dsa`, `system-design`, `behavioral`, `misc`).

---

## Deploy for free (GitHub Pages)

1. Create a GitHub repo and push these files.
2. Repo **Settings → Pages → Build and deployment → Source: "Deploy from a branch"**,
   pick `main` / root.
3. Your site goes live at `https://<username>.github.io/<repo>/`.

Since it's fully static, it also works on Netlify, Vercel, Cloudflare Pages, or
any static host.

---

## Project structure

```
youtube-video-hub/
├── index.html          # Page markup
├── assets/
│   ├── styles.css      # Theme & layout
│   └── app.js          # Loads videos.json, tabs, search, rendering
├── videos.json         # Generated data (your real channel data)
├── videos.sample.json  # Categorized demo data (DSA/SysDesign/Behavioral/Misc)
├── fetch_videos.py     # Pulls videos via YouTube Data API + categorizes
├── build_from_ytdlp.py # Alternative: build videos.json from a yt-dlp dump (no key)
├── categorize.py       # Keyword categorization logic (editable)
└── README.md
```

---

## Roadmap to destinationfaang.com

This static site is the MVP. To grow it into destinationfaang.com:

1. **Domain + hosting** — point destinationfaang.com at GitHub Pages, Netlify,
   Cloudflare Pages, or Vercel (all free, all work with these static files).
2. **Rebrand** — swap the header title to "Destination FAANG", add a logo, and
   lean into the FAANG angle (company filters are already wired in).
3. **Per-problem pages** (SEO) — generate a page per video/problem so Google can
   index "Two Sum Google interview" etc. A static-site generator (Astro, Next.js,
   or 11ty) reading videos.json is the natural next step.
4. **Roadmaps / playlists** — group the multi-part "Complete DSA Course" and
   "System Design Mega Course" videos into ordered learning tracks.
5. **Progress tracking** — let visitors mark problems solved (localStorage first,
   accounts later).
6. **Auto-refresh** — run fetch_videos.py on a schedule (GitHub Action) so new
   uploads appear automatically.
