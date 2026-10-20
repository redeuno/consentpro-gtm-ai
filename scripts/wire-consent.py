"""Configure a reviewed Consent Pro integration in Google Tag Manager.

READS or WRITES: reads GTM state; writes tags, templates, triggers and a version only
with --apply --approve-plan SHA256. Publishing also requires --publish. Without
--apply, even --publish only simulates. No customer data is saved locally.
Apply: first simulate the exact options, review every proposed change and existing
workspace change, then supply the printed PLAN_SHA256 using --approve-plan.
Repeat: existing objects are reused, but each application creates a new version.
A changed workspace or changed options invalidate the approval. Updates use GTM
fingerprints; readback precedes version creation and publication. There is no
transaction or automatic rollback. After failure, inspect the workspace and review
a new simulation; restore a prior GTM version manually if rollback is needed.

Page-load tags move to consent-updated. Business-event tags retain their triggers
and receive consent checks. Essential tags retain triggers; skip retains everything.
Only web containers with known capabilities are supported. Custom page-lifecycle
triggers require manual review. All version collections and the container are
compared with the approved inventory before publication.
Existing regional rows and optional settings are preserved when their flags are
omitted. The simple CLI cannot replace multiple regional rows. Configure Advanced
Consent Mode separately and use explicit skip for those reviewed tags.
"""

import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

API = "https://tagmanager.googleapis.com/tagmanager/v2"
TOKEN_URL = "https://oauth2.googleapis.com/token"
_spec = importlib.util.spec_from_file_location("consent_template", Path(__file__).with_name("consent-template.py"))
template_support = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(template_support)

CLIENT_FILE = os.environ.get("GTM_OAUTH_CLIENT")
TOKEN_FILE = os.environ.get("GTM_OAUTH_TOKEN")

TRIGGER_CONSENT_INIT = "2147479572"
TRIGGER_ALL_PAGES = "2147479553"

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
            "refresh tokens after seven days. Run authorise.py --apply --write again, and see its header for "
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


def consent_trigger(triggers):
    candidates = []
    for trigger in triggers:
        filters = trigger.get("customEventFilter") or []
        valid = (trigger.get("type") == "customEvent" and isinstance(filters, list) and len(filters) == 1
                 and isinstance(filters[0], dict)
                 and filters[0].get("type") == "equals"
                 and isinstance(filters[0].get("parameter"), list) and len(filters[0]["parameter"]) == 2
                 and all(isinstance(p, dict) and p.get("type") == "template" for p in filters[0]["parameter"])
                 and {p.get("key"): p.get("value") for p in filters[0].get("parameter", [])}
                 == {"arg0": "{{_event}}", "arg1": "consent-updated"}
                 and not trigger.get("filter") and not trigger.get("autoEventFilter"))
        if trigger.get("name") == TRIGGER_NAME and not valid:
            raise SystemExit("A trigger named Consent Updated has different event conditions. Resolve it before writing.")
        if valid:
            candidates.append(trigger)
    if len(candidates) > 1:
        raise SystemExit("Multiple consent-updated triggers; resolve ambiguity before writing.")
    return candidates[0] if candidates else None


def business_trigger(trigger):
    if trigger.get("type") in {"click", "linkClick", "formSubmission", "historyChange", "timer",
                               "youTubeVideo", "scrollDepth", "elementVisibility", "jsError"}:
        return True
    if trigger.get("type") != "customEvent":
        return False
    filters = trigger.get("customEventFilter")
    if not isinstance(filters, list) or len(filters) != 1 or not isinstance(filters[0], dict):
        return False
    condition = filters[0]
    parameters = condition.get("parameter")
    if (condition.get("type") != "equals" or not isinstance(parameters, list) or len(parameters) != 2
            or any(not isinstance(item, dict) or item.get("type") != "template" for item in parameters)):
        return False
    values = {item.get("key"): item.get("value") for item in parameters}
    event = values.get("arg1")
    return (values.get("arg0") == "{{_event}}" and isinstance(event, str) and bool(event)
            and "{{" not in event and not event.startswith("gtm.") and event != "consent-updated")


