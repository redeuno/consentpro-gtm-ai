"""
What it does: reads a site's published HTML and reports what is actually there: whether
          Consent Pro is installed, WHICH ENGINE it uses (which decides your documentation
          trail), the site id, the tag manager container, what loads before the consent layer,
          and whether image trackers have been handled.
READS or WRITES: **READS ONLY, and only public HTML.** No credential, no API, no login. It
          fetches the page the same way any visitor does.
How to apply: nothing is applied. There is no write path and no flag that creates one.
Safe to run again? Always. It is a plain GET.

⭐ WHY THIS EXISTS: it replaces a question with a measurement.
   Every guide starts by asking "is your site Webflow or something else?" and people answer
   with what they believe. That belief is wrong often enough to matter: a Webflow project
   managed from the web app follows the web app trail, and answering "Webflow" sends you to
   the wrong region instructions. **The script address on the page settles it**, and the page
   is public.

⚠️ WHAT IT CANNOT TELL YOU: whether anything is actually blocked. This reads declarations in
   HTML, not behaviour in a browser. A page can declare everything correctly and still fire
   trackers before consent. For that, see docs/reference/verify-behaviour.md, which is the
   check that loads the page and watches.

Usage:
   python inspect-site.py https://example.com
"""

import argparse
import re
import sys
import urllib.error
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# The two engines, told apart by the PATH and not by the host.
#
# ⛔ Matching the host was the first version and it was wrong. A site on staging, on a branch
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

# Anything with a host that is not the site itself. Deliberately broad: a font or a widget
# loading before the consent layer matters as much as an obvious tracker.
THIRD_PARTY = re.compile(r"""src=["'](?:https?:)?//([a-z0-9][a-z0-9.-]*\.[a-z]{2,})""", re.I)
CONSENT_HOSTS = re.compile(r"consentpro|consent-pro", re.I)


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
    a = p.parse_args()

    url = a.url if a.url.startswith("http") else "https://" + a.url
    status, html = fetch(url)
    print("\n%s  (HTTP %s, %d bytes)\n" % (url, status, len(html)))
    if status != 200 or not html:
        raise SystemExit("The page did not return content, so nothing below can be measured.")

    # --- which engine, which trail -------------------------------------------------
    engine = trail = None
    pos_consent = None
    for label, pattern, key in ENGINES:
        m = re.search(pattern, html)
        if m:
            engine, trail, pos_consent = label, key, m.start()
            break

    if engine is None:
        print("CONSENT PRO      not found on this page")
        print("                 Either it is not installed, or it is injected later by")
        print("                 something this cannot see. Check the page source yourself")
        print("                 before concluding it is missing.\n")
    else:
        print("CONSENT PRO      %s" % engine)
        print("YOUR TRAIL       %s" % TRAIL[trail])
        sid = re.search(r"""(?:site-?id|siteid)=["']([a-f0-9]{16,})""", html, re.I)
        if not sid:
            sid = re.search(r"/cdn/core/([a-f0-9]{16,})\.js", html)
        if sid:
            print("SITE ID          %s" % sid.group(1))

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
        for m in THIRD_PARTY.finditer(html):
            if m.start() < pos_consent:
                host = m.group(1)
                if CONSENT_HOSTS.search(host):
                    continue
                if host not in before:
                    before.append(host)
        if before:
            print("⛔ LOAD ORDER    %d third-party request(s) load BEFORE the consent layer:" % len(before))
            for h in before:
                print("                 %s" % h)
            print("                 The consent script must be the first thing in <head>.")
            print("                 Anything above it runs before consent is known, and that")
            print("                 includes fonts and widgets, not only obvious trackers.")
        else:
            print("✅ LOAD ORDER    nothing third-party loads before the consent layer")

    # --- image trackers -------------------------------------------------------------
    gated = len(re.findall(r"fs-consent-src=", html))
    pixels = len(re.findall(r"""<img[^>]+src=["'](?:https?:)?//(?!cdn\.)[^"']*(?:pixel|collect|track|tr\?|\.gif\?)""", html, re.I))
    print()
    print("IMAGE TRACKERS   %d gated with fs-consent-src, %d ungated candidate(s) seen"
          % (gated, pixels))
    if pixels and not gated:
        print("                 Image requests cannot be blocked by the script alone: the src")
        print("                 has to leave the HTML. See docs/05-what-gtm-does-not-cover.md")

    # --- what to do next -------------------------------------------------------------
    print()
    print("NEXT             This read declarations, not behaviour. A page can look correct")
    print("                 here and still fire trackers before consent.")
    print("                 Run the behaviour check: docs/reference/verify-behaviour.md")
    if containers:
        print("                 And audit the container: scripts/audit-container.py")
    print()


if __name__ == "__main__":
    sys.exit(main())
