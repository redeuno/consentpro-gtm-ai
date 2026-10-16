"""Build self-contained Consent Pro skill folders for local agent clients.

READS local repository files only; WRITES packages only with --apply.
Apply: python3 scripts/package-skills.py --output /chosen/skills --apply
Repeating identical output is safe. Different existing packages are refused;
build into a fresh directory and review before replacing an installation.
No network, credentials, client configuration or customer data are accessed.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SKILLS = {
    "consent-pro": "skills/consent-pro/SKILL.md",
    "consent-pro-gtm": "skill/SKILL.md",
}
RUNTIME_SCRIPTS = (
    "inspect-site.py", "authorise.py", "audit-container.py",
    "wire-consent.py", "consent-template.py",
)
LINK = re.compile(r"(!?\[[^\]]*\]\()([^\s)]+)(\))")
REPOSITORY = "https://github.com/redeuno/consentpro-gtm-ai/blob/main/"


def source_map(name):
    sources = {ROOT / path: Path("SKILL.md") if key == name
               else Path("references") / (key + ".md")
               for key, path in SKILLS.items()}
    for path in [*ROOT.glob("docs/[0-5][0-9]-*.md"),
                 *ROOT.glob("docs/reference/*.md"),
                 ROOT / "docs/06-agent-readiness/operations.md",
                 ROOT / "docs/07-agent-installation/README.md",
                 ROOT / "SECURITY.md", ROOT / "LICENSE"]:
        sources[path] = path.relative_to(ROOT)
    for script in RUNTIME_SCRIPTS:
        sources[ROOT / "scripts" / script] = Path("scripts") / script
    ui = ROOT / SKILLS[name]
    sources[ui.parent / "agents/openai.yaml"] = Path("agents/openai.yaml")
    return sources


def rewrite_links(content, source, destination, sources):
    def replace(match):
        target = urlsplit(match[2])
        if target.scheme or target.netloc or not target.path:
            return match[0]
        resolved = (source.parent / unquote(target.path)).resolve()
        if not resolved.is_relative_to(ROOT):
            raise ValueError("Source link escapes repository: " + str(source))
        if resolved in sources:
            link = Path(os.path.relpath(sources[resolved], destination.parent)).as_posix()
        else:
            link = REPOSITORY + resolved.relative_to(ROOT).as_posix()
        if target.fragment:
            link += "#" + target.fragment
        return match[1] + link + match[3]
    return LINK.sub(replace, content)


def build_files(name):
    sources = source_map(name)
    files = {}
    for source, destination in sources.items():
        if source.is_symlink() or not source.is_file():
            raise ValueError("Missing or symbolic source: " + str(source))
        data = source.read_bytes()
        if source.suffix == ".md":
            data = rewrite_links(data.decode(), source, destination, sources).encode()
        files[destination.as_posix()] = data
    manifest = {"format": 1, "name": name,
                "files": {path: hashlib.sha256(data).hexdigest()
                          for path, data in sorted(files.items())}}
    files["package-manifest.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
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


def install(output, apply=False):
    bundles = {name: build_files(name) for name in SKILLS}
    for name, files in bundles.items():
        target = output / name
        if (target.exists() or target.is_symlink()) and not existing_matches(target, files):
            raise ValueError("Refusing to replace differing package: " + str(target)
                             + ". Choose a fresh output directory and review the differences.")
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/skills")
    parser.add_argument("--apply", action="store_true", help="write local packages")
    args = parser.parse_args()
    try:
        install(args.output.expanduser().absolute(), args.apply)
    except (ValueError, OSError) as error:
        parser.exit(1, str(error) + "\n")


if __name__ == "__main__":
    main()