def region_parameters(init, banner, regions, wait):
    parameters = copy.deepcopy((init or {}).get("parameter") or [])
    tables = [p for p in parameters if p.get("key") == "regionDefaults"]
    if len(tables) > 1:
        raise SystemExit("Duplicate regionDefaults parameters; resolve before writing.")
    rows = tables[0].get("list", []) if tables else []
    if init and not rows and banner is None and regions is None:
        raise SystemExit("Existing initialization tag has no regional defaults. Supply --banner and --regions explicitly.")
    if len(rows) > 1 and (banner is not None or regions is not None):
        raise SystemExit("Multiple region rows cannot be replaced by this CLI. Omit --banner/--regions to preserve them, or edit in GTM.")
    if not init or banner is not None or regions is not None:
        if (banner is None) != (regions is None):
            raise SystemExit("Changing regional defaults requires both --banner and --regions.")
        banner = "opt-in" if banner is None else banner
        regions = "Global" if regions is None else regions
        if regions != "Global" and (not re.fullmatch(r"[A-Z]{2}(?:-[A-Z0-9]{1,3})?(?:,[A-Z]{2}(?:-[A-Z0-9]{1,3})?)*", regions)
                                    or "EU" in regions.split(",") or len(set(regions.split(","))) != len(regions.split(","))):
            raise SystemExit("Use Global or explicit unique region codes such as GB,US-CA. Expand EU and remove spaces.")
        state = "denied" if banner == "opt-in" else "granted"
        table = {"type": "list", "key": "regionDefaults", "list": [{"type": "map", "map": [
            {"type": "template", "key": "regions", "value": regions}]
            + [{"type": "template", "key": f, "value": state} for f in FIELDS]}]}
        parameters = [p for p in parameters if p.get("key") != "regionDefaults"] + [table]
    if wait is not None or not init:
        wait = "1000" if wait is None else wait
        if not str(wait).isdigit() or int(wait) > 10000:
            raise SystemExit("--wait must be an integer from 0 to 10000 milliseconds.")
        parameters = [p for p in parameters if p.get("key") != "waitForUpdate"] + [
            {"type": "template", "key": "waitForUpdate", "value": wait}]
    return parameters


METADATA = {"path", "fingerprint", "tagManagerUrl", "workspaceId", "accountId", "containerId", "containerVersionId"}
STATE_KEYS = {
    "tags": ("tag", "tagId"), "triggers": ("trigger", "triggerId"), "templates": ("customTemplate", "templateId"),
    "variables": ("variable", "variableId"), "folders": ("folder", "folderId"),
    "built_in_variables": ("builtInVariable", "type"), "zones": ("zone", "zoneId"),
    "clients": ("client", "clientId"), "gtag_config": ("gtagConfig", "gtagConfigId"),
    "transformations": ("transformation", "transformationId"),
}
FEATURE_KEYS = {
    "tags": "supportTags", "triggers": "supportTriggers", "templates": "supportTemplates",
    "variables": "supportVariables", "folders": "supportFolders", "built_in_variables": "supportBuiltInVariables",
    "zones": "supportZones", "clients": "supportClients", "gtag_config": "supportGtagConfigs",
    "transformations": "supportTransformations",
}
VERSION_METADATA = {"path", "accountId", "containerId", "containerVersionId", "name", "deleted", "description",
                    "fingerprint", "tagManagerUrl", "container"}


def validate_container(container, account, identifier, public_id):
    if (not isinstance(container, dict) or container.get("accountId") != account
            or container.get("containerId") != identifier or container.get("publicId") != public_id):
        raise SystemExit("Container identity is unavailable or differs from the selected target; no writes made.")
    if container.get("usageContext") != ["web"]:
        raise SystemExit("This writer supports web containers only. Review other container types manually; no writes made.")
    features = container.get("features")
    required = {*FEATURE_KEYS.values(), "supportWorkspaces", "supportVersions"}
    if not isinstance(features, dict) or any(not isinstance(features.get(key), bool) for key in required):
        raise SystemExit("Container capabilities are incomplete. Cannot inventory the full version safely; no writes made.")
    if any(not features[key] for key in ("supportWorkspaces", "supportVersions", "supportTags", "supportTriggers", "supportTemplates")):
        raise SystemExit("Container does not support the required consent workflow; no writes made.")


def container_body(container):
    if not isinstance(container, dict):
        raise SystemExit("Container readback is unavailable; refusing publication.")
    return {key: value for key, value in container.items() if key not in {"path", "fingerprint", "tagManagerUrl"}}


def entity_body(entity):
    return {key: copy.deepcopy(value) for key, value in entity.items() if key not in METADATA}


