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

## Going live on destinationfaang.com

This repo is **private**. GitHub Pages does **not** serve private repos on the
free plan, so pick one of these:

### Option A — Cloudflare Pages (free, keeps the repo private) ✅ recommended
1. <https://dash.cloudflare.com> → **Workers & Pages → Create → Pages → Connect to Git**.
2. Authorize GitHub and pick `destinationfaang-site`.
3. Build settings: **Framework preset: None**, **Build command: (empty)**,
   **Output directory: `/`**. Deploy.
4. **Custom domains → Set up a domain → `destinationfaang.com`** and follow the
   DNS instructions. Done — live and private.

### Option B — Netlify (free, keeps the repo private)
1. <https://app.netlify.com> → **Add new site → Import from Git → GitHub** →
   pick `destinationfaang-site`. `netlify.toml` already configures it (no build).
2. **Domain settings → Add custom domain → `destinationfaang.com`**.

### Option C — GitHub Pages (free, **repo must be public**) — ✅ currently active
The site is **deployed and live** at
<https://parthvyas2912.github.io/destinationfaang-site/>.

To attach **destinationfaang.com**, configure DNS at your domain registrar, then
add the domain in GitHub:

1. **At your DNS provider**, for the apex domain `destinationfaang.com` add four
   `A` records pointing at GitHub Pages:
   ```
   185.199.108.153
   185.199.109.153
   185.199.110.153
   185.199.111.153
   ```
   (optional IPv6 `AAAA`: `2606:50c0:8000::153`, `...8001::153`, `...8002::153`, `...8003::153`)
   and a `CNAME` record for `www` → `parthvyas2912.github.io`.
2. **GitHub → repo Settings → Pages → Custom domain** → enter
   `destinationfaang.com` → Save (this recreates the `CNAME` file). Wait for the
   DNS check to pass, then tick **Enforce HTTPS**.

> ⚠️ Do step 1 **before** step 2. Setting the custom domain before DNS resolves
> makes the github.io URL redirect to a dead domain.

---

## Project structure

```
destinationfaang-site/
├── index.html          # Page markup + SEO meta + JSON-LD
├── assets/
│   ├── styles.css      # Theme & layout
│   ├── app.js          # Loads videos.json, tabs/filters, search, rendering
│   └── og-image.svg    # Social share image
├── videos.json         # Generated data (your real channel data)
├── videos.sample.json  # Categorized demo data (DSA/SysDesign/Behavioral/Misc)
├── fetch_videos.py     # Pulls videos via YouTube Data API + categorizes + enriches
├── build_from_ytdlp.py # Alternative: build videos.json from a yt-dlp dump (no key)
├── build_seo.py        # Generates sitemap.xml, robots.txt + injects JSON-LD
├── categorize.py       # Keyword categorization + company/difficulty/topic tagging
├── CNAME               # Custom domain for GitHub Pages (destinationfaang.com)
├── netlify.toml        # Netlify deploy config
├── robots.txt          # SEO: crawl + sitemap reference (generated)
├── sitemap.xml         # SEO: sitemap (generated)
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
