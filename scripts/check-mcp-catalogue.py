"""Compare two saved MCP tool contracts without calling a server.

READS local catalogue JSON; WRITES nothing. No apply flag or network access.
Repeat safely: exit 0 means equal contracts, 1 means drift, 2 means invalid input.
Usage: python3 scripts/check-mcp-catalogue.py baseline.json candidate.json
Changed tools require review; this command never enables a new capability.
"""

import argparse
import json
from pathlib import Path


def contracts(path):
    if path.stat().st_size > 10 * 1024 * 1024:
        raise ValueError("Catalogue exceeds 10 MiB")
    payload = json.loads(path.read_text())
    entries = payload.get("tools")
    if not isinstance(entries, list) or not entries:
        raise ValueError("Expected a non-empty tools array")
    result = {}
    for tool in entries:
        name = tool.get("name") if isinstance(tool, dict) else None
        if not isinstance(name, str) or not name or name in result:
            raise ValueError("Missing or duplicate tool name")
        if not isinstance(tool.get("inputSchema"), dict):
            raise ValueError("Missing inputSchema for " + name)
        result[name] = {key: tool.get(key) for key in
                        ("description", "inputSchema", "outputSchema", "annotations")}
    return result


def compare(before, after):
    return {
        "added": sorted(after.keys() - before.keys()),
        "removed": sorted(before.keys() - after.keys()),
        "changed": sorted(name for name in before.keys() & after.keys()
                          if before[name] != after[name]),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    try:
        changes = compare(contracts(args.baseline), contracts(args.candidate))
    except (OSError, ValueError) as error:
        parser.exit(2, str(error) + "\n")
    print(json.dumps(changes, indent=2))
    if any(changes.values()):
        parser.exit(1, "Contract drift detected. Review before changing supported capabilities.\n")


if __name__ == "__main__":
    main()