def normalized_state(state):
    for kind, items in state.items():
        identifier = STATE_KEYS[kind][1]
        if (not isinstance(items, list)
                or any(not isinstance(item, dict) or not isinstance(item.get(identifier), str)
                       or not item[identifier] for item in items)
                or len({item[identifier] for item in items}) != len(items)):
            raise SystemExit("Invalid or duplicate %s identity; inspect GTM before writing." % kind)
    return {kind: sorted((entity_body(item) for item in items), key=lambda x: str(x[STATE_KEYS[kind][1]]))
            for kind, items in state.items()}


def read_state(inventory, base, container):
    state = {kind: inventory(base + "/" + kind, "template" if kind == "templates" else STATE_KEYS[kind][0])
             if container["features"][FEATURE_KEYS[kind]] else []
             for kind in STATE_KEYS}
    normalized_state(state)
    return {kind: sorted(items, key=lambda item: item[STATE_KEYS[kind][1]]) for kind, items in state.items()}


def status_entities(status):
    if (not isinstance(status, dict) or status.get("mergeConflict")
            or not isinstance(status.get("workspaceChange", []), list)):
        raise SystemExit("Workspace status is unavailable or has merge conflicts. Resolve before writing.")
    changes = {}
    for change in status.get("workspaceChange", []):
        if not isinstance(change, dict):
            raise SystemExit("Invalid workspace change; inspect it in GTM.")
        kinds = [key for key in change if key != "changeStatus"]
        if len(kinds) != 1 or not isinstance(change[kinds[0]], dict):
            raise SystemExit("Unrecognized workspace change; inspect it in GTM.")
        kind = kinds[0]
        entity = change[kind]
        identifier = entity.get(kind + "Id") or entity.get("templateId") or entity.get("type")
        if identifier is None:
            raise SystemExit("Workspace change has no stable identity; inspect it in GTM.")
        key = (kind, str(identifier))
        if key in changes:
            raise SystemExit("Duplicate workspace change identity; inspect it in GTM.")
        changes[key] = change
    return changes


def verify_status(current, baseline, written):
    old, new = status_entities(baseline), status_entities(current)
    if {k: v for k, v in old.items() if k not in written} != {k: v for k, v in new.items() if k not in written}:
        raise SystemExit("Workspace changes outside this plan were detected. No version will be created.")


