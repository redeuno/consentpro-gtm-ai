"""Exercise installation outside the checkout and detect unsafe package changes."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


package = load("skill_package", "package-skills.py")
catalogue = load("catalogue", "check-mcp-catalogue.py")
repository = load("repository_check", "check-repository.py")


class SkillPackages(unittest.TestCase):
    def test_dry_run_then_install_outside_checkout_then_repeat(self):
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()):
            output = Path(folder) / "installed"
            package.install(output)
            self.assertFalse(output.exists())
            package.install(output, apply=True)
            before = {p: p.read_bytes() for p in output.rglob("*") if p.is_file()}
            package.install(output, apply=True)
            self.assertEqual(before, {p: p.read_bytes() for p in output.rglob("*") if p.is_file()})
            for name in package.SKILLS:
                root = (output / name).resolve()
                for script in ("inspect-site.py", "wire-consent.py", "authorise.py", "audit-container.py"):
                    result = subprocess.run([sys.executable, "-B", str(root / "scripts" / script), "--help"],
                                            cwd=folder, capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                for path in root.rglob("*.md"):
                    for match in package.LINK.finditer(path.read_text()):
                        target = package.urlsplit(match[2])
                        if not target.scheme and target.path:
                            resolved = (path.parent / target.path).resolve()
                            self.assertTrue(resolved.is_relative_to(root), str(path) + ": " + match[2])
                            self.assertTrue(resolved.exists(), str(resolved))

    def test_modified_install_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()):
            output = Path(folder)
            package.install(output, apply=True)
            target = output / "consent-pro/SKILL.md"
            target.write_text("local customization")
            with self.assertRaisesRegex(ValueError, "Refusing"):
                package.install(output, apply=True)
            self.assertEqual(target.read_text(), "local customization")

    def test_symlink_install_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            (output / "consent-pro").symlink_to(output / "absent")
            with self.assertRaisesRegex(ValueError, "Refusing"):
                package.install(output, apply=True)


class CatalogueDrift(unittest.TestCase):
    def test_command_distinguishes_equal_changed_and_invalid_contracts(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            before, after = root / "before.json", root / "after.json"
            payload = {"tools": [{"name": "read", "inputSchema": {"type": "object"},
                                  "annotations": {"readOnlyHint": True}}]}
            before.write_text(json.dumps(payload))
            after.write_text(json.dumps(payload))
            argv = ["check-mcp-catalogue.py", str(before), str(after)]
            with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()), \
                    contextlib.redirect_stderr(io.StringIO()):
                catalogue.main()
                payload["tools"][0]["annotations"]["readOnlyHint"] = False
                after.write_text(json.dumps(payload))
                with self.assertRaises(SystemExit) as changed:
                    catalogue.main()
                self.assertEqual(changed.exception.code, 1)
                after.write_text('{"tools": []}')
                with self.assertRaises(SystemExit) as invalid:
                    catalogue.main()
                self.assertEqual(invalid.exception.code, 2)

    def test_add_remove_and_change_contract(self):
        before = {"read": {"annotations": {"readOnlyHint": True}}, "old": {}}
        after = {"read": {"annotations": {"readOnlyHint": False}}, "write": {}}
        self.assertEqual(catalogue.compare(before, before), {"added": [], "removed": [], "changed": []})
        self.assertEqual(catalogue.compare(before, after),
                         {"added": ["write"], "removed": ["old"], "changed": ["read"]})

    def test_duplicate_tool_cannot_hide_drift(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "catalogue.json"
            tool = {"name": "read", "inputSchema": {"type": "object"}}
            path.write_text(json.dumps({"tools": [tool, tool]}))
            with self.assertRaisesRegex(ValueError, "duplicate"):
                catalogue.contracts(path)


class RepositoryChecks(unittest.TestCase):
    def test_command_fails_on_broken_local_link(self):
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            root = Path(folder)
            (root / "README.md").write_text("Valid guide\n")
            with mock.patch.object(sys, "argv", ["check-repository.py", "--root", str(root)]):
                repository.main()
                (root / "README.md").write_text("[Missing](missing.md)\n")
                with self.assertRaises(SystemExit) as broken:
                    repository.main()
                self.assertEqual(broken.exception.code, 1)

    def test_missing_link_and_authored_dash_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "README.md").write_text("[Guide](guide.md)\n")
            self.assertEqual(len(repository.check(root)[1]), 1)
            (root / "guide.md").write_text("Valid guide\n")
            self.assertEqual(repository.check(root), (1, []))
            (root / "guide.md").write_text("Invalid " + chr(0x2014) + " punctuation\n")
            self.assertEqual(len(repository.check(root)[1]), 1)


if __name__ == "__main__":
    unittest.main()
