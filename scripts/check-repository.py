"""Validate local Markdown links and the authored-text punctuation rule.

READS repository files only; WRITES nothing and makes no network requests.
No apply flag. Safe to repeat; missing local link targets or long dashes fail.
Raw source collections and private evidence must remain outside this repository.
"""

import argparse
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"!?\[[^\]]*\]\(([^\s)]+)\)")


def check(root):
    errors, count = [], 0
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part.startswith(".") or part in ("dist", "__pycache__", "venv") for part in relative.parts):
            continue
        if path.is_file() and ("private-evidence" in relative.parts or
                               "customer-data" in relative.parts or
                               relative.parts[:3] == ("docs", "06-agent-readiness", "sources")):
            errors.append(str(relative) + ": private source evidence belongs outside the repository")
            continue
        if path.suffix not in (".md", ".py", ".yaml", ".yml") or not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        if any(character in content for character in (chr(0x2013), chr(0x2014))):
            errors.append(str(relative) + ": long dash in authored text")
        if path.suffix != ".md":
            continue
        for match in LINK.finditer(content):
            target = urlsplit(match[1])
            if target.scheme or target.netloc or not target.path:
                continue
            count += 1
            resolved = (path.parent / unquote(target.path)).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                errors.append(str(relative) + ": missing or escaping link " + match[1])
    return count, errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    count, errors = check(args.root)
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    print("Validated %d local Markdown links and authored-text punctuation." % count)


if __name__ == "__main__":
    main()
