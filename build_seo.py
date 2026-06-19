"""Generate SEO assets from videos.json.

Produces:
  - sitemap.xml          (homepage entry with the latest upload as lastmod)
  - robots.txt           (allow all + sitemap reference)
  - injects JSON-LD structured data into index.html between the
    <!-- SEO:JSONLD:START --> / <!-- SEO:JSONLD:END --> markers:
      * WebSite (with a SearchAction sitelinks search box)
      * ItemList of VideoObject entries (rich-result eligible)

Run this whenever videos.json changes:
    python build_seo.py
"""

import json
import re
from datetime import date

SITE = "https://destinationfaang.com"
INDEX = "index.html"
VIDEOS = "videos.json"
MAX_VIDEO_OBJECTS = 413  # cap structured-data size if the catalog grows huge


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
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"  <url>\n    <loc>{SITE}/</loc>\n    <lastmod>{lastmod}</lastmod>\n"
        "    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n  </url>\n"
        "</urlset>\n"
    )
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(xml)


def write_robots():
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")


def main():
    videos = load_videos()
    inject_jsonld(build_jsonld(videos))
    write_sitemap(videos)
    write_robots()
    print(f"SEO assets generated: JSON-LD ({len(videos)} videos), sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
