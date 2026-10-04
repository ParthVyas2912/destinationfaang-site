import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import build_from_ytdlp
import build_seo
import fetch_videos
from site_branding import rebrand_catalog, rebrand_text


class SiteBrandingTests(unittest.TestCase):
    def catalog(self):
        return {
            "channelId": "UC-original-channel",
            "channelTitle": "Destination FAANG",
            "count": 1,
            "videos": [{
                "id": "original-id",
                "title": "Destination FAANG Channel Update",
                "description": "A Destination FAANG lesson for FAANG interviews.",
                "url": "https://www.youtube.com/watch?v=original-id",
                "thumbnail": "https://i.ytimg.com/vi/original-id/mqdefault.jpg",
                "publishedAt": "2026-09-22T04:23:21Z",
                "category": "system-design",
                "companies": ["Google"],
                "topics": [],
            }],
        }

    def test_rebrands_only_catalog_text_without_mutating_original(self):
        original = self.catalog()
        snapshot = copy.deepcopy(original)
        branded = rebrand_catalog(original)
        self.assertEqual(original, snapshot)
        self.assertEqual(branded["channelTitle"], "Destination Engineer")
        expected = copy.deepcopy(snapshot)
        expected["channelTitle"] = "Destination Engineer"
        expected["videos"][0]["title"] = "Destination Engineer Channel Update"
        expected["videos"][0]["description"] = "A Destination Engineer lesson for FAANG interviews."
        self.assertEqual(branded, expected)

    def test_normalization_is_idempotent(self):
        branded = rebrand_catalog(self.catalog())
        self.assertEqual(rebrand_catalog(branded), branded)

    def test_case_variants_and_external_handles(self):
        self.assertEqual(rebrand_text("DESTINATION FAANG / destination faang"),
                         "Destination Engineer / Destination Engineer")
        external = "https://www.youtube.com/@DestinationFAANG FAANG interviews"
        self.assertEqual(rebrand_text(external), external)

    def test_absent_and_null_optional_fields_are_preserved(self):
        payload = {"videos": [{"id": "one"}, {"id": "two", "description": None}]}
        self.assertEqual(rebrand_catalog(payload), payload)

    def test_api_import_brands_after_categorization_and_before_truncation(self):
        video = self.catalog()["videos"][0]
        video["description"] = "Destination FAANG " + "x" * 320
        original = copy.deepcopy(video)

        def enrich(value):
            self.assertEqual(value["title"], original["title"])
            self.assertEqual(value["description"], original["description"])
            value["category"] = "system-design"

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "videos.json"
            args = ["fetch_videos.py", "--channel-id", "UC-original-channel",
                    "--api-key", "test-placeholder", "--out", str(output)]
            with patch.object(sys, "argv", args), \
                    patch.object(fetch_videos, "get_uploads_playlist", return_value="uploads"), \
                    patch.object(fetch_videos, "get_all_videos", return_value=[video]), \
                    patch.object(fetch_videos, "enrich", side_effect=enrich):
                fetch_videos.main()
            data = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(data["videos"][0]["title"], "Destination Engineer Channel Update")
            self.assertTrue(data["videos"][0]["description"].startswith("Destination Engineer "))
            self.assertEqual(len(data["videos"][0]["description"]), 300)
            self.assertEqual(data["videos"][0]["url"], original["url"])

    def test_ytdlp_import_uses_the_same_branding(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "channel.json"
            output = Path(directory) / "videos.json"
            source.write_text(json.dumps({
                "channel_id": "UC-original-channel",
                "title": "Destination FAANG",
                "entries": [{"id": "original-id", "title": "Destination FAANG Channel Update"}],
            }), encoding="utf-8")
            with patch.object(sys, "argv", ["build_from_ytdlp.py", str(source), str(output)]):
                build_from_ytdlp.main()
            data = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(data["channelTitle"], "Destination Engineer")
            self.assertEqual(data["videos"][0]["title"], "Destination Engineer Channel Update")
            self.assertEqual(data["videos"][0]["id"], "original-id")

    def test_seo_build_updates_the_catalog_consumed_by_the_browser(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "videos.json"
            source.write_text(json.dumps(self.catalog()), encoding="utf-8")
            with patch.object(build_seo, "VIDEOS", str(source)):
                videos = build_seo.load_videos()
                content = source.read_bytes()
                self.assertEqual(build_seo.load_videos(), videos)
                self.assertEqual(source.read_bytes(), content)
            self.assertEqual(json.loads(content)["videos"], videos)
            page = build_seo.video_page_html(videos[0])
            self.assertIn("<title>Destination Engineer Channel Update | Destination Engineer</title>", page)
            self.assertIn("(formerly Destination FAANG)", page)


if __name__ == "__main__":
    unittest.main()
