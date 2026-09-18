"""
What it does: checks a Google Tag Manager container against the Consent Pro setup guide and
          reports which of the consent steps are in place. Answers "is this container wired
          to consent, or does it just have tags in it?".
READS or WRITES: **READS ONLY.** There is no write path in this file, by design. An audit
          that fixes things on its own hides what was wrong. With --save it writes one JSON
          diagnostic to the current directory, which is local disk.
How to apply: nothing is applied. There is no apply flag.
Safe to run again? Always. It is a pure read.

REQUIRES a Google OAuth credential with the tagmanager.readonly scope. Setting one up is
outside this script: see Google's Tag Manager API quickstart. Point the two environment
variables below at the client file and the refresh token.

⛔ WHY IT ASKS YOU TO CONFIRM THE ACCOUNT NAME:
   a Google credential usually reaches every container that account can see, including other
   clients and production properties. An account id is easy to mistype and impossible to
   sanity check by eye. This script prints the live account name and requires you to pass it
   back with --confirm-name, so a wrong target fails before it reads anything else.

Usage:
   python audit-container.py --account 1234567890 --container GTM-XXXXXXX
   (it will print the account name and tell you what to pass to --confirm-name)
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

CLIENT_FILE = os.environ.get("GTM_OAUTH_CLIENT")
TOKEN_FILE = os.environ.get("GTM_OAUTH_TOKEN")

# Built-in trigger ids. They do not appear in the workspace trigger list.
TRIGGER_ALL_PAGES = "2147479553"
TRIGGER_CONSENT_INIT = "2147479573"


def access_token():
    if not CLIENT_FILE or not TOKEN_FILE:
        raise SystemExit(
            "Set GTM_OAUTH_CLIENT to your OAuth client json and GTM_OAUTH_TOKEN to the file "
            "holding the refresh token.")
    with open(CLIENT_FILE, encoding="utf-8") as f:
        cli = json.load(f)["installed"]
    with open(TOKEN_FILE, encoding="utf-8") as f:
        refresh = f.read().strip()
    data = urllib.parse.urlencode({
        "client_id": cli["client_id"],
        "client_secret": cli["client_secret"],
        "refresh_token": refresh,
        "grant_type": "refresh_token",
    }).encode()
    with urllib.request.urlopen(urllib.request.Request(TOKEN_URL, data=data), timeout=40) as r:
        return json.load(r)["access_token"]


def read(tok, path, attempts=4):
    """Backoff on retry. Live reads fail often enough that stopping at the first refusal
    turns 'did not answer' into 'does not exist'."""
    wait = 3
    for n in range(attempts):
        req = urllib.request.Request(API + path, method="GET")
        req.add_header("Authorization", "Bearer " + tok)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:400]
            if e.code in (429, 500, 502, 503) and n < attempts - 1:
                time.sleep(wait); wait *= 2; continue
            raise SystemExit("HTTP %s on %s\n%s" % (e.code, path, body))
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            if n < attempts - 1:
                time.sleep(wait); wait *= 2; continue
            raise SystemExit("transport failure on %s: %s" % (path, e))
    raise SystemExit("no answer: " + path)


def trigger_name(tid, triggers):
    if tid == TRIGGER_ALL_PAGES:
        return "All Pages (built-in)"
    if tid == TRIGGER_CONSENT_INIT:
        return "Consent Initialization - All Pages (built-in)"
    for t in triggers:
        if t.get("triggerId") == tid:
            return "%s [%s]" % (t.get("name", "?"), t.get("type", "?"))
    return "id %s (not in this workspace)" % tid


def has_consent_check(tag):
    cs = tag.get("consentSettings") or {}
    return cs.get("consentStatus") == "needed" or bool(cs.get("consentType"))


def scanner_can_see(tag, consent_updated_ids):
    """Can the Consent Pro scanner see this tag at all?

    ⛔ THIS IS THE CHECK THAT EXPLAINS 'THE SCAN MISSED MY TRACKER'.
    The official documentation is explicit: the scanner only detects scripts from Google Tag
    Manager that fire on 'All Pages' or on a Consent Pro custom event such as
    'consent-updated'. A tag on any other trigger (a click, a timer, a scroll, one specific
    page, a custom event of your own) is INVISIBLE to it.

    The consequence people hit: that tracker never appears in the app, never gets a category,
    and therefore never gets a consent check. It fires, and nothing in the product mentions
    it exists. This is documented behaviour, not a bug, and it is the single most common
    reason a scan comes back with fewer trackers than the site actually loads.
    """
    triggers = set(tag.get("firingTriggerId") or [])
    if not triggers:
        return False
    # ⛔ The initialization tag is NOT a tracker, it is the consent layer itself. It belongs on
    # Consent Initialization by design, and the scanner has no reason to see it. Flagging it
    # would be a false alarm, and a checker that cries wolf on its own correct setup is a
    # checker people stop reading.
    if TRIGGER_CONSENT_INIT in triggers:
        return True
    return bool(triggers & ({TRIGGER_ALL_PAGES} | consent_updated_ids))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--account", required=True, help="account id")
    p.add_argument("--container", required=True, help="public id, GTM-XXXXXXX")
    p.add_argument("--confirm-name", default=None,
                   help="the account name, exactly as printed on the first run")
    p.add_argument("--workspace", default=None)
    p.add_argument("--save", action="store_true", help="write a json diagnostic here")
    a = p.parse_args()

    tok = access_token()

    account = read(tok, "/accounts/%s" % a.account)
    live_name = account.get("name")
    if a.confirm_name is None:
        raise SystemExit(
            "\nAccount %s is named: %s\n\nIf that is the right account, run again adding:\n"
            "  --confirm-name \"%s\"\n\nIf it is not, stop and check the id.\n"
            % (a.account, live_name, live_name))
    if a.confirm_name != live_name:
        raise SystemExit(
            "Account %s is named '%s', not '%s'. Stopping." % (a.account, live_name, a.confirm_name))

    containers = read(tok, "/accounts/%s/containers" % a.account).get("container", [])
    target = next((c for c in containers if c.get("publicId") == a.container), None)
    if target is None:
        raise SystemExit("container %s not found in account %s" % (a.container, a.account))

    wss = read(tok, "/accounts/%s/containers/%s/workspaces"
               % (a.account, target["containerId"])).get("workspace", [])
    if a.workspace:
        ws = next((w for w in wss if w.get("workspaceId") == a.workspace), None)
        if ws is None:
            raise SystemExit("workspace %s not found" % a.workspace)
    elif len(wss) == 1:
        ws = wss[0]
    else:
        raise SystemExit("there are %d workspaces, pick one with --workspace: %s"
                         % (len(wss), ", ".join(w.get("workspaceId", "?") for w in wss)))

    base = "/accounts/%s/containers/%s/workspaces/%s" % (
        a.account, target["containerId"], ws["workspaceId"])
    tags = read(tok, base + "/tags").get("tag", [])
    triggers = read(tok, base + "/triggers").get("trigger", [])
    templates = read(tok, base + "/templates").get("template", [])

    print("\nACCOUNT   %s (%s)" % (live_name, a.account))
    print("CONTAINER %s (%s), workspace %s" % (a.container, target.get("name", "?"), ws.get("name", "?")))
    print("%d tags, %d workspace triggers, %d templates\n" % (len(tags), len(triggers), len(templates)))

    tpl = [t for t in templates
           if "consent" in (t.get("name", "") + json.dumps(t.get("templateData", ""))).lower()]
    init = [t for t in tags if TRIGGER_CONSENT_INIT in (t.get("firingTriggerId") or [])]

    def is_consent_updated(t):
        if t.get("type") != "customEvent":
            return False
        for f in t.get("customEventFilter", []):
            for par in f.get("parameter", []):
                if par.get("key") == "arg1" and par.get("value") == "consent-updated":
                    return True
        return False

    cu = [t for t in triggers if is_consent_updated(t)]
    cu_ids = {t["triggerId"] for t in cu}
    on_cu = [t for t in tags if cu_ids & set(t.get("firingTriggerId") or [])]
    checked = [t for t in tags if has_consent_check(t)]

    steps = [
        ("2. Consent Pro template imported", bool(tpl),
         "%d template(s)" % len(tpl) if tpl else "no templates in this workspace"),
        ("3. Init tag on Consent Initialization", bool(init),
         "%d tag(s)" % len(init) if init else "no tag uses the initialization trigger"),
        ("5. Consent Updated trigger (consent-updated)", bool(cu),
         "%d trigger(s)" % len(cu) if cu else "no custom event trigger for that event"),
        ("6. Tags moved onto that trigger", bool(on_cu), "%d of %d tags" % (len(on_cu), len(tags))),
        ("7. Per-tag consent check", bool(checked), "%d of %d tags" % (len(checked), len(tags))),
    ]

    print("CONSENT STEPS FROM THE OFFICIAL GUIDE:")
    for name, ok, detail in steps:
        print("  %s  %-48s %s" % ("[x]" if ok else "[ ]", name, detail))

    print("\nHOW EACH TAG FIRES TODAY:")
    invisible = []
    for t in tags:
        names = [trigger_name(g, triggers) for g in (t.get("firingTriggerId") or [])]
        flags = []
        if not has_consent_check(t):
            flags.append("no consent check")
        if not scanner_can_see(t, cu_ids):
            flags.append("SCANNER CANNOT SEE THIS")
            invisible.append((t.get("name", "?"), ", ".join(names) or "no trigger"))
        mark = ("   (" + "; ".join(flags) + ")") if flags else ""
        print("  %-40s %s%s" % (t.get("name", "?")[:40], ", ".join(names) or "no trigger", mark))

    if invisible:
        print("\n⛔ %d TAG(S) THE CONSENT PRO SCANNER CANNOT SEE:" % len(invisible))
        for name, trg in invisible:
            print("   %-40s fires on: %s" % (name[:40], trg))
        print("   The docs are explicit: the scanner only detects tags that fire on 'All Pages'")
        print("   or on a Consent Pro event such as 'consent-updated'. These will never appear")
        print("   in the app, never get a category, and never get a consent check. They fire,")
        print("   and nothing in the product says they exist.")
        print("   This is documented behaviour, and it is the usual reason a scan returns fewer")
        print("   trackers than the site loads. Fix: move them to 'Consent Updated', or to")
        print("   'All Pages' if you only need them detected.")

    done = sum(1 for _, ok, _ in steps if ok)
    print("\nRESULT: %d of %d consent steps are in place." % (done, len(steps)))
    if done == 0:
        print("  The container has tags in it and no consent integration at all.")
        print("  The scanner still DETECTS those tags, because detection works on All Pages.")
        print("  Blocking does not happen: they fire before the visitor chooses.")
    elif done < len(steps):
        print("  Partially wired. The unchecked steps above are what is missing.")
    else:
        print("  All steps present. This reads configuration, not behaviour:")
        print("  load the site, refuse, and inspect cookies to test what actually happens.")

    if a.save:
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        out = "gtm-consent-audit-%s-%s.json" % (a.container, stamp)
        with open(out, "w", encoding="utf-8") as f:
            json.dump({
                "read_at": datetime.now(timezone.utc).isoformat(),
                "account": a.account, "account_name": live_name, "container": a.container,
                "workspace": ws.get("workspaceId"),
                "steps": [{"step": n, "done": ok, "detail": d} for n, ok, d in steps],
                "tags": tags, "triggers": triggers, "templates": templates,
            }, f, ensure_ascii=False, indent=2)
        print("\ndiagnostic saved to %s" % out)


if __name__ == "__main__":
    main()
