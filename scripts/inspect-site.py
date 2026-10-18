"""
What it does: reads a site's published HTML and reports what is actually there: whether
          Consent Pro is installed, WHICH ENGINE it uses (which decides your documentation
          trail), the site id, the tag manager container, what loads before the consent layer,
          and whether image trackers have been handled.
READS or WRITES: **READS ONLY, and only public HTML.** No credential, no API, no login. It
          fetches the page the same way any visitor does.
How to apply: nothing is applied. There is no write path and no flag that creates one.
Safe to run again? Always. It is a plain GET.

WHY THIS EXISTS: it replaces a question with a measurement.
   Every guide starts by asking "is your site Webflow or something else?" and people answer
   with what they believe. That belief is wrong often enough to matter: a Webflow project
   managed from the web app follows the web app trail, and answering "Webflow" sends you to
   the wrong region instructions. **The script address on the page settles it**, and the page
   is public.

WHAT IT CANNOT TELL YOU: whether anything is actually blocked. This reads declarations in
   HTML, not behaviour in a browser. A page can declare everything correctly and still fire
   trackers before consent. For that, see docs/reference/verify-behaviour.md, which is the
   check that loads the page and watches.

Usage:
   python inspect-site.py https://example.com
"""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# The two engines, told apart by the PATH and not by the host.
#
# Matching the host was the first version and it was wrong. A site on staging, on a branch
# preview or on a self-hosted CDN serves the same script from somewhere that is not
# consentpro.com, and the check reported "not installed" on a site that plainly had it. The
# path is the stable part: /v2/cdn/runtime is engine 1, /cdn/core/ is engine 2.
ENGINES = [
    ("Webflow app (engine 1)", r"/v2/cdn/runtime", "webflow"),
    ("Web app (engine 2)", r"/cdn/core/[a-f0-9]{16,}\.js", "web-app"),
]

TRAIL = {
    "webflow": "https://docs.consentpro.com/webflow/google-tag-manager",
    "web-app": "https://docs.consentpro.com/web-app/google-tag-manager",
}

