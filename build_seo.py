"""Generate SEO assets from videos.json.

Produces:
  - sitemap.xml          (homepage, key pages + one entry per video page)
  - robots.txt           (allow all + sitemap reference)
  - v/<id>.html          (one indexable page per video with VideoObject +
                          BreadcrumbList JSON-LD, OpenGraph and a YouTube embed)
  - injects JSON-LD structured data into index.html between the
    <!-- SEO:JSONLD:START --> / <!-- SEO:JSONLD:END --> markers:
      * WebSite (with a SearchAction sitelinks search box)
      * ItemList of VideoObject entries (rich-result eligible)

Run this whenever videos.json changes:
    python build_seo.py
"""

import html
import json
import os
import re
from datetime import date

SITE = "https://destinationfaang.com"
INDEX = "index.html"
VIDEOS = "videos.json"
VIDEO_DIR = "v"  # per-video pages live under /v/<id>.html
CSS_VERSION = "20260701"
CHANNEL = "https://www.youtube.com/channel/UC49H999tjewVmrdLoCWCs4g"
MAX_VIDEO_OBJECTS = 413  # cap structured-data size if the catalog grows huge

CATEGORY_LABELS = {
    "dsa": "DSA",
    "system-design": "System Design",
    "behavioral": "Behavioral",
    "misc": "Miscellaneous",
}

# Static pages (besides the homepage) that should appear in the sitemap.
STATIC_PAGES = [
    ("about.html", "monthly", "0.6"),
    ("start-here.html", "monthly", "0.9"),
    ("resources.html", "monthly", "0.8"),
]


def clean_description(v):
    """Build a clean, human-readable meta description from a video entry."""
    desc = (v.get("description") or "").strip()
    # Drop the boilerplate "Join this channel..." intro if a real
    # "Description:" section follows.
    m = re.search(r"Description:\s*(.+)", desc, flags=re.DOTALL)
    if m:
        desc = m.group(1).strip()
    desc = re.sub(r"https?://\S+", "", desc)          # strip raw URLs
    desc = re.sub(r"\s+", " ", desc).strip()           # collapse whitespace
    if not desc:
        desc = v.get("title", "")
    if len(desc) > 160:
        desc = desc[:157].rstrip() + "…"
    return desc


def load_videos():
    with open(VIDEOS, encoding="utf-8") as f:
        return json.load(f).get("videos", [])


def build_jsonld(videos):
    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Destination FAANG",
        "url": SITE + "/",
        "description": "Filterable library of FAANG DSA, System Design and "
                       "Behavioral interview-prep videos.",
        "potentialAction": {
            "@type": "SearchAction",
            "target": SITE + "/?q={search_term_string}",
            "query-input": "required name=search_term_string",
        },
    }

    elements = []
    for i, v in enumerate(videos[:MAX_VIDEO_OBJECTS], start=1):
        vid = {
            "@type": "VideoObject",
            "name": v.get("title", ""),
            "description": (v.get("description") or v.get("title", ""))[:200],
            "thumbnailUrl": v.get("thumbnail", ""),
            "contentUrl": v.get("url", ""),
            "embedUrl": f"https://www.youtube.com/embed/{v.get('id','')}",
        }
        if v.get("publishedAt"):
            vid["uploadDate"] = v["publishedAt"]
        elements.append({"@type": "ListItem", "position": i, "item": vid})

    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "FAANG Interview Prep Videos",
        "numberOfItems": len(elements),
        "itemListElement": elements,
    }

    return (
        '<script type="application/ld+json">'
        + json.dumps(website, ensure_ascii=False, separators=(",", ":"))
        + "</script>\n  "
        + '<script type="application/ld+json">'
        + json.dumps(item_list, ensure_ascii=False, separators=(",", ":"))
        + "</script>"
    )


def inject_jsonld(block):
    with open(INDEX, encoding="utf-8") as f:
        html = f.read()
    replacement = "<!-- SEO:JSONLD:START -->\n  " + block + "\n  <!-- SEO:JSONLD:END -->"
    new = re.sub(
        r"<!-- SEO:JSONLD:START -->.*?<!-- SEO:JSONLD:END -->",
        lambda _m: replacement,  # function form avoids backslash-escape processing
        html,
        flags=re.DOTALL,
    )
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(new)


