#!/usr/bin/env python3
"""Archive images and the template referenced by the public Consent Pro scrape.

READS only HTTPS URLs on docs.consentpro.com, rejects redirects and sends no
credentials. WRITES only public assets and their local integrity index.
Dry run by default; --collect applies local downloads. Does not change the site.
Safe to repeat: reuses files with verified size/hash and refuses to replace
mismatched or unindexed files. To undo, remove this collection's assets/ and
assets-index.json, preserving the source JSON files.
"""
import argparse
import datetime
import hashlib
import http.client
import json
import os
import pathlib
import re
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request


HOST = "docs.consentpro.com"
MAX_URLS = 80
MAX_ASSET_BYTES = 10 * 1024 * 1024
MAX_TOTAL_BYTES = 120 * 1024 * 1024
TIMEOUT_SECONDS = 30
MAX_RETRIES = 1
IMAGE_LINE = re.compile(r"!\[.*\]\((https://docs\.consentpro\.com/[^\s]+)\)")
SOURCE_FILES = ("web-app.json", "references.json")


def timestamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def checked_url(url):
    parsed = urllib.parse.urlsplit(url)
    if (parsed.scheme != "https" or parsed.hostname != HOST
            or parsed.username or parsed.password or parsed.port not in (None, 443)):
        raise ValueError("URL outside the only permitted HTTPS host")
    return urllib.parse.urlunsplit(parsed._replace(fragment=""))


