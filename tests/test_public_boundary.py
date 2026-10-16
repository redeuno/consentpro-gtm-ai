"""Reject raw source collections without depending on their private contents."""

import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("repository_boundary", ROOT / "scripts/check-repository.py")
repository = importlib.util.module_from_spec(spec)
spec.loader.exec_module(repository)


class PublicBoundary(unittest.TestCase):
    def test_raw_evidence_is_rejected_even_when_not_markdown(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "README.md").write_text("Customer instructions\n")
            self.assertEqual(repository.check(root), (0, []))
            for name in ("docs/06-agent-readiness/sources/capture.json",
                         "private-evidence/capture.png", "customer-data/export.json"):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"synthetic")
                self.assertIn("private source evidence", " ".join(repository.check(root)[1]))
                path.unlink()
            self.assertEqual(repository.check(root), (0, []))


if __name__ == "__main__":
    unittest.main()