def write_sitemap(videos):
    dates = sorted(v.get("publishedAt", "")[:10] for v in videos if v.get("publishedAt"))
    lastmod = dates[-1] if dates else date.today().isoformat()
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        f"  <url>\n    <loc>{SITE}/</loc>\n    <lastmod>{lastmod}</lastmod>\n"
        "    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n  </url>",
    ]
    for page, changefreq, priority in STATIC_PAGES:
        parts.append(
            f"  <url>\n    <loc>{SITE}/{page}</loc>\n    <lastmod>{lastmod}</lastmod>\n"
            f"    <changefreq>{changefreq}</changefreq>\n    <priority>{priority}</priority>\n  </url>"
        )
    for v in videos:
        vid = v.get("id")
        if not vid or not re.fullmatch(r"[A-Za-z0-9_-]+", vid):
            continue
        vmod = (v.get("publishedAt") or "")[:10] or lastmod
        parts.append(
            f"  <url>\n    <loc>{SITE}/{VIDEO_DIR}/{vid}.html</loc>\n    <lastmod>{vmod}</lastmod>\n"
            "    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>"
        )
    parts.append("</urlset>\n")
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(parts))


def write_robots():
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")


def nav_html(prefix=""):
    """Shared top-nav markup. `prefix` is '../' for pages in subdirectories."""
    return f"""  <header class="site-header">
    <div class="wrap">
      <nav class="top-nav" aria-label="Primary">
        <a class="top-nav-brand" href="{prefix}index.html">
          <img class="brand-logo" src="{prefix}assets/logo.png" alt="Destination FAANG logo" width="40" height="40" />
          <span>Destination FAANG</span>
        </a>
        <div class="top-nav-links">
          <a class="nav-btn nav-btn--ghost" href="{prefix}index.html">Videos</a>
          <a class="nav-btn nav-btn--ghost" href="{prefix}start-here.html">Start Here</a>
          <a class="nav-btn nav-btn--ghost" href="{prefix}resources.html">Resources</a>
          <a class="nav-btn nav-btn--ghost" href="{prefix}about.html">About</a>
          <a class="nav-btn nav-btn--linkedin" href="https://www.linkedin.com/company/107371838/" target="_blank" rel="noopener noreferrer">
            <span class="nav-btn-ic" aria-hidden="true">in</span> LinkedIn
          </a>
          <a class="nav-btn nav-btn--support" href="{prefix}about.html#support" rel="noopener">
            <span aria-hidden="true">❤</span> Support
          </a>
        </div>
      </nav>
    </div>
  </header>"""


def footer_html(prefix=""):
    return f"""  <footer class="site-footer">
    <div class="wrap">
      <p><strong>Destination FAANG</strong> · Free FAANG interview prep · made with ❤ by Parth Vyas</p>
      <p class="footer-links">
        <a href="{prefix}index.html">Videos</a>
        <a href="{prefix}start-here.html">Start Here</a>
        <a href="{prefix}resources.html">Resources</a>
        <a href="{prefix}about.html">About</a>
        <a href="{CHANNEL}?sub_confirmation=1" target="_blank" rel="noopener noreferrer">Subscribe</a>
        <a href="https://www.linkedin.com/company/107371838/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
      </p>
      <p class="footer-count" id="visitor-counter" hidden>👀 <strong><span id="visitor-count">—</span></strong> visitors and counting</p>
    </div>
  </footer>

  <a class="donate-btn donate-btn--floating" href="{prefix}about.html#support" rel="noopener" aria-label="Support Destination FAANG">
    <span class="donate-icon" aria-hidden="true">❤</span> Support
  </a>

  <script src="{prefix}assets/visitor-counter.js?v={CSS_VERSION}" defer></script>"""