def plan_hash(plan):
    return hashlib.sha256(json.dumps(plan, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def print_diff(label, before, after):
    old, new = entity_body(before or {}), entity_body(after)
    changes = {key: {"before": old.get(key), "after": new.get(key)}
               for key in sorted(set(old) | set(new)) if old.get(key) != new.get(key)}
    print("  " + label + ": " + json.dumps(changes, ensure_ascii=False, sort_keys=True))


def checked_update(tok, base, original, desired):
    fingerprint = original.get("fingerprint")
    if not fingerprint:
        raise SystemExit("Existing tag has no fingerprint; refusing an unguarded update.")
    path = base + "/tags/" + original["tagId"]
    current = call(tok, path)
    if not isinstance(current, dict) or current.get("fingerprint") != fingerprint or entity_body(current) != entity_body(original):
        raise SystemExit("Tag changed after the approved plan: " + original.get("name", original["tagId"]))
    response = call(tok, path + "?" + urllib.parse.urlencode({"fingerprint": fingerprint}), "PUT", entity_body(desired))
    if not isinstance(response, dict) or not response.get("fingerprint") or entity_body(response) != entity_body(desired):
        raise SystemExit("Tag update response differs from the plan. Inspect the workspace; no version created.")
    return response


def verify_version(version, expected, container, identifier=None):
    if not isinstance(version, dict) or not version.get("containerVersionId") or not version.get("fingerprint"):
        raise SystemExit("Version identity or fingerprint is missing; refusing publication.")
    if identifier is not None and version["containerVersionId"] != identifier:
        raise SystemExit("Version readback identity differs from the requested version. Nothing will be published.")
    allowed = VERSION_METADATA | {key for key, _ in STATE_KEYS.values()}
    if set(version) - allowed:
        raise SystemExit("Version contains unrecognized fields or collections. Review the API schema; nothing will be published.")
    if (version.get("accountId") != container["accountId"] or version.get("containerId") != container["containerId"]
            or version.get("deleted") or container_body(version.get("container")) != container_body(container)):
        raise SystemExit("Version container differs from the approved target. Nothing will be published.")
    actual = {kind: version.get(key, []) for kind, (key, _) in STATE_KEYS.items()}
    if normalized_state(actual) != normalized_state(expected):
        raise SystemExit("Version readback differs from the verified workspace. Nothing will be published.")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--account", required=True)
    p.add_argument("--container", required=True, help="public id, GTM-XXXXXXX")
    p.add_argument("--confirm-name", help="the account name, exactly as printed")
    p.add_argument("--workspace")
    p.add_argument("--banner", choices=["opt-in", "opt-out"], help="omit to preserve existing regional defaults")
    p.add_argument("--regions", help="Global or explicit comma-separated region codes; omit to preserve existing rows")
    p.add_argument("--wait", help="wait for consent update in milliseconds; omit to preserve an existing value")
    p.add_argument("--map", help="JSON mapping every non-initialization tag name to a category or skip")
    p.add_argument("--scaffold", action="store_true", help="print a complete category map and exit")
    p.add_argument("--apply", action="store_true", help="apply the reviewed plan; otherwise simulate")
    p.add_argument("--publish", action="store_true", help="include publication in the plan; only writes with --apply")
    p.add_argument("--approve-plan", help="SHA-256 printed by the reviewed simulation")
    a = p.parse_args()
    if a.scaffold and (a.apply or a.publish or a.approve_plan):
        raise SystemExit("--scaffold cannot be combined with apply or publication.")

    tok = access_token()
    account = call(tok, "/accounts/%s" % a.account)
    live = account.get("name")
    if a.confirm_name is None:
        raise SystemExit("Account %s is named: %s\nRun again with --confirm-name \"%s\" if this is the intended account."
                         % (a.account, live, live))
    if a.confirm_name != live:
        raise SystemExit("Account %s is named '%s', not '%s'. Stopping." % (a.account, live, a.confirm_name))
    inventory = lambda path, key: template_support.list_all(lambda url: call(tok, url), path, key)
    containers = inventory("/accounts/%s/containers" % a.account, "container")
    target = next((c for c in containers if c.get("publicId") == a.container), None)
    if target is None:
        raise SystemExit("Container %s not found in account %s" % (a.container, a.account))
    container_base = "/accounts/%s/containers/%s" % (a.account, target["containerId"])
    container_id = target["containerId"]
    target = call(tok, container_base)
    validate_container(target, a.account, container_id, a.container)
    wss = inventory(container_base + "/workspaces", "workspace")
    ws = next((w for w in wss if w.get("workspaceId") == a.workspace), None) if a.workspace \
        else (wss[0] if len(wss) == 1 else None)
    if ws is None:
        raise SystemExit("Pick a workspace with --workspace: " + ", ".join(w.get("workspaceId", "?") for w in wss))
    base = container_base + "/workspaces/" + ws["workspaceId"]
    initial = read_state(inventory, base, target)
    tags, triggers, templates = initial["tags"], initial["triggers"], initial["templates"]
    tpl, identity = template_support.require_valid(templates)
    tag_type = template_support.tag_type(tpl, target["containerId"])
    existing_init = [tag for tag in tags if tag.get("name") == INIT_TAG_NAME
                     or tag_type and tag.get("type") == tag_type]
    if len(existing_init) > 1:
        raise SystemExit("Multiple Consent Pro initialization tags; resolve before changing anything")
    init = existing_init[0] if existing_init else None
    if init and (not tag_type or init.get("type") != tag_type):
        raise SystemExit("Initialization tag references an unverified template; no changes made")
    managed = [tag for tag in tags if tag is not init]
    names = [tag.get("name") for tag in managed]
    if any(not name for name in names) or len(names) != len(set(names)):
        raise SystemExit("Tag names must be present and unique before creating a category map.")
    if a.scaffold:
        print(json.dumps({name: "marketing" for name in names}, indent=2, ensure_ascii=False))
        print("Review every line. Essential removes additional checks; skip leaves the whole tag unchanged.", file=sys.stderr)
        return 0
    if not a.map:
        raise SystemExit("--map is required. Build one with --scaffold first.")
    with open(a.map, encoding="utf-8") as f:
        mapping = json.load(f)
    if not isinstance(mapping, dict) or any(not isinstance(value, str) or value not in CHECKS for value in mapping.values()):
        raise SystemExit("The category map must be an object using marketing, analytics, personalization, essential or skip.")
    if set(mapping) != set(names):
        raise SystemExit("Map must cover every tag exactly. Missing: %s; stale names: %s. Use explicit skip where appropriate."
                         % (", ".join(sorted(set(names) - set(mapping))) or "none",
                            ", ".join(sorted(set(mapping) - set(names))) or "none"))

    trg = consent_trigger(triggers)
    tid = trg["triggerId"] if trg else "<new>"
    known_triggers = {trigger["triggerId"]: trigger for trigger in triggers}
    trigger_body = {"name": TRIGGER_NAME, "type": "customEvent", "customEventFilter": [
        {"type": "equals", "parameter": [
            {"type": "template", "key": "arg0", "value": "{{_event}}"},
            {"type": "template", "key": "arg1", "value": "consent-updated"}]}]}
    init_body = entity_body(init or {})
    init_body.update({"name": init["name"] if init else INIT_TAG_NAME,
                      "type": tag_type or "cvt_<pending>", "firingTriggerId": [TRIGGER_CONSENT_INIT],
                      "parameter": region_parameters(init, a.banner, a.regions, a.wait)})
    planned = []
    for tag in managed:
        category = mapping[tag["name"]]
        if category == "skip":
            continue
        if not tag.get("fingerprint"):
            raise SystemExit("Existing tag has no fingerprint: " + tag["name"])
        desired = entity_body(tag)
        original_triggers = tag.get("firingTriggerId") or []
        if category != "essential":
            replaceable = {TRIGGER_ALL_PAGES, tid}
            if original_triggers and set(original_triggers) <= replaceable:
                desired["firingTriggerId"] = [tid]
            elif (not original_triggers or set(original_triggers) & replaceable
                  or not set(original_triggers) <= set(known_triggers)
                  or not all(business_trigger(known_triggers[identifier]) for identifier in original_triggers)):
                raise SystemExit("Unsupported or mixed firing triggers on '%s'. Review in GTM or map it to skip; no writes made."
                                 % tag["name"])
        desired["consentSettings"] = consent_settings(category)
        planned.append((tag, desired))
    if init and not init.get("fingerprint"):
        raise SystemExit("Existing initialization tag has no fingerprint; refusing an unguarded update.")
    baseline_status = call(tok, base + "/status")
    prior_changes = status_entities(baseline_status)
    plan = {"account": account, "container": target, "workspace": ws, "state": initial,
            "workspace_status": baseline_status, "mapping": mapping, "initialization": init_body,
            "trigger": trg or trigger_body, "tags": [desired for _, desired in planned], "publish": a.publish}
    approval = plan_hash(plan)
    print("\n%s account %s (%s), container %s, workspace %s"
          % ("APPLYING" if a.apply else "SIMULATING (nothing will be written)", live, a.account,
             a.container, ws.get("name", ws["workspaceId"])))
    print("Existing workspace changes included in the version: " + str(len(prior_changes)))
    for (kind, identifier), change in prior_changes.items():
        print("  %s %s: %s" % (kind, identifier, change[kind].get("name", change.get("changeStatus", "unknown"))))
    print("Version inventory approved for preservation: " + ", ".join(
        "%s=%d" % (kind, len(items)) for kind, items in initial.items()))
    if tpl:
        print("  step 2 existing template preserved: " + template_support.describe(identity))
    else:
        print("  step 2 would import gallery %s/%s at %s (permissions acknowledged on --apply)"
              % (template_support.OWNER, template_support.REPOSITORY, template_support.VERSION))
    print_diff("steps 3+4 initialization changes", init, init_body)
    print("  step 5 " + ("reuse verified consent-updated trigger " + tid if trg else "create consent-updated trigger"))
    for tag, desired in planned:
        print("  %s: %s; firing triggers %s -> %s" % (tag["name"], mapping[tag["name"]],
              tag.get("firingTriggerId", []), desired.get("firingTriggerId", [])))
        print_diff("tag changes", tag, desired)
    for tag in managed:
        if mapping[tag["name"]] == "skip":
            print("  %s: explicitly skipped, unchanged" % tag["name"])
    print("  step 8 create a version" + (" and publish after readback" if a.publish else "; do not publish"))
    print("PLAN_SHA256=" + approval)
    if a.apply and a.approve_plan != approval:
        raise SystemExit("Review the simulation, then pass --apply --approve-plan " + approval + ". A changed plan requires new approval.")
    if not a.apply:
        return 0
    if (call(tok, container_base) != target or read_state(inventory, base, target) != initial
            or call(tok, base + "/status") != baseline_status):
        raise SystemExit("Workspace changed after planning. Simulate and approve again; no writes made.")

    expected = copy.deepcopy(initial)
    written = set()
    if tpl is None:
        imported = call(tok, template_support.import_path(base), "POST")
        if not isinstance(imported, dict):
            raise SystemExit("Invalid gallery import response; inspect workspace before retrying")
        location = {"accountId": a.account, "containerId": target["containerId"], "workspaceId": ws["workspaceId"]}
        if any(key in imported and imported[key] != value for key, value in location.items()):
            raise SystemExit("Gallery import returned a different workspace; inspect before retrying")
        tpl, identity = template_support.require_valid([imported])
        if not tpl or identity["source"] != "gallery":
            raise SystemExit("Gallery import identity unverified; inspect workspace before retrying")
        expected["templates"].append(tpl)
        written.add(("customTemplate", str(tpl["templateId"])))
    init_body["type"] = template_support.tag_type(tpl, target["containerId"])
    if init:
        updated = checked_update(tok, base, init, init_body)
        expected["tags"] = [updated if tag["tagId"] == init["tagId"] else tag for tag in expected["tags"]]
    else:
        updated = call(tok, base + "/tags", "POST", init_body)
        if (not isinstance(updated, dict) or not isinstance(updated.get("tagId"), str) or not updated["tagId"]
                or updated["tagId"] in {tag["tagId"] for tag in expected["tags"]}):
            raise SystemExit("Initialization tag response has no identity; inspect workspace before retrying.")
        if entity_body(updated) != dict(init_body, tagId=updated["tagId"]):
            raise SystemExit("Initialization tag response differs from the plan; no version will be created.")
        expected["tags"].append(updated)
    written.add(("tag", str(updated["tagId"])))
    if trg is None:
        trg = call(tok, base + "/triggers", "POST", trigger_body)
        if (not isinstance(trg, dict) or not isinstance(trg.get("triggerId"), str) or not trg["triggerId"]
                or trg["triggerId"] in {item["triggerId"] for item in expected["triggers"]}):
            raise SystemExit("Consent trigger response has no identity; inspect workspace before retrying.")
        if consent_trigger([trg]) is None or entity_body(trg) != dict(trigger_body, triggerId=trg["triggerId"]):
            raise SystemExit("Consent trigger response differs from the plan; no version will be created.")
        expected["triggers"].append(trg)
        written.add(("trigger", str(trg["triggerId"])))
    for original, desired in planned:
        if desired.get("firingTriggerId") == ["<new>"]:
            desired["firingTriggerId"] = [trg["triggerId"]]
        updated = checked_update(tok, base, original, desired)
        expected["tags"] = [updated if tag["tagId"] == original["tagId"] else tag for tag in expected["tags"]]
        written.add(("tag", str(updated["tagId"])))
    actual = read_state(inventory, base, target)
    if normalized_state(actual) != normalized_state(expected):
        raise SystemExit("Workspace readback differs from the plan. Changes may be partial; no version will be created.")
    if container_body(call(tok, container_base)) != container_body(target):
        raise SystemExit("Container changed after planning. No version will be created.")
    verify_status(call(tok, base + "/status"), baseline_status, written)
    ver = call(tok, base + ":create_version", "POST",
               {"name": "Consent wiring %s" % datetime.now(timezone.utc).strftime("%Y-%m-%d")})
    if not isinstance(ver, dict) or ver.get("compilerError") or ver.get("syntaxError"):
        raise SystemExit("Version compilation failed. Workspace changes may remain; nothing was published.")
    version = ver.get("containerVersion")
    vid = version.get("containerVersionId") if isinstance(version, dict) else None
    if not isinstance(vid, str) or not vid:
        raise SystemExit("Version response has no id. Inspect the workspace before retrying.")
    version_path = container_base + "/versions/" + vid
    saved = call(tok, version_path)
    verify_version(saved, expected, target, vid)
    print("Version %s created and read back." % vid)
    if a.publish:
        fresh = call(tok, version_path)
        verify_version(fresh, expected, target, vid)
        if fresh.get("fingerprint") != saved.get("fingerprint"):
            raise SystemExit("Version fingerprint changed before publication. Nothing was published.")
        result = call(tok, version_path + ":publish?" + urllib.parse.urlencode({"fingerprint": fresh["fingerprint"]}), "POST")
        if not isinstance(result, dict) or result.get("compilerError"):
            raise SystemExit("GTM reported a publication compile error. Inspect the live version.")
        published = call(tok, container_base + "/versions:live")
        verify_version(published, expected, target)
        if published.get("containerVersionId") != vid:
            raise SystemExit("Live version does not match the published version. Inspect GTM before retrying.")
        print("Version %s published and confirmed live." % vid)
    else:
        print("Not published. Publication requires a separate simulation with --publish and new approval.")
    print("Next: test named trackers in the browser. No runtime behaviour was verified by this script.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