class RejectRedirects(urllib.request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        fp.close()
        raise ValueError("Redirect rejected without reading the response body")

    http_error_301 = http_error_303 = http_error_307 = http_error_308 = http_error_302


def discover(source_dir):
    urls = {}
    sources = []
    page_count = 0
    for name in SOURCE_FILES:
        raw = (source_dir / name).read_bytes()
        document = json.loads(raw)
        sources.append({"path": name, "bytes": len(raw), "sha256": digest(raw)})
        pages = document["pages"]
        page_count += len(pages)
        for page in pages:
            for line in page.get("markdown", "").splitlines():
                match = IMAGE_LINE.fullmatch(line)
                if match:
                    urls[checked_url(match.group(1))] = "image"
            for url in page.get("links", []):
                if urllib.parse.urlsplit(url).path.endswith(".tpl"):
                    urls[checked_url(url)] = "template"
    if len(urls) > MAX_URLS:
        raise ValueError("Collection exceeds the URL limit")
    return urls, sources, page_count


def local_path(url):
    basename = pathlib.PurePosixPath(urllib.parse.unquote(urllib.parse.urlsplit(url).path)).name
    basename = re.sub(r"[^a-z0-9._-]+", "-", basename.lower()).strip("-.")[:100]
    if not basename:
        raise ValueError("Asset has no filename")
    return "assets/" + digest(url.encode())[:20] + "-" + basename


def checked_response_headers(headers):
    lengths = headers.get_all("Content-Length", [])
    encodings = headers.get_all("Transfer-Encoding", [])
    if len(lengths) > 1:
        raise ValueError("Multiple Content-Length headers rejected")
    if len(encodings) > 1:
        raise ValueError("Multiple Transfer-Encoding headers rejected")
    if lengths and encodings:
        raise ValueError("Transfer-Encoding combined with Content-Length rejected")
    if encodings and encodings[0] != "chunked":
        raise ValueError("Transfer-Encoding must be exactly chunked")
    if lengths:
        if not re.fullmatch(r"[0-9]+", lengths[0]):
            raise ValueError("Invalid Content-Length rejected")
        return int(lengths[0])
    return None


def remaining_budget(budget):
    remaining = MAX_TOTAL_BYTES - budget["network_bytes"]
    if remaining <= 0:
        raise ValueError("Transfer reached the total byte limit")
    return remaining


def incomplete_read_bytes(error):
    pending = [error]
    visited = set()
    total = 0
    while pending:
        current = pending.pop()
        if id(current) in visited:
            continue
        visited.add(id(current))
        if isinstance(current, http.client.IncompleteRead):
            total += len(current.partial)
        pending.extend(item for item in (current.__cause__, current.__context__) if item is not None)
    return total


def fetch(opener, url, budget):
    for attempt in range(MAX_RETRIES + 1):
        remaining_budget(budget)
        try:
            request = urllib.request.Request(checked_url(url), headers={
                "User-Agent": "consentpro-gtm-ai-public-docs-archive/1.0",
                "Accept-Encoding": "identity",
            })
            with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
                final_url = checked_url(response.url)
                declared_length = checked_response_headers(response.headers)
                if declared_length is not None and declared_length > MAX_ASSET_BYTES:
                    raise ValueError("Asset exceeds the per-file byte limit")
                if declared_length is not None and declared_length > remaining_budget(budget):
                    raise ValueError("Content-Length exceeds the remaining transfer budget")
                content = bytearray()
                while True:
                    if declared_length is not None and len(content) == declared_length:
                        break
                    allowance = min(65536, MAX_ASSET_BYTES - len(content), remaining_budget(budget))
                    if allowance <= 0:
                        raise ValueError("Asset reached the byte limit before its end was verified")
                    try:
                        chunk = response.read(allowance)
                    except http.client.IncompleteRead as error:
                        budget["network_bytes"] += incomplete_read_bytes(error)
                        raise
                    if not chunk:
                        break
                    content.extend(chunk)
                    budget["network_bytes"] += len(chunk)
                    if len(content) > MAX_ASSET_BYTES:
                        raise ValueError("Asset exceeds the per-file byte limit")
                    if budget["network_bytes"] > MAX_TOTAL_BYTES:
                        raise ValueError("Transfer exceeds the total byte limit")
                if declared_length is not None and len(content) != declared_length:
                    raise ValueError("Incomplete response according to Content-Length")
                if not content:
                    raise ValueError("Empty asset")
                return bytes(content), response.headers.get_content_type(), final_url
        except urllib.error.HTTPError as error:
            if attempt == MAX_RETRIES or error.code not in (408, 429, 500, 502, 503, 504):
                raise
        except (urllib.error.URLError, TimeoutError, http.client.HTTPException):
            if attempt == MAX_RETRIES or budget["network_bytes"] >= MAX_TOTAL_BYTES:
                raise
        remaining_budget(budget)
        time.sleep(1)
    raise RuntimeError("Retry limit reached")


def collect(source_dir, urls, sources, page_count):
    index_path = source_dir / "assets-index.json"
    previous = json.loads(index_path.read_text()) if index_path.exists() else {}
    prior_assets = {item["url"]: item for item in previous.get("assets", [])}
    opener = urllib.request.build_opener(RejectRedirects())
    results = {url: {**item, "status": "not_checked", "last_action": "preserved"}
               for url, item in prior_assets.items()}
    errors = []
    budget = {"network_bytes": 0, "archive_bytes": 0}
    counts = {"downloaded": 0, "reused": 0}
    (source_dir / "assets").mkdir(exist_ok=True)

    def persist():
        report = {"schema_version": 1, "last_run_at": timestamp(),
                  "mode": "public external reads and local archive writes only",
                  "discovered_count": len(urls),
                  "page_count": page_count, "source_files": sources,
                  "limits": {"urls": MAX_URLS, "bytes_per_asset": MAX_ASSET_BYTES,
                             "total_bytes": MAX_TOTAL_BYTES, "timeout_seconds": TIMEOUT_SECONDS,
                             "max_retries": MAX_RETRIES, "allowed_host": HOST,
                             "redirects": "rejected_without_reading_body"},
                  "summary": {"discovered": len(urls),
                              "successful": sum(item["status"] == "ok" for item in results.values()),
                              "preserved_unverified": sum(item["status"] != "ok" for item in results.values()),
                              **counts, "errors": len(errors), **budget},
                  "assets": list(results.values()), "failures": errors}
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", dir=source_dir,
                                             prefix=".assets-index-", suffix=".tmp", delete=False) as handle:
                temporary = pathlib.Path(handle.name)
                json.dump(report, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
            os.replace(temporary, index_path)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
        return report

    for position, (url, kind) in enumerate(sorted(urls.items())):
        relative = local_path(url)
        destination = source_dir / relative
        prior = prior_assets.get(url)
        try:
            if destination.exists():
                if not prior or prior.get("path") != relative:
                    raise ValueError("Existing file has no matching index entry; preserved")
                if destination.stat().st_size > MAX_ASSET_BYTES:
                    raise ValueError("Existing file exceeds the byte limit; preserved")
                content = destination.read_bytes()
                if len(content) != prior.get("bytes") or digest(content) != prior.get("sha256"):
                    raise ValueError("Existing file does not match the index; preserved")
                item = {key: value for key, value in prior.items() if key != "last_action"}
                action = "reused"
            else:
                content, content_type, final_url = fetch(opener, url, budget)
                if budget["archive_bytes"] + len(content) > MAX_TOTAL_BYTES:
                    raise ValueError("Local archive would exceed the total byte limit")
                with destination.open("xb") as handle:
                    handle.write(content)
                item = {"url": url, "path": relative, "kind": kind,
                        "bytes": len(content), "sha256": digest(content),
                        "content_type": content_type, "final_url": final_url,
                        "collected_at": timestamp()}
                action = "downloaded"
            budget["archive_bytes"] += len(content)
            if budget["archive_bytes"] > MAX_TOTAL_BYTES:
                raise ValueError("Local archive exceeds the total byte limit")
            item["last_action"] = action
            item["status"] = "ok"
            results[url] = item
            counts[action] += 1
        except (OSError, ValueError, urllib.error.URLError, http.client.HTTPException) as error:
            errors.append({"url": url, "path": relative,
                           "error": str(error), "type": type(error).__name__})
            if prior:
                results[url] = {**prior, "status": "verification_failed", "last_action": "preserved"}
        if budget["network_bytes"] >= MAX_TOTAL_BYTES and position + 1 < len(urls):
            errors.append({"error": "Collection stopped at the transfer byte limit"})
            persist()
            break
        persist()
    report = persist()
    print(json.dumps({"index": str(index_path), "index_updated": bool(previous),
                      **report["summary"]}, ensure_ascii=False))
    return 1 if errors else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=pathlib.Path,
                        default=pathlib.Path(__file__).resolve().parents[1] / "sources" / "2026-10-16")
    parser.add_argument("--collect", action="store_true",
                        help="Download public assets and write the local index; dry run without this flag.")
    args = parser.parse_args()
    source_dir = args.source_dir.resolve()
    urls, sources, page_count = discover(source_dir)
    if not args.collect:
        print(json.dumps({"mode": "simulation", "pages": page_count, "urls": len(urls),
                          "images": sum(kind == "image" for kind in urls.values()),
                          "templates": sum(kind == "template" for kind in urls.values()),
                          "source_dir": str(source_dir), "network_requests": 0,
                          "files_written": 0}, ensure_ascii=False))
        return 0
    return collect(source_dir, urls, sources, page_count)


if __name__ == "__main__":
    sys.exit(main())
