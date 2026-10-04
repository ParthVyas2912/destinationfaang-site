import html
import json
import re
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://destinationengineer.com"
BRAND = "Destination Engineer"
FORMER = "(formerly Destination FAANG)"
BRAND_ASSET_VERSION = "20261004-top-arrow"
STATIC = ["index.html", "about.html", "resources.html", "start-here.html", "404.html"]


class HeadAssets(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links = {}
        self.meta = {}
        self.brand_images = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link":
            self.links[attrs.get("rel")] = attrs.get("href", "")
        elif tag == "meta":
            self.meta[attrs.get("property") or attrs.get("name")] = attrs.get("content", "")
        elif tag == "img" and "brand-logo" in attrs.get("class", "").split():
            self.brand_images.append(attrs["src"])


class BrandingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.videos = json.loads((ROOT / "videos.json").read_text(encoding="utf-8"))["videos"]

    def test_static_and_generated_page_identity(self):
        pages = STATIC + [f"v/{v['id']}.html" for v in self.videos]
        for name in pages:
            with self.subTest(page=name):
                file = ROOT / name
                source = file.read_text(encoding="utf-8")
                head = HeadAssets(source)
                self.assertIn(f"<span>{BRAND}</span>", source)
                self.assertIn(f"<strong>{BRAND}</strong>", source)
                self.assertIn(f"<small>{FORMER}</small>", source)
                self.assertIn(f'<span class="brand-former">{FORMER}</span>', source)
                self.assertIn(f'alt="{BRAND} logo"', source)
                remaining = source.replace(FORMER, "").replace(
                    '"alternateName":"Destination FAANG"', ""
                )
                self.assertNotRegex(remaining, r"(?i)\bdestination\s+faang\b")
                if name != "404.html":
                    canonical = SITE + "/" + ("" if name == "index.html" else name)
                    self.assertEqual(head.links["canonical"], canonical)
                    self.assertEqual(head.meta["og:site_name"], BRAND)
                for key in ("icon", "apple-touch-icon"):
                    asset = urlsplit(head.links[key]).path
                    target = ROOT / asset.lstrip("/") if asset.startswith("/") else file.parent / asset
                    self.assertTrue(target.is_file(), target)
                    self.assertEqual(parse_qs(urlsplit(head.links[key]).query).get("v"), [BRAND_ASSET_VERSION])
                self.assertTrue(urlsplit(head.links["icon"]).path.endswith("logo.svg"))
                self.assertTrue(urlsplit(head.links["apple-touch-icon"]).path.endswith("apple-touch-icon.png"))
                self.assertEqual(len(head.brand_images), 1)
                self.assertEqual(
                    parse_qs(urlsplit(head.brand_images[0]).query).get("v"), [BRAND_ASSET_VERSION]
                )
                for key in ("og:image", "twitter:image"):
                    image = urlsplit(head.meta.get(key, ""))
                    if image.path.endswith("og-image.png"):
                        self.assertEqual(parse_qs(image.query).get("v"), [BRAND_ASSET_VERSION])

    def test_video_identity_and_catalog_titles_are_preserved(self):
        for video in self.videos:
            with self.subTest(video=video["id"]):
                for field in ("title", "description"):
                    self.assertNotRegex(video.get(field, ""), r"(?i)\bdestination\s+faang\b")
                source = (ROOT / "v" / f"{video['id']}.html").read_text(encoding="utf-8")
                self.assertIn(
                    f"<title>{html.escape(video['title'])} | {BRAND}</title>", source
                )
                self.assertIn(f"https://www.youtube-nocookie.com/embed/{video['id']}", source)
                self.assertIn("youtube.com/channel/UC49H999tjewVmrdLoCWCs4g", source)
                self.assertIn("linkedin.com/company/107371838/", source)

    def test_sitemap_and_domain(self):
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        actual = {node.text for node in root.findall("{*}url/{*}loc")}
        expected = {SITE + "/"}
        expected.update(SITE + "/" + p for p in STATIC if p not in ("index.html", "404.html"))
        expected.update(SITE + f"/v/{v['id']}.html" for v in self.videos)
        self.assertEqual(actual, expected)
        self.assertIn(f"Sitemap: {SITE}/sitemap.xml", (ROOT / "robots.txt").read_text())
        self.assertEqual((ROOT / "CNAME").read_text().strip(), "destinationengineer.com")

    def test_homepage_keeps_legacy_search_identity(self):
        source = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn(f"<title>{BRAND} {FORMER}</title>", source)
        data = [
            json.loads(block) for block in re.findall(
                r'<script type="application/ld\+json">(.*?)</script>', source, re.DOTALL
            )
        ]
        website = next(item for item in data if item["@type"] == "WebSite")
        self.assertEqual(website["name"], BRAND)
        self.assertEqual(website["alternateName"], "Destination FAANG")
        self.assertEqual(website["url"], SITE + "/")

    def test_homepage_intro_is_one_sentence(self):
        source = (ROOT / "index.html").read_text(encoding="utf-8")
        intro = source.split('<div class="hero">', 1)[1].split('<div class="search-box">', 1)[0]
        heading = re.search(r'<h1 class="hero-title">(.*?)</h1>', intro, re.DOTALL)
        self.assertIsNotNone(heading)
        self.assertEqual(
            html.unescape(re.sub(r"<[^>]+>", "", heading.group(1))),
            "Become a great engineer and solve the world's problems together.",
        )
        self.assertNotIn("<br", intro)
        self.assertNotIn("<p", intro)

    def test_artwork_sizes_and_vectors(self):
        sizes = {
            "logo.png": (800, 800),
            "apple-touch-icon.png": (180, 180),
            "og-image.png": (1200, 630),
            "brand/youtube-banner.png": (2560, 1440),
            "brand/youtube-watermark.png": (150, 150),
            "brand/linkedin-logo.png": (400, 400),
            "brand/linkedin-cover.png": (1128, 191),
        }
        for name, size in sizes.items():
            with self.subTest(asset=name), Image.open(ROOT / "assets" / name) as img:
                self.assertEqual(img.size, size)
                img.verify()
        for name in ("logo.svg", "og-image.svg", "brand/mark-transparent.svg", "brand/mark-monochrome.svg"):
            root = ET.parse(ROOT / "assets" / name).getroot()
            self.assertEqual(root.find("{*}title").text, BRAND)

    def test_original_angular_d_and_top_arrow(self):
        root = ET.parse(ROOT / "assets" / "logo.svg").getroot()
        paths = {node.attrib["fill"]: node.attrib["d"] for node in root.findall("{*}path")}
        self.assertEqual(
            paths["#f4f6ed"],
            "M104,140 L202,140 L268,206 L268,306 L202,372 L104,372 Z "
            "M150,188 L184,188 L220,224 L220,288 L184,324 L150,324 Z",
        )
        self.assertIn("L428,176", paths["#e5ff46"])
        self.assertNotIn("L428,256", paths["#e5ff46"])
        with Image.open(ROOT / "assets" / "logo.png") as img:
            scale = img.width / 512
            self.assertEqual(
                img.getpixel((round(416 * scale), round(176 * scale)))[:3], (229, 255, 70)
            )
            self.assertEqual(
                img.getpixel((round(416 * scale), round(256 * scale)))[:3], (11, 13, 19)
            )


if __name__ == "__main__":
    unittest.main()
