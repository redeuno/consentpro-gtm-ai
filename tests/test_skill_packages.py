"""Exercise installation outside the checkout and detect unsafe package changes."""

import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock
import zipfile

ROOT = Path(__file__).resolve().parent.parent


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


package = load("skill_package", "package-skills.py")
catalogue = load("catalogue", "check-mcp-catalogue.py")
repository = load("repository_check", "check-repository.py")


def committed_sources(root, attributes=None):
    paths = package.APPROVED_SOURCES | set(package.BUILD_INPUTS)
    for relative in paths:
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    if attributes is not None:
        (root / ".gitattributes").write_bytes(attributes)
    (root / "checkout-control.txt").write_bytes(b"checkout control\n")
    env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1")

    def git(*args):
        return subprocess.run(["git", "-C", str(root), *args], env=env,
                              capture_output=True, text=True, check=True).stdout.strip()

    git("init", "--quiet")
    git("config", "core.autocrlf", "false")
    git("add", ".")
    git("-c", "user.name=Package test", "-c", "user.email=package-test@example.invalid",
        "commit", "--quiet", "-m", "test: create disposable source fixture")
    return git, paths | {"checkout-control.txt"}


def checkout_with_autocrlf(root, git, paths):
    git("config", "core.autocrlf", "true")
    for relative in paths:
        (root / relative).unlink()
    git("reset", "--hard", "--quiet", "HEAD")


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
                    for match in package.LINK.finditer(path.read_text(encoding="utf-8")):
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
            target.write_text("local customization", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Refusing"):
                package.install(output, apply=True)
            self.assertEqual(target.read_text(encoding="utf-8"), "local customization")

    def test_symlink_install_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)
            (output / "consent-pro").symlink_to(output / "absent")
            with self.assertRaisesRegex(ValueError, "Refusing"):
                package.install(output, apply=True)

    def test_manifest_identifies_content_and_excludes_private_sources(self):
        files = package.build_files("consent-pro")
        manifest = json.loads(files["package-manifest.json"])
        self.assertEqual(manifest["format"], 2)
        self.assertEqual(manifest["version"], "0.2.1")
        self.assertEqual(manifest["channel"], "development")
        self.assertEqual(set(manifest["source"]), {"commit", "dirty", "content_sha256"})
        self.assertEqual(len(manifest["source"]["content_sha256"]), 64)
        self.assertIsInstance(manifest["source"]["dirty"], bool)
        self.assertEqual(manifest["files"], {path: package.digest(data)
                         for path, data in files.items() if path != "package-manifest.json"})
        self.assertFalse(any("sources/" in path or path.endswith("readiness/README.md")
                             or path.startswith("tests/") for path in files))
        for path, data in files.items():
            if path.endswith(".md"):
                self.assertNotIn(b"/blob/main/", data)

    def test_zip_cli_is_explicit_reproducible_and_runs_after_extraction(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            command = [sys.executable, "-B", str(ROOT / "scripts/package-skills.py"),
                       "--output", str(root / "skills"), "--archives", str(root / "release")]
            dry = subprocess.run(command, cwd=root, capture_output=True, text=True)
            self.assertEqual(dry.returncode, 0, dry.stderr)
            self.assertFalse((root / "skills").exists())
            self.assertFalse((root / "release").exists())
            first = subprocess.run(command + ["--apply"], cwd=root, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            before = {p.name: p.read_bytes() for p in (root / "release").iterdir()}
            repeated = subprocess.run(command + ["--apply"], cwd=root, capture_output=True, text=True)
            self.assertEqual(repeated.returncode, 0, repeated.stderr)
            self.assertEqual(before, {p.name: p.read_bytes() for p in (root / "release").iterdir()})
            with contextlib.redirect_stdout(io.StringIO()):
                package.install(root / "other-skills", True, root / "other-release")
            self.assertEqual(before, {p.name: p.read_bytes() for p in (root / "other-release").iterdir()})
            for line in before["SHA256SUMS"].decode().splitlines():
                expected, name = line.split("  ")
                self.assertEqual(package.digest(before[name]), expected)
                with zipfile.ZipFile(io.BytesIO(before[name])) as archive:
                    roots = {entry.split("/")[0] for entry in archive.namelist()}
                    self.assertEqual(len(roots), 1)
                    skill = roots.pop()
                    self.assertIn(skill, package.SKILLS)
                    manifest = json.loads(archive.read(skill + "/package-manifest.json"))
                    self.assertEqual(set(archive.namelist()),
                                     {skill + "/" + p for p in manifest["files"]}
                                     | {skill + "/package-manifest.json"})
                    for path, sha in manifest["files"].items():
                        self.assertEqual(package.digest(archive.read(skill + "/" + path)), sha)
                    archive.extractall(root / "extracted")
                    script = root / "extracted" / skill / "scripts/inspect-site.py"
                    check = subprocess.run([sys.executable, "-B", str(script), "--help"],
                                           cwd=root, capture_output=True, text=True)
                    self.assertEqual(check.returncode, 0, check.stderr)

    def test_modified_archive_is_refused_before_installing(self):
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()):
            root = Path(folder).resolve()
            package.install(root / "one", True, root / "release")
            target = next((root / "release").glob("*.zip"))
            target.write_bytes(b"modified archive")
            with self.assertRaisesRegex(ValueError, "differing archive"):
                package.install(root / "two", True, root / "release")
            self.assertFalse((root / "two").exists())
            self.assertEqual(target.read_bytes(), b"modified archive")

    def test_added_file_or_symlink_in_package_is_refused(self):
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()):
            output = Path(folder).resolve()
            package.install(output, True)
            extra = output / "consent-pro/private-policy.md"
            extra.write_text("not distributed", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Refusing"):
                package.install(output, True)
            extra.unlink()
            extra.symlink_to(output / "missing")
            with self.assertRaisesRegex(ValueError, "Refusing"):
                package.install(output, True)

    def test_output_symlink_and_archive_inside_skill_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            actual = root / "actual"
            actual.mkdir()
            (root / "linked").symlink_to(actual, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symbolic"):
                package.install(root / "linked/skills", True)
            with self.assertRaisesRegex(ValueError, "inside an installed skill"):
                package.install(root / "skills", True, root / "skills/consent-pro/release")
            self.assertFalse((root / "skills").exists())

    def test_cli_rejects_archive_nesting_hidden_by_parent_segments(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            for output, archives in (
                    (root / "skills", root / "skills/../skills/consent-pro/archives"),
                    (root / "intermediate/../skills", root / "skills/consent-pro/archives")):
                with self.subTest(output=output, archives=archives):
                    result = subprocess.run([sys.executable, "-B", str(ROOT / "scripts/package-skills.py"),
                                             "--output", str(output), "--archives", str(archives), "--apply"],
                                            cwd=root, capture_output=True, text=True)
                    self.assertEqual(result.returncode, 1, result.stdout)
                    self.assertIn("inside an installed skill", result.stderr)
                    self.assertFalse((root / "skills").exists())
                    self.assertFalse((root / "intermediate").exists())

    def test_parent_segments_are_normalized_before_archive_boundary_check(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            for output, archives in (
                    (root / "skills", root / "skills/../skills/consent-pro/archives"),
                    (root / "intermediate/../skills", root / "skills/consent-pro/archives")):
                with self.subTest(output=output), self.assertRaisesRegex(ValueError, "inside an installed skill"):
                    package.install(output, True, archives)
            self.assertFalse((root / "skills").exists())

    def test_archive_boundary_rejects_case_and_normalization_aliases(self):
        parent = PurePosixPath("/delivery/caf\u00e9/skills/consent-pro")
        for candidate in (
                "/delivery/caf\u00e9/skills/CONSENT-PRO/archives",
                "/DELIVERY/caf\u00e9/SKILLS/CONSENT-PRO/archives",
                "/delivery/cafe\u0301/skills/consent-pro/archives",
                "/delivery/caf\u00e9/skills/consent-pro. /archives"):
            with self.subTest(candidate=candidate):
                self.assertTrue(package.archive_within_skill(PurePosixPath(candidate), parent))
        self.assertFalse(package.archive_within_skill(PurePosixPath("/delivery/releases"), parent))
        self.assertFalse(package.archive_within_skill(PurePosixPath("/delivery/caf\u00e9/skills/consent-pro-extra"), parent))

    def test_cli_case_alias_cannot_add_files_to_installed_package(self):
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()):
            root = Path(folder).resolve()
            output = root / "skills"
            alias = output / "CONSENT-PRO"
            command = [sys.executable, "-B", str(ROOT / "scripts/package-skills.py"),
                       "--output", str(output), "--archives", str(alias / "archives"), "--apply"]
            first = subprocess.run(command, cwd=root, capture_output=True, text=True)
            self.assertEqual(first.returncode, 1, first.stdout)
            self.assertIn("inside an installed skill", first.stderr)
            self.assertFalse(output.exists())
            package.install(output, True)
            if alias.exists():
                self.assertTrue(alias.samefile(output / "consent-pro"))
            before = {p.relative_to(output).as_posix(): p.read_bytes()
                      for p in output.rglob("*") if p.is_file()}
            repeated = subprocess.run(command, cwd=root, capture_output=True, text=True)
            self.assertEqual(repeated.returncode, 1, repeated.stdout)
            self.assertIn("inside an installed skill", repeated.stderr)
            self.assertFalse((output / "consent-pro/archives").exists())
            package.install(output, True)
            self.assertEqual(before, {p.relative_to(output).as_posix(): p.read_bytes()
                                     for p in output.rglob("*") if p.is_file()})

    def test_private_sources_and_destination_traversal_are_rejected(self):
        for source, destination, message in (
                (ROOT / "docs/06-agent-readiness/sources/private.md", Path("private.md"), "not approved"),
                (ROOT / "SECURITY.md", Path("../outside.md"), "Unsafe"),
                (ROOT / "SECURITY.md", Path("/outside.md"), "Unsafe"),
                (ROOT / "SECURITY.md", Path("package-manifest.json"), "reserved")):
            with self.subTest(destination=destination), mock.patch.object(
                    package, "source_map", return_value={source: destination}):
                with self.assertRaisesRegex(ValueError, message):
                    package.build_files("consent-pro")

    def test_only_explicit_runtime_files_are_selected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            (root / "docs/reference").mkdir(parents=True)
            (root / "docs/reference/private-policy.md").write_text("private", encoding="utf-8")
            with mock.patch.object(package, "ROOT", root):
                selected = package.source_map("consent-pro")
                self.assertNotIn(root / "docs/reference/private-policy.md", selected)

    def test_interface_metadata_is_posix_with_windows_path_semantics(self):
        for path_type in (Path, PureWindowsPath):
            with self.subTest(path_type=path_type), mock.patch.object(package, "Path", path_type):
                self.assertEqual(package.interface_metadata("skills/consent-pro/SKILL.md"),
                                 "skills/consent-pro/agents/openai.yaml")
                self.assertEqual(package.interface_metadata("skill/SKILL.md"), "skill/agents/openai.yaml")
        self.assertIn("skills/consent-pro/agents/openai.yaml", package.APPROVED_SOURCES)
        self.assertIn("skill/agents/openai.yaml", package.APPROVED_SOURCES)

    def test_missing_or_symbolic_source_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            (root / "SECURITY.md").symlink_to(ROOT / "SECURITY.md")
            with mock.patch.object(package, "ROOT", root):
                with self.assertRaisesRegex(ValueError, "symbolic"):
                    package.read_source(root / "SECURITY.md", {"SECURITY.md"})
                with self.assertRaisesRegex(ValueError, "Missing"):
                    package.read_source(root / "LICENSE", {"LICENSE"})

    def test_existing_private_file_is_rejected_before_reading(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            target = root / "private-policy.md"
            target.write_text("synthetic private material", encoding="utf-8")
            with mock.patch.object(package, "ROOT", root), self.assertRaisesRegex(ValueError, "not approved"):
                package.read_source(target, {"SECURITY.md"})

    def test_links_are_closed_to_packaged_dependencies(self):
        source = ROOT / "docs/00-the-journey.md"
        destination = Path("docs/00-the-journey.md")
        sources = package.source_map("consent-pro")
        valid = "Read [setup](07-agent-installation/README.md#start-in-your-current-chat)."
        self.assertEqual(package.rewrite_links(valid, source, destination, sources), valid)
        omitted = package.rewrite_links("[Evidence](06-agent-readiness/README.md)",
                                        source, destination, sources)
        self.assertEqual(omitted, "Evidence (maintainer reference omitted from this package)")
        for link in ("06-agent-readiness/sources/private.md", "reference/missing.md",
                     "../../../../outside.md", "%2e%2e/%2e%2e/outside.md",
                     "https://github.com/redeuno/consentpro-gtm-ai/blob/main/README.md",
                     "https://raw.githubusercontent.com/redeuno/consentpro-gtm-ai/main/README.md",
                     "https://github.com/redeuno/consentpro-gtm-ai/blob/v1/docs/06-agent-readiness/sources/x.json",
                     "file:///tmp/private.md", "//private.example/path", "reference/onboarding.md?private=1"):
            with self.subTest(link=link), self.assertRaises(ValueError):
                package.rewrite_links("[Required](" + link + ")", source, destination, sources)

    def test_zip_rejects_unsafe_members_and_skill_names(self):
        for path in ("../private.md", "/private.md", "a/../private.md", "a\\private.md", ".env"):
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "Unsafe"):
                package.archive_bytes("consent-pro", {path: b"content"})
        with self.assertRaisesRegex(ValueError, "Unknown"):
            package.archive_bytes("../private", {"SKILL.md": b"content"})

    def test_preview_requires_clean_recorded_source_and_declared_channel(self):
        with mock.patch.object(package, "git_state", return_value={"commit": "a" * 40, "dirty": True}):
            with self.assertRaisesRegex(ValueError, "clean Git"):
                package.build_files("consent-pro", "preview")
        with self.assertRaisesRegex(ValueError, "channel must match"):
            package.build_files("consent-pro", "stable")

    def test_clean_preview_matches_its_commit_and_hidden_edits_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            git, _ = committed_sources(root)
            commit = git("rev-parse", "HEAD")
            with mock.patch.object(package, "ROOT", root):
                bundle = package.build_files("consent-pro", "preview")
                manifest = json.loads(bundle["package-manifest.json"])
                self.assertEqual(manifest["source"]["commit"], commit)
                self.assertFalse(manifest["source"]["dirty"])
                self.assertEqual(manifest["channel"], "preview")
                git("update-index", "--assume-unchanged", "LICENSE")
                (root / "LICENSE").write_text("hidden edit", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "does not match the recorded commit"):
                    package.build_files("consent-pro", "preview")

    def test_autocrlf_checkout_keeps_identical_preview_archives(self):
        with tempfile.TemporaryDirectory() as folder, tempfile.TemporaryDirectory() as artifacts:
            root = Path(folder).resolve()
            git, paths = committed_sources(root)
            with mock.patch.object(package, "ROOT", root):
                before = package.archive_files({name: package.build_files(name, "preview")
                                                for name in package.SKILLS})
            checkout_with_autocrlf(root, git, paths)
            self.assertEqual((root / "checkout-control.txt").read_bytes(), b"checkout control\r\n")
            self.assertEqual(git("status", "--porcelain"), "")
            for relative in package.APPROVED_SOURCES | set(package.BUILD_INPUTS):
                self.assertNotIn(b"\r\n", (root / relative).read_bytes(), relative)
            with mock.patch.object(package, "ROOT", root):
                after = package.archive_files({name: package.build_files(name, "preview")
                                               for name in package.SKILLS})
                self.assertEqual(before, after)
                output = Path(artifacts).resolve()
                result = subprocess.run([sys.executable, "-B", str(root / "scripts/package-skills.py"),
                                         "--output", str(output / "skills"), "--archives", str(output / "release"),
                                         "--channel", "preview", "--apply"],
                                        cwd=output, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(after, {path.name: path.read_bytes() for path in (output / "release").iterdir()})
                git("update-index", "--assume-unchanged", "LICENSE")
                (root / "LICENSE").write_bytes(b"hidden edit\n")
                with self.assertRaisesRegex(ValueError, "does not match the recorded commit"):
                    package.build_files("consent-pro", "preview")

    def test_autocrlf_without_lf_attributes_is_rejected_even_when_git_is_clean(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            git, paths = committed_sources(root, attributes=b"# Deliberately missing LF rules\n")
            checkout_with_autocrlf(root, git, paths)
            self.assertIn(b"\r\n", (root / "LICENSE").read_bytes())
            self.assertEqual(git("status", "--porcelain"), "")
            with mock.patch.object(package, "ROOT", root), self.assertRaisesRegex(
                    ValueError, "does not match the recorded commit"):
                package.build_files("consent-pro", "preview")

    def test_distribution_guard_mutations_are_detected(self):
        path = ROOT / "scripts/package-skills.py"
        source = path.read_text(encoding="utf-8")
        controls = (
            ("source allowlist",
             "if not path.is_relative_to(ROOT) or path.relative_to(ROOT).as_posix() not in approved:",
             "if False:", "test_existing_private_file_is_rejected_before_reading"),
            ("changed installed content", "return actual == files", "return True",
             "test_modified_install_is_not_overwritten"),
            ("exact source commit", "if result.returncode or digest(result.stdout) != expected:",
             "if False:", "test_clean_preview_matches_its_commit_and_hidden_edits_are_rejected"),
            ("required local reference",
             'raise ValueError("Required reference is not packaged: " + relative + " in " + str(source))',
             "return match[0]", "test_links_are_closed_to_packaged_dependencies"),
            ("portable metadata path",
             'return (Path(skill_path).parent / "agents/openai.yaml").as_posix()',
             'return str(Path(skill_path).parent / "agents/openai.yaml")',
             "test_interface_metadata_is_posix_with_windows_path_semantics"),
            ("normalized package output", "output = output.resolve()", "output = output.absolute()",
             "test_parent_segments_are_normalized_before_archive_boundary_check"),
            ("normalized archive output", "archives = archives.resolve()", "archives = archives.absolute()",
             "test_parent_segments_are_normalized_before_archive_boundary_check"),
            ("case and filesystem aliases",
             "return len(candidate) >= len(parent) and candidate[:len(parent)] == parent",
             "return archive.is_relative_to(skill)",
             "test_archive_boundary_rejects_case_and_normalization_aliases"),
        )
        for name, before, after, test in controls:
            with self.subTest(control=name):
                self.assertEqual(source.count(before), 1)
                mutant = types.ModuleType("package_guard_mutant")
                mutant.__file__ = str(path)
                exec(compile(source.replace(before, after), str(path), "exec"), mutant.__dict__)
                result = unittest.TestResult()
                with mock.patch.object(sys.modules[__name__], "package", mutant), \
                        contextlib.redirect_stdout(io.StringIO()):
                    SkillPackages(test).run(result)
                self.assertFalse(result.errors, result.errors)
                self.assertTrue(result.failures, "Broken guard was accepted: " + name)


class CatalogueDrift(unittest.TestCase):
    def test_command_distinguishes_equal_changed_and_invalid_contracts(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            before, after = root / "before.json", root / "after.json"
            payload = {"tools": [{"name": "read", "inputSchema": {"type": "object"},
                                  "annotations": {"readOnlyHint": True}}]}
            before.write_text(json.dumps(payload), encoding="utf-8")
            after.write_text(json.dumps(payload), encoding="utf-8")
            argv = ["check-mcp-catalogue.py", str(before), str(after)]
            with mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(io.StringIO()), \
                    contextlib.redirect_stderr(io.StringIO()):
                catalogue.main()
                payload["tools"][0]["annotations"]["readOnlyHint"] = False
                after.write_text(json.dumps(payload), encoding="utf-8")
                with self.assertRaises(SystemExit) as changed:
                    catalogue.main()
                self.assertEqual(changed.exception.code, 1)
                after.write_text('{"tools": []}', encoding="utf-8")
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
            path.write_text(json.dumps({"tools": [tool, tool]}), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate"):
                catalogue.contracts(path)


class RepositoryChecks(unittest.TestCase):
    def test_command_fails_on_broken_local_link(self):
        with tempfile.TemporaryDirectory() as folder, contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            root = Path(folder)
            (root / "README.md").write_text("Valid guide\n", encoding="utf-8")
            with mock.patch.object(sys, "argv", ["check-repository.py", "--root", str(root)]):
                repository.main()
                (root / "README.md").write_text("[Missing](missing.md)\n", encoding="utf-8")
                with self.assertRaises(SystemExit) as broken:
                    repository.main()
                self.assertEqual(broken.exception.code, 1)

    def test_missing_link_and_authored_dash_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "README.md").write_text("[Guide](guide.md)\n", encoding="utf-8")
            self.assertEqual(len(repository.check(root)[1]), 1)
            (root / "guide.md").write_text("Valid guide\n", encoding="utf-8")
            self.assertEqual(repository.check(root), (1, []))
            (root / "guide.md").write_text("Invalid " + chr(0x2014) + " punctuation\n", encoding="utf-8")
            self.assertEqual(len(repository.check(root)[1]), 1)


if __name__ == "__main__":
    unittest.main()