def video_page_html(v):
    """Full HTML document for a single video page."""
    vid = v.get("id", "")
    title = v.get("title", "Video")
    label = CATEGORY_LABELS.get(v.get("category"), "Miscellaneous")
    desc = clean_description(v)
    thumb = v.get("thumbnail") or f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
    watch_url = v.get("url") or f"https://www.youtube.com/watch?v={vid}"
    page_url = f"{SITE}/{VIDEO_DIR}/{vid}.html"
    published = v.get("publishedAt", "")

    e = html.escape
    companies = v.get("companies") or []
    topics = v.get("topics") or []
    pills = "".join(
        f'<span class="pill company">{e(c)}</span>' for c in companies
    ) + "".join(
        f'<span class="pill topic">{e(t)}</span>' for t in topics
    )
    diff = v.get("difficulty")
    diff_pill = (
        f'<span class="pill diff-{e(diff.lower())}">{e(diff)}</span>' if diff else ""
    )

    video_object = {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": title,
        "description": desc,
        "thumbnailUrl": thumb,
        "contentUrl": watch_url,
        "embedUrl": f"https://www.youtube.com/embed/{vid}",
    }
    if published:
        video_object["uploadDate"] = published

    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": label,
             "item": f"{SITE}/?cat={v.get('category', 'all')}"},
            {"@type": "ListItem", "position": 3, "name": title, "item": page_url},
        ],
    }
    jsonld = (
        '<script type="application/ld+json">'
        + json.dumps(video_object, ensure_ascii=False, separators=(",", ":"))
        + "</script>\n  "
        + '<script type="application/ld+json">'
        + json.dumps(breadcrumb, ensure_ascii=False, separators=(",", ":"))
        + "</script>"
    )

    pub_human = published[:10] if published else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{e(title)} | Destination FAANG</title>
  <meta name="description" content="{e(desc)}" />
  <link rel="canonical" href="{page_url}" />
  <meta name="theme-color" content="#0b0d13" />
  <link rel="icon" type="image/png" href="../assets/logo.png" />
  <link rel="apple-touch-icon" href="../assets/logo.png" />
  <link rel="preconnect" href="https://www.youtube-nocookie.com" />
  <link rel="preconnect" href="https://i.ytimg.com" crossorigin />
  <meta name="robots" content="index, follow" />

  <meta property="og:type" content="video.other" />
  <meta property="og:site_name" content="Destination FAANG" />
  <meta property="og:title" content="{e(title)}" />
  <meta property="og:description" content="{e(desc)}" />
  <meta property="og:url" content="{page_url}" />
  <meta property="og:image" content="{e(thumb)}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{e(title)}" />
  <meta name="twitter:description" content="{e(desc)}" />
  <meta name="twitter:image" content="{e(thumb)}" />

  {jsonld}

  <link rel="stylesheet" href="../assets/styles.css?v={CSS_VERSION}" />
</head>
<body>
{nav_html(prefix="../")}

  <main class="wrap video-main">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="../index.html">Home</a> <span>›</span>
      <a href="../index.html?cat={e(v.get('category', 'all'))}">{e(label)}</a> <span>›</span>
      <span class="breadcrumb-current">{e(title)}</span>
    </nav>

    <article class="video-article">
      <div class="video-embed">
        <iframe
          src="https://www.youtube-nocookie.com/embed/{e(vid)}"
          title="{e(title)}"
          loading="lazy"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          referrerpolicy="strict-origin-when-cross-origin"
          allowfullscreen></iframe>
      </div>

      <h1 class="video-title">{e(title)}</h1>
      <div class="video-meta">
        <span class="badge {e(v.get('category', 'misc'))}">{e(label)}</span>
        {diff_pill}
        {f'<span class="date">{e(pub_human)}</span>' if pub_human else ''}
      </div>
      {f'<div class="pills">{pills}</div>' if pills else ''}

      {f'<p class="video-desc">{e(desc)}</p>' if desc else ''}

      <div class="video-cta">
        <a class="nav-btn nav-btn--support" href="{e(watch_url)}" target="_blank" rel="noopener noreferrer">
          <span aria-hidden="true">▶</span> Watch on YouTube
        </a>
        <a class="nav-btn nav-btn--ghost" href="{CHANNEL}?sub_confirmation=1" target="_blank" rel="noopener noreferrer">Subscribe</a>
        <a class="nav-btn nav-btn--ghost" href="../resources.html">Practice resources</a>
      </div>

      <p class="video-back">
        <a href="../index.html?cat={e(v.get('category', 'all'))}">← More {e(label)} videos</a>
      </p>
    </article>
  </main>

{footer_html(prefix="../")}
</body>
</html>
"""


def write_video_pages(videos):
    os.makedirs(VIDEO_DIR, exist_ok=True)
    written = 0
    for v in videos:
        vid = v.get("id")
        if not vid or not re.fullmatch(r"[A-Za-z0-9_-]+", vid):
            continue
        path = os.path.join(VIDEO_DIR, f"{vid}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(video_page_html(v))
        written += 1
    return written


def main():
    videos = load_videos()
    inject_jsonld(build_jsonld(videos))
    pages = write_video_pages(videos)
    write_sitemap(videos)
    write_robots()
    print(
        f"SEO assets generated: JSON-LD ({len(videos)} videos), "
        f"{pages} video pages in /{VIDEO_DIR}/, sitemap.xml, robots.txt"
    )


if __name__ == "__main__":
    main()
