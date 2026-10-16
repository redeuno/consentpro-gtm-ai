"""Build versioned, self-contained Consent Pro skill folders and ZIP archives.

READS local repository files and Git metadata; no network or account access.
WRITES only local output with --apply. Add --archives DIR to create ZIPs and
SHA256SUMS there. Example: --output dist/skills --archives dist --apply
Identical output is unchanged; differing output is refused. Use a fresh directory
for upgrades and remove only the generated output to undo this operation.
Development builds identify dirty or unversioned source. Preview and stable
builds require a clean Git checkout; a build does not establish client acceptance.
"""

import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from urllib.parse import unquote, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parent.parent
SKILLS = {
    "consent-pro": "skills/consent-pro/SKILL.md",
    "consent-pro-gtm": "skill/SKILL.md",
}
RUNTIME_SCRIPTS = (
    "inspect-site.py", "authorise.py", "audit-container.py",
    "wire-consent.py", "consent-template.py",
)
GUIDES = (
    "docs/00-the-journey.md", "docs/01-google-cloud-setup.md",
    "docs/02-tag-manager-account.md", "docs/03-authorise.md",
    "docs/04-run-it.md", "docs/05-what-gtm-does-not-cover.md",
    "docs/reference/categories.md", "docs/reference/onboarding.md",
    "docs/reference/regions.md", "docs/reference/verify-behaviour.md",
    "docs/reference/verify.md", "docs/reference/consent-mode.md",
    "docs/reference/troubleshooting.md", "docs/reference/nine-steps.md",
    "docs/06-agent-readiness/operations.md", "docs/07-agent-installation/README.md",
    "SECURITY.md", "LICENSE",
)
BUILD_INPUTS = (".gitattributes", "package-release.json", "scripts/package-skills.py")


def interface_metadata(skill_path):
    return (Path(skill_path).parent / "agents/openai.yaml").as_posix()


APPROVED_SOURCES = frozenset((*SKILLS.values(), *GUIDES,
    *("scripts/" + name for name in RUNTIME_SCRIPTS),
    *(interface_metadata(path) for path in SKILLS.values())))
INFORMATIONAL_REFERENCES = frozenset((
    "docs/06-agent-readiness/README.md", "tests/README.md", "scripts/README.md",
))
LINK = re.compile(r"(!?\[[^\]]*\]\()([^\s)]+)(\))")
CHANNELS = ("development", "preview", "stable")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def safe_relative(value):
    path = PurePosixPath(value)
    if (not value or "\\" in value or "\x00" in value or path.is_absolute()
            or any(part in (".", "..") or part.startswith(".") for part in value.split("/"))):
        raise ValueError("Unsafe package path: " + value)
    return path


def no_symlinks(path, stop=None):
    for item in (path, *path.parents):
        if item == stop:
            break
        if (sys.platform == "darwin" and item in (Path("/var"), Path("/tmp"))
                and item.resolve() == Path("/private") / item.name):
            continue
        if item.is_symlink():
            raise ValueError("Refusing symbolic path: " + str(item))


def archive_within_skill(archive, skill):
    def components(path):
        return tuple(unicodedata.normalize("NFD", part).casefold().rstrip(" .") for part in path.parts)
    candidate, parent = components(archive), components(skill)
    return len(candidate) >= len(parent) and candidate[:len(parent)] == parent


def source_map(name):
    if name not in SKILLS:
        raise ValueError("Unknown skill: " + name)
    sources = {ROOT / path: Path("SKILL.md") if key == name
               else Path("references") / (key + ".md")
               for key, path in SKILLS.items()}
    for path in GUIDES:
        sources[ROOT / path] = Path(path)
    for script in RUNTIME_SCRIPTS:
        sources[ROOT / "scripts" / script] = Path("scripts") / script
    sources[ROOT / interface_metadata(SKILLS[name])] = Path("agents/openai.yaml")
    return sources


def read_source(path, approved):
    if not path.is_relative_to(ROOT) or path.relative_to(ROOT).as_posix() not in approved:
        raise ValueError("Source is not approved for distribution: " + str(path))
    no_symlinks(path, ROOT)
    if not path.is_file():
        raise ValueError("Missing source: " + str(path))
    return path.read_bytes()


