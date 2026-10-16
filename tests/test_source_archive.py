"""Exercise archive validation with synthetic documents and no private source files."""

import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "source_archive", ROOT / "docs/06-agent-readiness/checks/verify-snapshot.py")
archive = importlib.util.module_from_spec(spec)
spec.loader.exec_module(archive)


class ArchiveChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.url = "https://docs.consentpro.com/web-app/"
        self.ref = "https://docs.consentpro.com/runtime/example"
        self.asset = "https://docs.consentpro.com/example.png"
        self.put("image.png", b"\x89PNG\r\n\x1a\nsynthetic bytes")
        self.put("template.tpl", b"synthetic template")
        template_url = "https://docs.consentpro.com/example.tpl"
        page = {"metadata": {"sourceURL": self.url, "statusCode": 200},
                "markdown": "Synthetic public documentation. " * 10 +
                            "\n![Synthetic](" + self.asset + ")\n",
                "links": [self.ref, template_url]}
        ref = {"metadata": {"sourceURL": self.ref, "statusCode": 200},
               "markdown": "Synthetic runtime reference. " * 10, "links": []}
        self.put_json("web-app.json", {"pages": [page]})
        self.put_json("references.json", {"pages": [ref]})
        self.put_json("map.json", {"links": [self.url]})
        self.put("sitemap.xml", ("<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">"
                                  "<url><loc>" + self.url + "</loc></url></urlset>").encode())
        self.put_json("mcp-catalogue.json", {"tools": [
            {"name": "synthetic_read", "annotations": {"readOnlyHint": True}}]})
        self.put_json("assets-index.json", {"failures": [], "assets": [
            self.record("image.png", url=self.asset, kind="image"),
            self.record("template.tpl", url=template_url, kind="template")],
            "source_files": [self.record("web-app.json")]})

    def put(self, name, data):
        (self.root / name).write_bytes(data)

    def put_json(self, name, value):
        self.put(name, json.dumps(value).encode())

    def record(self, path, **extra):
        data = (self.root / path).read_bytes()
        return {"path": path, "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(), **extra}

    def run_archive(self):
        output = io.StringIO()
        with mock.patch("sys.argv", ["verify-snapshot.py", "--root", str(self.root),
                                      "--self-check"]), contextlib.redirect_stdout(output):
            archive.main()
        return json.loads(output.getvalue())

    def test_complete_archive_and_deliberate_failures(self):
        result = self.run_archive()
        self.assertEqual(result["status"], "verified")
        self.assertEqual(result["assets_verified"], 2)
        self.assertEqual(len(result["negative_controls"]), 4)
        self.assertTrue(all(result["negative_controls"].values()))

    def test_changed_file_is_rejected(self):
        self.put("image.png", b"broken")
        with self.assertRaisesRegex(ValueError, "Size mismatch"):
            self.run_archive()

    def test_missing_page_is_rejected(self):
        self.put_json("web-app.json", {"pages": []})
        with self.assertRaisesRegex(ValueError, "inventory"):
            self.run_archive()

    def test_archive_escape_is_rejected(self):
        with mock.patch.object(archive, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "outside"):
                archive.check_file({"path": "../outside", "bytes": 0, "sha256": ""})

    def test_private_location_is_never_guessed(self):
        with mock.patch("sys.argv", ["verify-snapshot.py"]), \
                contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as error:
                archive.main()
        self.assertEqual(error.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