class PageElements(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.line_offsets = [0] + [match.end() for match in re.finditer("\n", html)]
        self.scripts = []
        self.resources = []
        self.script_details = {}
        self.images = []
        self.in_head = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == "head":
            self.in_head = True
        attributes = dict(attrs)
        if tag == "img":
            self.images.append(attributes)
        src = attributes.get("src")
        if src:
            line, column = self.getpos()
            resource = (self.line_offsets[line - 1] + column, src)
            self.resources.append(resource)
            if tag == "script":
                self.scripts.append(resource)
                self.script_details[resource[0]] = {
                    "attrs": attributes, "in_head": self.in_head,
                    "duplicates": len(attrs) != len(attributes),
                }

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False


def parse_src(src):
    try:
        return urllib.parse.urlsplit(src)
    except ValueError:
        return None


def find_consent_script(elements):
    for position, src in elements.scripts:
        parsed = parse_src(src)
        if parsed is None:
            continue
        for label, pattern, trail in ENGINES:
            if re.search(pattern, parsed.path):
                return label, trail, position
    return None, None, None


def fetch(url, attempts=3):
    wait = 2
    for n in range(attempts):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.status, r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            return e.code, ""
        except Exception as e:
            if n < attempts - 1:
                import time
                time.sleep(wait); wait *= 2; continue
            raise SystemExit("could not fetch %s: %s" % (url, e))
    raise SystemExit("no answer from " + url)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("url", help="the published page to read, for example https://example.com")
    p.add_argument("--expected-site-id", help="compare the core tag with the confirmed project ID")
    a = p.parse_args()

    url = a.url if a.url.startswith("http") else "https://" + a.url
    status, html = fetch(url)
    print("\n%s  (HTTP %s, %d bytes)\n" % (url, status, len(html)))
    if status != 200 or not html:
        raise SystemExit("The page did not return content, so nothing below can be measured.")

    # --- which engine, which trail -------------------------------------------------
    elements = PageElements(html)
    engine, trail, pos_consent = find_consent_script(elements)

    if engine is None:
        print("CONSENT PRO      not found on this page")
        print("                 Either it is not installed, or it is injected later by")
        print("                 something this cannot see. Check the page source yourself")
        print("                 before concluding it is missing.\n")
    else:
        print("CONSENT PRO      %s" % engine)
        print("YOUR TRAIL       %s" % TRAIL[trail])
        details = elements.script_details[pos_consent]
        attrs = details["attrs"]
        site_id = attrs.get("data-consentpro-site-id")
        if site_id:
            print("SITE ID          %s" % site_id)
        if trail == "web-app":
            missing = [key for key in ("data-consentpro-script", "data-consentpro-site-id")
                       if not attrs.get(key)]
            print("CORE ATTRIBUTES  " + ("missing/empty: " + ", ".join(missing) if missing
                                          else "both required attributes present"))
            if attrs.get("data-consentpro-script") != "runtime":
                print("CORE MARKER      expected data-consentpro-script=runtime; compare the project snippet")
            source_id = re.search(r"/cdn/core/([a-f0-9]{16,})\.js", parse_src(attrs["src"]).path)
            if source_id and site_id != source_id.group(1):
                print("CORE SITE ID     MISMATCH: script URL and data-consentpro-site-id differ")
            if a.expected_site_id and site_id != a.expected_site_id:
                print("PROJECT MATCH    MISMATCH: installed site ID differs from the confirmed project")
            elif a.expected_site_id:
                print("PROJECT MATCH    site ID matches the confirmed project")
            else:
                print("PROJECT MATCH    not checked; use --expected-site-id from the confirmed project")
            print("HEAD PLACEMENT   " + ("inside head" if details["in_head"] else "not inside an explicit head"))
            if details["duplicates"]:
                print("CORE ATTRIBUTES  duplicate attributes found; compare the exact project snippet")
        runtime_count = sum(any(re.search(pattern, parsed.path) for _, pattern, _ in ENGINES)
                            for _, src in elements.scripts if (parsed := parse_src(src)) is not None)
        if runtime_count > 1:
            print("RUNTIME COUNT    %d runtime declarations; investigate duplicate installations" % runtime_count)

    # --- tag manager ---------------------------------------------------------------
    containers = sorted(set(re.findall(r"GTM-[A-Z0-9]{6,}", html)))
    noscript = "googletagmanager.com/ns.html" in html
    if containers:
        print("TAG MANAGER      %s" % ", ".join(containers))
        print("                 the <noscript> block is %s"
              % ("STILL PRESENT, and step 1 says remove it" if noscript else "gone, good"))
    else:
        print("TAG MANAGER      no container found on this page")

    # --- what runs before the consent layer ----------------------------------------
    print()
    if pos_consent is None:
        print("LOAD ORDER       cannot be checked without the consent layer on the page")
    else:
        before = []
        invalid_before = 0
        for position, src in elements.resources:
            if position < pos_consent:
                parsed = parse_src(src)
                if parsed is None:
                    invalid_before += 1
                    continue
                host = parsed.hostname
                if host and parsed.scheme in ("", "http", "https"):
                    before.append(host)
        if before:
            print("LOAD ORDER       %d external resource declaration(s) appear BEFORE the consent script:" % len(before))
            for h in before:
                print("                 %s" % h)
            print("                 Review these earlier declarations when checking consent initialization.")
            print("                 HTML order alone does not prove request or execution order.")
        elif not invalid_before:
            print("LOAD ORDER       no earlier external src declarations found")
        if invalid_before:
            print("LOAD ORDER       %d resource(s) before consent have invalid URLs; hosts could not be classified."
                  % invalid_before)

    # --- image trackers -------------------------------------------------------------
    gated = sum(bool(img.get("fs-consent-src")) for img in elements.images)
    pixels = sum(bool(re.search(r"(?:pixel|collect|track|tr\?|\.gif\?)", img.get("src") or "", re.I))
                 for img in elements.images)
    invalid_gated = sum(bool(img.get("fs-consent-src"))
                        and (bool(img.get("src")) or not img.get("fs-consent-categories"))
                        for img in elements.images)
    print()
    print("IMAGE TRACKERS   %d gated with fs-consent-src, %d ungated candidate(s) seen"
          % (gated, pixels))
    if invalid_gated:
        print("IMAGE ATTRIBUTES %d gated image(s) retain src or lack fs-consent-categories" % invalid_gated)
    if pixels and not gated:
        print("                 Image requests cannot be blocked by the script alone: the src")
        print("                 has to leave the HTML. See docs/05-what-gtm-does-not-cover.md")

    # --- what to do next -------------------------------------------------------------
    print()
    print("NEXT             This read declarations, not behaviour. A page can look correct")
    print("                 here and still fire trackers before consent.")
    reference_dir = "docs/reference" if (Path(__file__).resolve().parent.parent / "docs/reference").is_dir() else "reference"
    print("                 Run the behaviour check: " + reference_dir + "/verify-behaviour.md")
    if containers:
        print("                 And audit the container: scripts/audit-container.py")
    print()


if __name__ == "__main__":
    sys.exit(main())