def release_config():
    data = json.loads(read_source(ROOT / "package-release.json", {"package-release.json"}))
    if (set(data) != {"version", "release_channel"}
            or not isinstance(data["version"], str)
            or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", data["version"])
            or data["release_channel"] not in ("preview", "stable")):
        raise ValueError("Invalid package-release.json")
    return data


def git_state():
    def git(*args):
        return subprocess.run(["git", "-C", str(ROOT), *args], check=True,
                              capture_output=True, text=True).stdout.strip()
    try:
        if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
            return {"commit": None, "dirty": True}
        commit = git("rev-parse", "HEAD")
        if not re.fullmatch(r"[0-9a-f]{40,64}", commit):
            raise ValueError("Invalid source commit")
        return {"commit": commit, "dirty": bool(git("status", "--porcelain", "--untracked-files=all"))}
    except (OSError, subprocess.CalledProcessError):
        return {"commit": None, "dirty": True}


def rewrite_links(content, source, destination, sources):
    def replace(match):
        target = urlsplit(match[2])
        decoded = unquote(target.path)
        if target.scheme or target.netloc:
            if (target.scheme != "https" or not target.netloc or "\\" in match[2]
                    or target.username or target.password):
                raise ValueError("Unsupported external reference in " + str(source))
            if (target.hostname in ("github.com", "raw.githubusercontent.com")
                    and decoded.startswith("/redeuno/consentpro-gtm-ai/")
                    and ("/main/" in decoded or "/sources/" in decoded
                         or decoded.endswith("/docs/06-agent-readiness/README.md"))):
                raise ValueError("Mutable or private repository reference in " + str(source))
            return match[0]
        if not target.path:
            return match[0]
        if "\\" in decoded or "\x00" in decoded or target.query:
            raise ValueError("Unsupported local reference in " + str(source))
        resolved = (source.parent / decoded).resolve()
        if not resolved.is_relative_to(ROOT):
            raise ValueError("Source link escapes repository: " + str(source))
        relative = resolved.relative_to(ROOT).as_posix()
        if relative in INFORMATIONAL_REFERENCES:
            if match[1].startswith("!"):
                raise ValueError("An image cannot be an omitted reference")
            return match[1][1:-2] + " (maintainer reference omitted from this package)"
        if resolved not in sources:
            raise ValueError("Required reference is not packaged: " + relative + " in " + str(source))
        link = Path(os.path.relpath(sources[resolved], destination.parent)).as_posix()
        if target.fragment:
            link += "#" + target.fragment
        return match[1] + link + match[3]
    return LINK.sub(replace, content)


def build_files(name, channel="development", state=None):
    if channel not in CHANNELS:
        raise ValueError("Unknown channel: " + str(channel))
    config = release_config()
    if channel != "development" and channel != config["release_channel"]:
        raise ValueError("Release channel must match package-release.json")
    state = git_state() if state is None else dict(state)
    if channel != "development" and (state["dirty"] or not state["commit"]):
        raise ValueError("Preview and stable packages require a clean Git checkout")
    sources = source_map(name)
    files, original = {}, {}
    for source, destination in sources.items():
        relative = safe_relative(destination.as_posix()).as_posix()
        if relative in files or relative == "package-manifest.json":
            raise ValueError("Duplicate or reserved package path: " + relative)
        data = read_source(source, APPROVED_SOURCES)
        original[source.relative_to(ROOT).as_posix()] = digest(data)
        if source.suffix == ".md":
            data = rewrite_links(data.decode(), source, destination, sources).encode()
        files[relative] = data
    for path in BUILD_INPUTS:
        original[path] = digest(read_source(ROOT / path, {path}))
    for path, expected in original.items():
        if digest(read_source(ROOT / path, set(original))) != expected:
            raise ValueError("Source changed during packaging: " + path)
        if channel != "development":
            result = subprocess.run(["git", "-C", str(ROOT), "show", state["commit"] + ":" + path],
                                    capture_output=True, check=False)
            if result.returncode or digest(result.stdout) != expected:
                raise ValueError("Source does not match the recorded commit: " + path)
    state["content_sha256"] = digest(json_bytes(original))
    manifest = {"format": 2, "name": name, "version": config["version"],
                "channel": channel, "source": state,
                "files": {path: digest(data) for path, data in sorted(files.items())}}
    files["package-manifest.json"] = json_bytes(manifest)
    return files


