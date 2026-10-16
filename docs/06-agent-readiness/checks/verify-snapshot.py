#!/usr/bin/env python3
"""Verify the local archive and negative completeness controls.

READS only local files. Does not access the network or write files.
Usage: python3 -B verify-snapshot.py [--self-check]. There is no apply mode.
Safe to repeat; changes no state and requires no rollback.
"""
import argparse
import copy
import datetime
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1] / "sources" / "2026-10-16"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(url):
    parsed = urlsplit(url)
    return parsed.scheme + "://" + parsed.netloc + parsed.path.rstrip("/")


def check_pages(pages, expected):
    urls = [canonical(p["metadata"]["sourceURL"]) for p in pages]
    require(len(urls) == len(set(urls)), "Duplicate pages")
    require(set(urls) == expected, "Page inventory does not match the expected URLs")
    for page in pages:
        require(page["metadata"].get("statusCode") == 200, "Page did not report HTTP success")
        require(len(page.get("markdown", "")) > 100, "Page has insufficient extracted text")


def check_file(record):
    path = (ROOT / record["path"]).resolve()
    require(path.is_relative_to(ROOT.resolve()), "File is outside the archive")
    data = path.read_bytes()
    require(len(data) == record["bytes"], "Size mismatch: " + record["path"])
    require(hashlib.sha256(data).hexdigest() == record["sha256"],
            "Hash mismatch: " + record["path"])
    if record.get("kind") == "image":
        require(data.startswith(b"\x89PNG\r\n\x1a\n"), "Image does not have a PNG signature")


def rejected(callback):
    try:
        callback()
    except ValueError:
        return True
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-check", action="store_true")
    args = parser.parse_args()
    web = json.loads((ROOT / "web-app.json").read_text())["pages"]
    refs = json.loads((ROOT / "references.json").read_text())["pages"]
    sitemap = ET.fromstring((ROOT / "sitemap.xml").read_bytes())
    expected = {canonical(node.text) for node in sitemap.findall("{*}url/{*}loc")
                if node.text.startswith("https://docs.consentpro.com/web-app/")}
    check_pages(web, expected)
    ref_urls = {canonical(url) for page in web for url in page.get("links", [])
                if url.startswith("https://docs.consentpro.com/runtime/")
                or canonical(url) == "https://docs.consentpro.com/scanner"}
    check_pages(refs, ref_urls)
    internal = {canonical(url) for page in web for url in page.get("links", [])
                if url.startswith("https://docs.consentpro.com/web-app/")
                and not Path(urlsplit(url).path).suffix}
    require(internal <= expected, "Internal link has no collected page")
    assets = json.loads((ROOT / "assets-index.json").read_text())
    require(not assets["failures"], "Asset collection has failures")
    records = assets["assets"]
    images = {url for page in web + refs for url in re.findall(
        r"^!\[[^\n]*\]\((https://docs\.consentpro\.com/[^\n]*)\)$",
        page["markdown"], re.M)}
    templates = {url for page in web + refs for url in page.get("links", [])
                 if urlsplit(url).path.endswith(".tpl")}
    require({r["url"] for r in records} == images | templates,
            "Collected assets do not match their references")
    require(len(records) == len(images | templates), "Duplicate assets")
    for record in records + assets["source_files"]:
        check_file(record)
    catalogue = json.loads((ROOT / "mcp-catalogue.json").read_text())
    tools = catalogue["tools"]
    result = {"verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "web_app_expected": len(expected), "web_app_collected": len(web),
              "references_collected": len(refs), "images": len(images),
              "templates": len(templates), "assets_verified": len(records),
              "asset_bytes": sum(r["bytes"] for r in records),
              "mcp_tools": len(tools),
              "mcp_read_only": sum(t["annotations"]["readOnlyHint"] is True for t in tools),
              "mcp_write": sum(t["annotations"]["readOnlyHint"] is False for t in tools),
              "files": []}
    for name in ("web-app.json", "references.json", "map.json", "sitemap.xml",
                 "assets-index.json", "mcp-catalogue.json"):
        data = (ROOT / name).read_bytes()
        result["files"].append({"path": name, "bytes": len(data),
                                "sha256": hashlib.sha256(data).hexdigest()})
    if args.self_check:
        broken_pages = copy.deepcopy(web)
        broken_pages[0]["metadata"]["statusCode"] = 500
        broken_hash = dict(records[0], sha256="0" * 64)
        controls = {
            "missing_page_rejected": rejected(lambda: check_pages(web[1:], expected)),
            "missing_reference_rejected": rejected(lambda: check_pages(refs[1:], ref_urls)),
            "failed_page_rejected": rejected(lambda: check_pages(broken_pages, expected)),
            "changed_asset_rejected": rejected(lambda: check_file(broken_hash)),
        }
        require(all(controls.values()), "A negative control was incorrectly accepted")
        result["negative_controls"] = controls
    result["status"] = "verified"
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
