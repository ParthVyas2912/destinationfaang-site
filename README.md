# Destination Engineer

**Become a great engineer and solve the world's problems together.**

The site displays **Destination Engineer (formerly Destination FAANG)** during
the transition. The public brand and target canonical domain are now
Destination Engineer and `https://destinationengineer.com`. The repository name,
YouTube channel ID, LinkedIn organization ID, and visitor-counter storage remain
unchanged. Original YouTube titles and description archives are retained;
`videos.json` is website presentation data and uses the current brand name.

A clean, fast, **static website** that organizes your YouTube channel's 400+ videos
into four browsable categories:

- **DSA** — Data Structures & Algorithms
- **System Design**
- **Behavioral** — interview questions
- **Miscellaneous** — everything else

Features: category tabs with live counts, **company filter** (Google / Amazon /
Microsoft / Meta / Apple), **difficulty filter** (Easy / Medium / Hard), instant
search, topic/company/difficulty badges on each card, responsive card grid, and
a dark theme. No frontend framework or bundler — just HTML/CSS/JS plus small
Python scripts that fetch the catalog and generate the website metadata.

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
python build_seo.py
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
python build_seo.py
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

## Publishing the rebrand

The site uses the existing GitHub Pages deployment in
`.github/workflows/deploy.yml`. Cloudflare manages the domain/DNS; moving to
Cloudflare Pages or renaming this repository is not required.

Deployment regenerates the branded catalog and pages, then publishes only the
five root HTML pages, `videos.json`, `robots.txt`, `sitemap.xml`, `assets/`, and
`v/`. Source scripts, README/SEO notes, CSVs, original-description archives, and
course-production material remain in GitHub, not in the public website artifact.

**The source changes do not perform the live domain or social-account cutover.**
Do not publish new-domain links until DNS, certificates, and redirects are ready.
The publishing jobs can overwrite manually edited YouTube descriptions, so
coordinate their pause/resume with the launch.

1. Verify ownership of `destinationengineer.com` in GitHub Pages and retain
   ownership of `destinationfaang.com`. Verify both in Google Search Console.
2. Prepare the new DNS records and old-domain redirects in Cloudflare before a
   coordinated cutover. The apex uses GitHub Pages A records
   `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`;
   `www` uses a CNAME to `parthvyas2912.github.io`. Follow GitHub's domain
   verification guidance before activating DNS pointing at Pages.
3. Deploy `worker/counter.js` to the **existing** Worker and KV namespace so both
   domains are accepted. See `worker/README.md`.
4. Pause the YouTube metadata/comment workflows for the cutover. Publish the
   prepared website and set **Settings > Pages > Custom domain** to
   `destinationengineer.com`, coordinating DNS activation and certificate
   provisioning. Enable **Enforce HTTPS** when available. With Actions-based
   publishing, changing the `CNAME` file alone is not sufficient.
5. Once the new site responds correctly, activate permanent redirects for both
   old hostnames, HTTP and HTTPS. The old domain needs active TLS and **proxied**
   Cloudflare DNS. Match only `destinationfaang.com` and
   `www.destinationfaang.com`, use status **301**, and enable
   **Preserve query string** with this dynamic target:

   ```text
   concat("https://destinationengineer.com", http.request.uri.path)
   ```

   Also canonicalize `www.destinationengineer.com` to the non-www HTTPS domain.
   Preserve `/v/<id>.html`, other paths, and query filters; never redirect every
   page to the homepage. Keep old-domain redirects for at least one year,
   preferably indefinitely, and keep renewing the old domain.
6. Verify the homepage, all main pages, a video deep link, filtered search URLs,
   old-domain redirects, social previews, and the counter. Submit Search
   Console's **Change of Address** and the new sitemap; monitor indexing/404s.
7. Rename the **existing** YouTube channel and LinkedIn Page in their respective
   admin interfaces. Set an available handle/public URL, update descriptions and
   website links, and upload the artwork below. The stable IDs in this repo do
   not change. Update Stripe's public branding and linked Google practice sheets
   through their owner accounts without replacing payment or document URLs.
8. Announce the change, review the prepared `seo-suggestions.csv` descriptions,
   and resume YouTube publishing only when ready. Preserve timestamps, metadata
   history, and historical video titles. The LinkedIn publishing schedule remains
   paused; a rebrand does not resolve its existing API-access restriction.