def existing_matches(target, files):
    if target.is_symlink() or not target.is_dir():
        return False
    entries = list(target.rglob("*"))
    if any(path.is_symlink() for path in entries):
        return False
    actual = {path.relative_to(target).as_posix(): path.read_bytes()
              for path in entries if path.is_file()}
    return actual == files


def archive_bytes(name, files):
    if name not in SKILLS:
        raise ValueError("Unknown skill archive: " + name)
    output = io.BytesIO()
    members = set()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for relative, data in sorted(files.items()):
            member = name + "/" + safe_relative(relative).as_posix()
            if member in members:
                raise ValueError("Duplicate archive member: " + member)
            members.add(member)
            entry = zipfile.ZipInfo(member, (1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)
    return output.getvalue()


def archive_files(bundles):
    files = {}
    for name, bundle in bundles.items():
        manifest = json.loads(bundle["package-manifest.json"])
        suffix = "" if manifest["channel"] == "stable" else "-" + manifest["channel"]
        filename = name + "-" + manifest["version"] + suffix + ".zip"
        files[filename] = archive_bytes(name, bundle)
    files["SHA256SUMS"] = "".join(digest(data) + "  " + name + "\n"
                                 for name, data in sorted(files.items())).encode()
    return files


def install(output, apply=False, archives=None, channel="development"):
    output = output.expanduser().absolute()
    no_symlinks(output)
    output = output.resolve()
    state = git_state()
    inputs = APPROVED_SOURCES | set(BUILD_INPUTS)
    before = {path: digest(read_source(ROOT / path, inputs)) for path in inputs}
    bundles = {name: build_files(name, channel, state) for name in SKILLS}
    if state != git_state() or any(digest(read_source(ROOT / path, inputs)) != sha
                                  for path, sha in before.items()):
        raise ValueError("Source changed during packaging; retry after edits finish")
    archives = archives.expanduser().absolute() if archives is not None else None
    if archives is not None:
        no_symlinks(archives)
        archives = archives.resolve()
    packaged = archive_files(bundles) if archives is not None else {}
    for name, files in bundles.items():
        target = output / name
        if (target.exists() or target.is_symlink()) and not existing_matches(target, files):
            raise ValueError("Refusing to replace differing package: " + str(target)
                             + ". Choose a fresh output directory and review the differences.")
    if archives is not None:
        if any(archive_within_skill(archives, output / name) for name in SKILLS):
            raise ValueError("Archive output cannot be inside an installed skill")
        for name, data in packaged.items():
            target = archives / name
            no_symlinks(target)
            if target.exists() and (not target.is_file() or target.read_bytes() != data):
                raise ValueError("Refusing to replace differing archive: " + str(target))
    for name, files in bundles.items():
        target = output / name
        if target.exists():
            print("UNCHANGED " + str(target))
            continue
        print(("INSTALL " if apply else "WOULD INSTALL ") + str(target))
        if not apply:
            continue
        output.mkdir(parents=True, exist_ok=True)
        stage = Path(tempfile.mkdtemp(prefix=".consent-pro-stage-", dir=output))
        try:
            for relative, data in files.items():
                path = stage / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            if target.exists() or target.is_symlink():
                raise ValueError("Destination appeared during installation: " + str(target))
            stage.rename(target)
        finally:
            if stage.exists():
                shutil.rmtree(stage)
    for name, data in packaged.items():
        target = archives / name
        if target.exists():
            print("UNCHANGED " + str(target))
            continue
        print(("ARCHIVE " if apply else "WOULD ARCHIVE ") + str(target))
        if apply:
            archives.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as stream:
                stream.write(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/skills")
    parser.add_argument("--archives", type=Path, help="also create versioned ZIPs and SHA256SUMS here")
    parser.add_argument("--channel", choices=CHANNELS, default="development")
    parser.add_argument("--apply", action="store_true", help="write local packages and requested archives")
    args = parser.parse_args()
    try:
        install(args.output, args.apply, args.archives, args.channel)
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + "\n")


if __name__ == "__main__":
    main()
