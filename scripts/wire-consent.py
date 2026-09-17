"""
What it does: performs steps 2 through 8 of the official Consent Pro tag manager guide on a
          container: imports the template, creates the initialization tag with the regional
          defaults, creates the consent-updated trigger, moves the tags onto it, applies each
          tag's consent check from a category map you supply, creates a version and publishes.
READS or WRITES: ⛔ **WRITES to Google Tag Manager**, which is a live external system.
How to apply: --apply. Without it, prints every call it would make and touches nothing.
          Publishing needs a SECOND flag, --publish, because publishing is what reaches the
          site and saving is not.
Safe to run again? Yes for the objects, no for the history. Template, trigger and the
          initialization tag are matched by name and updated rather than duplicated, and the
          tag edits write final state. What accumulates is one container VERSION per run,
          which is harmless and visible in the history.

⛔ THE THREE GUARDS, AND WHY EACH ONE EXISTS
   1. ACCOUNT BY ID, CONFIRMED BY NAME. A Google credential reaches every container that
      account can see. An id is easy to mistype and impossible to sanity check by eye, so the
      script prints the live account name and refuses to continue until you pass it back.
      A name check alone would be worse: names are mutable, and a deny list defaults to
      permitting, which is the wrong default for a token that reaches production.
   2. PUBLISHING IS A SEPARATE CONFIRMATION. --apply configures. --publish ships. Bundling
      them means one typo reaches a live site.
   3. THE RESULT IS READ BACK. After writing, run audit-container.py and compare. The
      response to a write tells you the call was accepted, not that the state is what you
      intended, and those are different claims.

⚠️ WHAT THIS SCRIPT WILL NOT DECIDE FOR YOU: which trackers are essential. Essential is the
   only category that skips consent entirely, so it is the one field where a wrong automatic
   answer causes real harm and no check catches it. Build the map with --scaffold, read it,
   and change what is wrong before applying.

Typical run:
   python wire-consent.py --account 123 --container GTM-XXX --scaffold > map.json
   # edit map.json, read the essential lines carefully
   python wire-consent.py --account 123 --container GTM-XXX --confirm-name "..." \
       --banner opt-in --regions Global --map map.json
   # review the simulation, then add --apply, then --apply --publish
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API = "https://tagmanager.googleapis.com/tagmanager/v2"
TOKEN_URL = "https://oauth2.googleapis.com/token"
TEMPLATE_URL = "https://docs.consentpro.com/gtm/templates/Consent%20Pro%20-%20GTM%20Template.tpl"

CLIENT_FILE = os.environ.get("GTM_OAUTH_CLIENT")
TOKEN_FILE = os.environ.get("GTM_OAUTH_TOKEN")

TRIGGER_CONSENT_INIT = "2147479573"

TEMPLATE_NAME = "Consent Pro - GTM Template"
INIT_TAG_NAME = "Consent Pro Init"
TRIGGER_NAME = "Consent Updated"

# Category to Google Consent Mode checks. Essential is deliberately empty: that is what
# "runs without asking" means, and it is why the essential lines in the map deserve a read.
CHECKS = {
    "marketing": ["ad_storage", "ad_user_data", "ad_personalization"],
    "analytics": ["analytics_storage"],
    "personalization": ["personalization_storage"],
    "essential": [],
    "skip": None,  # leave this tag alone entirely
}

FIELDS = ["analyticsStorage", "adStorage", "functionalityStorage",
          "personalizationStorage", "adUserData", "adPersonalization"]


def access_token():
    if not CLIENT_FILE or not TOKEN_FILE:
        raise SystemExit("Set GTM_OAUTH_CLIENT and GTM_OAUTH_TOKEN. See authorise.py.")
    with open(CLIENT_FILE, encoding="utf-8") as f:
        data = json.load(f)
    cli = data.get("installed") or data.get("web")
    with open(os.path.expanduser(TOKEN_FILE), encoding="utf-8") as f:
        refresh = f.read().strip()
    body = urllib.parse.urlencode({
        "client_id": cli["client_id"], "client_secret": cli["client_secret"],
        "refresh_token": refresh, "grant_type": "refresh_token"}).encode()
    try:
        with urllib.request.urlopen(urllib.request.Request(TOKEN_URL, data=body), timeout=40) as r:
            return json.load(r)["access_token"]
    except urllib.error.HTTPError as e:
        raise SystemExit(
            "Could not refresh the token (HTTP %s). If this worked before and stopped, the "
            "most likely cause is an External consent screen still in Testing, which expires "
            "refresh tokens after seven days. Run authorise.py again, and see its header for "
            "how to remove the deadline." % e.code)


def call(tok, path, method="GET", body=None, attempts=4):
    """Retry rules differ by method. A write that returns 5xx has an undefined result: the
    server may have created the object and failed to answer, so retrying creates a second one.
    The API has no idempotency key, so writes do not retry. 429 means the call did not run,
    so that one is safe to retry either way."""
    url = path if path.startswith("http") else API + path
    writing = method != "GET"
    wait = 3
    for n in range(attempts):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Authorization", "Bearer " + tok)
        if data:
            req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                txt = r.read().decode("utf-8")
                return json.loads(txt) if txt.strip() else {}
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:500]
            if e.code == 429 and n < attempts - 1:
                time.sleep(wait); wait *= 2; continue
            if e.code in (500, 502, 503) and not writing and n < attempts - 1:
                time.sleep(wait); wait *= 2; continue
            raise SystemExit("HTTP %s on %s %s\n%s" % (e.code, method, path, detail))
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            if not writing and n < attempts - 1:
                time.sleep(wait); wait *= 2; continue
            raise SystemExit("transport failure on %s %s: %s" % (method, path, e))
    raise SystemExit("no answer: " + path)


def consent_settings(category):
    checks = CHECKS.get(category)
    if not checks:
        return {"consentStatus": "notSet"}
    return {"consentStatus": "needed",
            "consentType": {"type": "list",
                            "list": [{"type": "template", "value": c} for c in checks]}}


def fetch_template():
    req = urllib.request.Request(TEMPLATE_URL)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8-sig")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--account", required=True)
    p.add_argument("--container", required=True, help="public id, GTM-XXXXXXX")
    p.add_argument("--confirm-name", default=None, help="the account name, exactly as printed")
    p.add_argument("--workspace", default=None)
    p.add_argument("--banner", choices=["opt-in", "opt-out"], default="opt-in",
                   help="opt-in denies every default; opt-out, do-not-sell and informational grant")
    p.add_argument("--regions", default="Global",
                   help=("region codes EXACTLY as the tag manager expects. 'Global' for the "
                         "default banner, never the screen label 'Global (default)'. Countries "
                         "as GB or FR, subdivisions as US-CA, comma separated. The app's EU "
                         "option is an interface shortcut: list each country instead"))
    p.add_argument("--wait", default="1000", help="wait for consent update, in ms")
    p.add_argument("--map", default=None, help="json mapping tag name to category")
    p.add_argument("--scaffold", action="store_true",
                   help="print a category map skeleton from the container's tags and exit")
    p.add_argument("--apply", action="store_true", help="write for real")
    p.add_argument("--publish", action="store_true", help="publish; requires --apply")
    a = p.parse_args()

    if a.publish and not a.apply:
        raise SystemExit("--publish requires --apply. Publishing is a separate decision.")

    tok = access_token()

    account = call(tok, "/accounts/%s" % a.account)
    live = account.get("name")
    if a.confirm_name is None:
        raise SystemExit(
            "\nAccount %s is named: %s\n\nIf that is the right account, run again adding:\n"
            "  --confirm-name \"%s\"\n\nIf it is not, stop and check the id.\n"
            % (a.account, live, live))
    if a.confirm_name != live:
        raise SystemExit("Account %s is named '%s', not '%s'. Stopping." % (a.account, live, a.confirm_name))

    containers = call(tok, "/accounts/%s/containers" % a.account).get("container", [])
    target = next((c for c in containers if c.get("publicId") == a.container), None)
    if target is None:
        raise SystemExit("container %s not found in account %s" % (a.container, a.account))

    wss = call(tok, "/accounts/%s/containers/%s/workspaces"
               % (a.account, target["containerId"])).get("workspace", [])
    ws = next((w for w in wss if w.get("workspaceId") == a.workspace), None) if a.workspace \
        else (wss[0] if len(wss) == 1 else None)
    if ws is None:
        raise SystemExit("pick a workspace with --workspace: %s"
                         % ", ".join(w.get("workspaceId", "?") for w in wss))

    base = "/accounts/%s/containers/%s/workspaces/%s" % (
        a.account, target["containerId"], ws["workspaceId"])
    tags = call(tok, base + "/tags").get("tag", [])
    triggers = call(tok, base + "/triggers").get("trigger", [])
    templates = call(tok, base + "/templates").get("template", [])

    if a.scaffold:
        # ⛔ THE DEFAULT IS THE STRICTEST CATEGORY, NOT THE COMMONEST ONE.
        # An earlier version defaulted every line to 'essential' with a warning to read them.
        # That is a permissive default dressed as a safeguard: someone who applies the file
        # unread gets every tracker firing without consent, which is invisible and is exactly
        # the failure this whole setup exists to prevent. Defaulting to 'marketing' means the
        # unread case over-blocks instead. That error is visible within minutes, and nobody's
        # visitor is tracked without consent while it lasts.
        skeleton = {t["name"]: "marketing" for t in tags if t.get("name") != INIT_TAG_NAME}
        print(json.dumps(skeleton, indent=2, ensure_ascii=False))
        print("\n// Every line defaults to 'marketing', the strictest category, so an unread",
              file=sys.stderr)
        print("// file over-blocks rather than under-blocks. Change each line to what the",
              file=sys.stderr)
        print("// tracker actually is. Valid: marketing, analytics, personalization,",
              file=sys.stderr)
        print("// essential, skip.", file=sys.stderr)
        print("// ⛔ 'essential' means FIRES WITHOUT ASKING. Use it only where the site stops",
              file=sys.stderr)
        print("//    working without that tracker.", file=sys.stderr)
        return 0

    if not a.map:
        raise SystemExit("--map is required. Build one with --scaffold first.")
    with open(a.map, encoding="utf-8") as f:
        mapping = json.load(f)
    unknown = sorted({v for v in mapping.values() if v not in CHECKS})
    if unknown:
        raise SystemExit("unknown categories in the map: %s\nValid: %s"
                         % (", ".join(unknown), ", ".join(CHECKS)))

    mode = "APPLYING" if a.apply else "SIMULATING (nothing will be written)"
    print("\n%s  account %s (%s), container %s\n" % (mode, live, a.account, a.container))

    state = "denied" if a.banner == "opt-in" else "granted"

    # step 2, template
    tpl = next((t for t in templates if t.get("name") == TEMPLATE_NAME), None)
    if tpl:
        print("  step 2  template already present, templateId %s" % tpl.get("templateId"))
    elif a.apply:
        tpl = call(tok, base + "/templates", "POST",
                   {"name": TEMPLATE_NAME, "templateData": fetch_template()})
        print("  step 2  template imported, templateId %s" % tpl.get("templateId"))
    else:
        print("  step 2  would download and import the official template")

    tag_type = "cvt_%s_%s" % (target["containerId"], tpl["templateId"]) if tpl else "cvt_<pending>"

    # steps 3 and 4, init tag.
    # ⛔ The parameter key is regionDefaults, which is the table. regionSettings is only the
    # group label shown in the interface and is NOT a parameter. Swapping them makes the
    # template discard the region with no error at all.
    init_body = {
        "name": INIT_TAG_NAME, "type": tag_type,
        "firingTriggerId": [TRIGGER_CONSENT_INIT],
        "parameter": [
            {"type": "list", "key": "regionDefaults", "list": [{
                "type": "map", "map": [{"type": "template", "key": "regions", "value": a.regions}]
                + [{"type": "template", "key": f, "value": state} for f in FIELDS]}]},
            {"type": "template", "key": "waitForUpdate", "value": a.wait},
        ],
    }
    init = next((t for t in tags if t.get("name") == INIT_TAG_NAME), None)
    if init and a.apply:
        body = dict(init_body); body["tagId"] = init["tagId"]
        call(tok, base + "/tags/%s" % init["tagId"], "PUT", body)
        print("  steps 3+4  init tag updated, regions '%s', all %s" % (a.regions, state))
    elif init:
        print("  steps 3+4  would update the existing init tag to regions '%s', all %s" % (a.regions, state))
    elif a.apply:
        r = call(tok, base + "/tags", "POST", init_body)
        print("  steps 3+4  init tag created, tagId %s, regions '%s', all %s" % (r.get("tagId"), a.regions, state))
    else:
        print("  steps 3+4  would create '%s' on Consent Initialization, regions '%s', all %s"
              % (INIT_TAG_NAME, a.regions, state))

    # step 5, trigger
    trg = next((t for t in triggers if t.get("name") == TRIGGER_NAME), None)
    if trg:
        print("  step 5  trigger already present, triggerId %s" % trg.get("triggerId"))
    elif a.apply:
        trg = call(tok, base + "/triggers", "POST", {
            "name": TRIGGER_NAME, "type": "customEvent",
            "customEventFilter": [{"type": "equals", "parameter": [
                {"type": "template", "key": "arg0", "value": "{{_event}}"},
                {"type": "template", "key": "arg1", "value": "consent-updated"}]}]})
        print("  step 5  trigger created, triggerId %s" % trg.get("triggerId"))
    else:
        print("  step 5  would create the '%s' trigger for event consent-updated" % TRIGGER_NAME)
    tid = trg.get("triggerId") if trg else "<new>"

    # steps 6 and 7
    print("\n  steps 6+7, tag by tag:")
    failures, counts = [], {}
    for t in tags:
        name = t.get("name", "?")
        if name == INIT_TAG_NAME:
            continue
        cat = mapping.get(name)
        if cat is None:
            print("    %-38s NOT IN THE MAP, left untouched" % name[:38])
            counts["unmapped"] = counts.get("unmapped", 0) + 1
            continue
        if cat == "skip":
            print("    %-38s skip, left untouched" % name[:38])
            counts["skip"] = counts.get("skip", 0) + 1
            continue
        checks = ", ".join(CHECKS[cat]) or "NONE, fires without asking"
        print("    %-38s %-16s %s" % (name[:38], cat, checks))
        counts[cat] = counts.get(cat, 0) + 1
        if a.apply:
            new = dict(t)
            new["firingTriggerId"] = [tid]
            new["consentSettings"] = consent_settings(cat)
            for k in ("path", "fingerprint", "tagManagerUrl", "workspaceId", "accountId", "containerId"):
                new.pop(k, None)
            try:
                call(tok, base + "/tags/%s" % t["tagId"], "PUT", new)
            except SystemExit as e:
                failures.append((name, str(e).splitlines()[0]))

    print("\n  summary: " + ", ".join("%d %s" % (v, k) for k, v in sorted(counts.items())))
    if counts.get("essential"):
        print("  ⚠️ %d tag(s) marked essential will fire without asking. Read that list again."
              % counts["essential"])

    if failures:
        print("\n  ⛔ %d tag(s) were NOT changed, so the container is half migrated:" % len(failures))
        for name, why in failures:
            print("     %-38s %s" % (name[:38], why))

    # step 8
    if a.apply:
        if failures:
            raise SystemExit("\n  ⛔ Not creating a version with %d tag(s) unchanged. A version "
                             "made of half-applied state is worse than none, because the history "
                             "says it was complete." % len(failures))
        ver = call(tok, base + ":create_version", "POST",
                   {"name": "Consent wiring %s" % datetime.now(timezone.utc).strftime("%Y-%m-%d")})
        if ver.get("compilerError") or ver.get("syntaxError"):
            raise SystemExit("\n  ⛔ The tag manager REFUSED the version. Tags were changed in the "
                             "workspace, nothing was published.\n     %s"
                             % json.dumps({k: v for k, v in ver.items() if k != "containerVersion"})[:400])
        vid = (ver.get("containerVersion") or {}).get("containerVersionId")
        if not vid:
            raise SystemExit("\n  ⛔ The version came back without an id: %s" % json.dumps(ver)[:300])
        print("\n  step 8  version %s created" % vid)
        if a.publish:
            call(tok, "/accounts/%s/containers/%s/versions/%s:publish"
                 % (a.account, target["containerId"], vid), "POST")
            print("  step 8  version %s PUBLISHED" % vid)
        else:
            print("  step 8  not published, add --publish when you are ready")
    else:
        print("\n  step 8  would create a version, and publish only with --publish")

    print("\n  step 9  tick the tag manager confirmation in the app: MANUAL, on screen")
    print("  NEXT     run audit-container.py and compare. A write being accepted is not the")
    print("           same claim as the state being what you intended.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