References: [GitHub custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site),
[Cloudflare domain redirects](https://developers.cloudflare.com/fundamentals/manage-domains/redirect-domain/),
[Google site moves](https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes).

## Brand artwork and copy

The **DE Forward** mark keeps the original angular D and a single forward arrow
on the E's **top bar**. The middle and bottom bars are plain; do not substitute
the rounded-D concept or the former middle-arrow variant.
Colors: near-black `#0b0d13`, electric lime `#e5ff46`, off-white `#f4f6ed`.
No third-party company logos are used.

| Use | File |
| --- | --- |
| Scalable website logo / favicon | `assets/logo.svg` |
| YouTube avatar (800 x 800) | `assets/logo.png` |
| Apple touch icon (180 x 180) | `assets/apple-touch-icon.png` |
| Transparent mark / monochrome vector | `assets/brand/mark-transparent.svg`, `mark-transparent.png`, `mark-monochrome.svg` |
| Transparent wordmark for dark backgrounds | `assets/brand/wordmark.png` |
| YouTube banner (2560 x 1440, centered safe-area content) | `assets/brand/youtube-banner.png` |
| YouTube watermark (150 x 150) | `assets/brand/youtube-watermark.png` |
| LinkedIn Page logo / cover | `assets/brand/linkedin-logo.png`, `linkedin-cover.png` |
| Website share image (1200 x 630) | `assets/og-image.png` |

Regenerate the artwork with Pillow installed:

```powershell
python scripts\make_og_image.py
python build_seo.py
python -m unittest discover -s tests
node --test tests\app.test.mjs tests\counter.test.mjs
```

Suggested channel/Page description:

> Destination Engineer helps you become a stronger software engineer with free
> DSA, system design, behavioral interview preparation, and career lessons.
> Formerly Destination FAANG. Same creator, same free learning mission.
> Explore the video library at https://destinationengineer.com.

Launch announcement (publish only after the domain works):

> Destination FAANG is now Destination Engineer. Same creator, same free learning
> mission, broader horizons. DSA and interview preparation remain, alongside the
> skills that help you become a stronger engineer. Our new home is
> https://destinationengineer.com.

Keep the parenthetical "(formerly Destination FAANG)" in the shared navigation
and footers during the transition. The homepage title also includes it, and
WebSite structured data retains `Destination FAANG` as `alternateName` so search
engines can associate the names. Remove the visible transition label from the
static pages and `build_seo.py` together when recognition has settled.
Spoken references and original titles on YouTube, and archived material, remain
unchanged. The website's own catalog replaces the old channel-brand wording
in displayed titles and descriptions, including milestone videos.
Refresh thumbnail/slide templates, course PDFs, other social profiles, email
signatures, support-page branding, and externally hosted practice sheets separately.

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
├── site_branding.py    # Shared normalization of website-facing catalog text
├── categorize.py       # Keyword categorization + company/difficulty/topic tagging
├── CNAME               # Target domain (also configure GitHub Pages settings)
├── netlify.toml        # Netlify deploy config
├── robots.txt          # SEO: crawl + sitemap reference (generated)
├── sitemap.xml         # SEO: sitemap (generated)
└── README.md
```

---

## Catalog refresh

`.github/workflows/refresh.yml` fetches videos daily at 06:17 UTC and on demand,
using the existing channel ID. A name/handle change does not require replacing
that ID. GitHub may delay scheduled runs.

Both catalog importers and `build_seo.py` use `site_branding.py` to replace
`Destination FAANG` with `Destination Engineer` in website titles, descriptions,
and optional channel titles. The transformation is idempotent and preserves
video IDs, watch/thumbnail URLs, dates, categories, and original archive files.
It does not change YouTube metadata or generic FAANG interview topic references.
Searching the website using either brand name returns the same matching videos.

The refresh commits `videos.json`, generated video pages, homepage structured
data, sitemap, and robots.txt. GitHub does **not** start push-triggered workflows
for commits made with `GITHUB_TOKEN`, so `deploy.yml` also listens for a successful
`Refresh videos.json` completion via `workflow_run`. That deployment checks out
the latest `main`, not the refresh's starting commit, to include the newly fetched
videos. Failed refreshes do not trigger a deployment.

To publish new uploads immediately, run **Actions > Refresh videos.json > Run
workflow** on `main`, then confirm the following **Deploy to GitHub Pages** run
succeeds. Fetching the catalog is read-only on YouTube; it does not run the
separate title/description or comment publishing tools.
