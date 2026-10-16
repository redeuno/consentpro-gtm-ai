import contextlib
import copy
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
import urllib.parse
import urllib.request

from test_gallery_install import FakeAPI, load, template_data


def trigger(identifier="88", name="Consent Updated", event="consent-updated"):
    return {"triggerId": identifier, "name": name, "type": "customEvent", "customEventFilter": [
        {"type": "equals", "parameter": [
            {"type": "template", "key": "arg0", "value": "{{_event}}"},
            {"type": "template", "key": "arg1", "value": event}]}]}


class WireSafetyTests(unittest.TestCase):
    def setUp(self):
        self.wire = load("wire-consent")
        helper = self.wire.template_support
        helper.CONTENT_HASH = helper.content_hash(template_data())
        self.api = FakeAPI(helper)
        self.api.templates = [self.api.template()]
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.mapping = Path(self.temp.name) / "map.json"
        self.mapping.write_text('{"Analytics":"analytics"}', encoding="utf-8")

    def run_cli(self, extra=(), dispatch=None):
        args = [self.wire.__file__, "--account", "123", "--container", "GTM-LAB", "--confirm-name", "Lab",
                "--map", str(self.mapping), *extra]
        output = io.StringIO()
        with mock.patch.object(sys, "argv", args), \
                mock.patch.object(self.wire, "access_token", return_value="fake"), \
                mock.patch.object(self.wire, "call", dispatch or self.api), \
                mock.patch.object(urllib.request, "urlopen", side_effect=AssertionError("Unexpected network access")), \
                contextlib.redirect_stdout(output):
            self.wire.main()
        return output.getvalue()

    def approve(self, extra=()):
        return self.run_cli(extra).split("PLAN_SHA256=")[-1].splitlines()[0]

    def apply(self, extra=(), dispatch=None):
        approval = self.approve(extra)
        return self.run_cli([*extra, "--apply", "--approve-plan", approval], dispatch)

    def has_write(self, suffix):
        return any(urllib.parse.urlsplit(path).path.endswith(suffix) for path, _, _ in self.api.writes)

    def initialization(self, rows):
        parameters = [{"type": "list", "key": "regionDefaults", "list": [
            {"type": "map", "map": [{"type": "template", "key": "regions", "value": region}]
             + [{"type": "template", "key": field, "value": state} for field in self.wire.FIELDS]}
            for region, state in rows]},
            {"type": "boolean", "key": "urlPassthrough", "value": "true"},
            {"type": "template", "key": "waitForUpdate", "value": "500"}]
        init = {"tagId": "2", "name": "Consent Pro Init", "type": "cvt_WRGND", "fingerprint": "init-v1",
                "firingTriggerId": [self.wire.TRIGGER_CONSENT_INIT], "parameter": parameters}
        self.api.tags.append(init)
        return init

    def test_wrong_named_trigger_fails_before_writes(self):
        self.api.triggers = [trigger(event="purchase")]
        with self.assertRaisesRegex(SystemExit, "different event conditions"):
            self.apply()
        self.assertEqual(self.api.writes, [])

    def test_filtered_or_mismatched_consent_trigger_fails_before_writes(self):
        for field in ("filter", "arg0", "type"):
            with self.subTest(field=field):
                existing = trigger()
                if field == "arg0":
                    existing["customEventFilter"][0]["parameter"][0]["value"] = "{{Page URL}}"
                elif field == "type":
                    existing["customEventFilter"][0]["type"] = "contains"
                else:
                    existing[field] = [{"type": "equals"}]
                self.api.triggers = [existing]
                with self.assertRaises(SystemExit):
                    self.apply()
                self.assertEqual(self.api.writes, [])

    def test_malformed_named_trigger_fails_cleanly_before_writes(self):
        for filters in ({"type": "equals"}, [None], [{"type": "equals", "parameter": None}],
                        [{"type": "equals", "parameter": [None, {}]}]):
            with self.subTest(filters=filters):
                self.api.triggers = [dict(trigger(), customEventFilter=filters)]
                with self.assertRaisesRegex(SystemExit, "different event conditions"):
                    self.apply()
                self.assertEqual(self.api.writes, [])

    def test_missing_or_duplicate_inventory_identity_fails_before_writes(self):
        for tags in ([{"name": "Missing identifier"}], [self.api.tags[0], self.api.tags[0]]):
            with self.subTest(tags=tags):
                self.api.tags = tags
                with self.assertRaisesRegex(SystemExit, "Invalid or duplicate tags identity"):
                    self.apply()
                self.assertEqual(self.api.writes, [])

    def test_verified_trigger_is_reused_even_if_renamed(self):
        self.api.triggers = [trigger(name="Existing consent event")]
        self.apply()
        self.assertEqual(self.api.tags[0]["firingTriggerId"], ["88"])
        self.assertFalse(self.has_write("/triggers"))

    def test_duplicate_consent_events_fail_before_writes(self):
        self.api.triggers = [trigger(), trigger("89", "Other consent event")]
        with self.assertRaisesRegex(SystemExit, "Multiple consent-updated"):
            self.apply()
        self.assertEqual(self.api.writes, [])

    def test_business_event_keeps_trigger_and_gains_consent_checks(self):
        self.api.triggers = [trigger(), trigger("77", "Purchase", "purchase")]
        self.api.tags[0]["firingTriggerId"] = ["77"]
        self.apply()
        tag = self.api.tags[0]
        self.assertEqual(tag["firingTriggerId"], ["77"])
        self.assertEqual(tag["consentSettings"]["consentType"]["list"], [{"type": "template", "value": "analytics_storage"}])

    def test_page_lifecycle_and_unknown_triggers_fail_before_writes(self):
        for kind in ("pageview", "domReady", "windowLoaded", "init", "consentInit", "triggerGroup", "always", "futureType"):
            with self.subTest(kind=kind):
                self.api.triggers = [{"triggerId": "77", "name": "Filtered page lifecycle", "type": kind,
                                      "filter": [{"type": "contains", "parameter": [
                                          {"type": "template", "key": "arg0", "value": "{{Page Path}}"},
                                          {"type": "template", "key": "arg1", "value": "/shop"}]}]}]
                self.api.tags[0]["firingTriggerId"] = ["77"]
                with self.assertRaisesRegex(SystemExit, "Unsupported or mixed"):
                    self.apply()
                self.assertEqual(self.api.writes, [])

    def test_custom_lifecycle_events_and_patterns_need_manual_review(self):
        for event, operator in (("gtm.js", "equals"), ("gtm.dom", "equals"), (".*", "matchRegex"), ("{{Event name}}", "equals")):
            with self.subTest(event=event):
                existing = trigger("77", "Lifecycle alias", event)
                existing["customEventFilter"][0]["type"] = operator
                self.api.triggers = [existing]
                self.api.tags[0]["firingTriggerId"] = ["77"]
                with self.assertRaisesRegex(SystemExit, "Unsupported or mixed"):
                    self.apply()
                self.assertEqual(self.api.writes, [])

    def test_click_trigger_and_its_conditions_are_preserved(self):
        self.api.triggers = [{"triggerId": "77", "name": "Checkout click", "type": "linkClick",
                              "filter": [{"type": "contains", "parameter": [
                                  {"type": "template", "key": "arg0", "value": "{{Click URL}}"},
                                  {"type": "template", "key": "arg1", "value": "/checkout"}]}]}]
        self.api.tags[0]["firingTriggerId"] = ["77"]
        original = copy.deepcopy(self.api.triggers)
        self.apply()
        self.assertEqual(self.api.tags[0]["firingTriggerId"], ["77"])
        self.assertEqual(self.api.triggers[0], original[0])

    def test_essential_keeps_page_trigger_and_skip_keeps_everything(self):
        self.mapping.write_text('{"Analytics":"essential"}', encoding="utf-8")
        self.apply()
        self.assertEqual(self.api.tags[0]["firingTriggerId"], [self.wire.TRIGGER_ALL_PAGES])
        self.assertEqual(self.api.tags[0]["consentSettings"], {"consentStatus": "notSet"})
        self.mapping.write_text('{"Analytics":"skip"}', encoding="utf-8")
        before = copy.deepcopy(self.api.tags[0])
        self.apply()
        self.assertEqual(self.api.tags[0], before)

    def test_mixed_unknown_or_initialization_triggers_require_manual_review(self):
        self.api.triggers = [trigger(), trigger("77", "Purchase", "purchase")]
        for triggers in ([self.wire.TRIGGER_ALL_PAGES, "77"], ["unknown"], [], [self.wire.TRIGGER_CONSENT_INIT]):
            with self.subTest(triggers=triggers):
                self.api.tags[0]["firingTriggerId"] = triggers
                with self.assertRaisesRegex(SystemExit, "Unsupported or mixed"):
                    self.apply()
                self.assertEqual(self.api.writes, [])

    def test_multiregion_and_optional_parameters_are_preserved(self):
        init = self.initialization([("GB", "denied"), ("US-CA", "granted")])
        original = copy.deepcopy(init["parameter"])
        self.apply()
        self.assertEqual(self.api.tags[1]["parameter"], original)

    def test_explicit_multiregion_replacement_fails_before_writes(self):
        self.initialization([("GB", "denied"), ("US-CA", "granted")])
        with self.assertRaisesRegex(SystemExit, "Multiple region rows"):
            self.apply(["--banner", "opt-in", "--regions", "GB"])
        self.assertEqual(self.api.writes, [])

    def test_single_region_change_preserves_unrelated_parameters(self):
        self.initialization([("GB", "denied")])
        self.apply(["--banner", "opt-out", "--regions", "US-CA"])
        parameters = {item["key"]: item for item in self.api.tags[1]["parameter"]}
        self.assertEqual(parameters["urlPassthrough"]["value"], "true")
        self.assertEqual(parameters["waitForUpdate"]["value"], "500")
        row = {item["key"]: item["value"] for item in parameters["regionDefaults"]["list"][0]["map"]}
        self.assertEqual(row["regions"], "US-CA")
        self.assertEqual(row["analyticsStorage"], "granted")

    def test_invalid_region_inputs_fail_before_writes(self):
        for extra in (["--regions", "GB"], ["--banner", "opt-in"],
                      ["--banner", "opt-in", "--regions", "EU"],
                      ["--banner", "opt-in", "--regions", "Global (default)"],
                      ["--banner", "opt-in", "--regions", "GB, GB"],
                      ["--banner", "opt-in", "--regions", "GB,GB"], ["--wait", "-1"]):
            with self.subTest(extra=extra):
                with self.assertRaises(SystemExit):
                    self.apply(extra)
                self.assertEqual(self.api.writes, [])

    def test_unmapped_tags_cannot_be_silently_skipped(self):
        self.mapping.write_text('{}', encoding="utf-8")
        with self.assertRaisesRegex(SystemExit, "Map must cover every tag"):
            self.apply()
        self.assertEqual(self.api.writes, [])

    def test_stale_names_and_duplicate_names_fail_before_writes(self):
        self.mapping.write_text('{"Analytics":"analytics","Old tag":"skip"}', encoding="utf-8")
        with self.assertRaisesRegex(SystemExit, "stale names"):
            self.apply()
        self.api.tags.append(dict(self.api.tags[0], tagId="8"))
        with self.assertRaisesRegex(SystemExit, "unique"):
            self.apply()
        self.assertEqual(self.api.writes, [])

    def test_apply_requires_approval_hash(self):
        with self.assertRaisesRegex(SystemExit, "approve-plan"):
            self.run_cli(["--apply"])
        self.assertEqual(self.api.writes, [])

    def test_changed_state_and_publish_intent_invalidate_approval(self):
        approval = self.approve()
        with self.assertRaisesRegex(SystemExit, "changed plan"):
            self.run_cli(["--apply", "--publish", "--approve-plan", approval])
        self.api.tags[0]["notes"] = "Changed outside this plan"
        with self.assertRaisesRegex(SystemExit, "changed plan"):
            self.run_cli(["--apply", "--approve-plan", approval])
        self.assertEqual(self.api.writes, [])

    def test_publish_flag_without_apply_only_simulates(self):
        self.run_cli(["--publish"])
        self.assertEqual(self.api.writes, [])

    def test_plan_exposes_changed_settings_and_initialization_fields(self):
        init = self.initialization([("GB", "denied")])
        init["firingTriggerId"] = [self.wire.TRIGGER_ALL_PAGES]
        self.api.tags[0]["consentSettings"] = {"consentStatus": "notSet"}
        output = self.run_cli()
        initial_diff = json.loads(next(line.split(": ", 1)[1] for line in output.splitlines()
                                       if "steps 3+4 initialization changes:" in line))
        tag_diff = json.loads(next(line.split(": ", 1)[1] for line in output.splitlines() if "tag changes:" in line))
        self.assertEqual(initial_diff["firingTriggerId"], {
            "before": [self.wire.TRIGGER_ALL_PAGES], "after": [self.wire.TRIGGER_CONSENT_INIT]})
        self.assertEqual(tag_diff["consentSettings"], {
            "before": {"consentStatus": "notSet"}, "after": self.wire.consent_settings("analytics")})
        self.assertEqual(self.api.writes, [])

    def test_missing_tag_fingerprint_fails_before_writes(self):
        del self.api.tags[0]["fingerprint"]
        with self.assertRaisesRegex(SystemExit, "no fingerprint"):
            self.apply()
        self.assertEqual(self.api.writes, [])

    def test_unknown_container_capabilities_fail_before_writes(self):
        features = copy.deepcopy(self.api.container["features"])
        for bad in (None, {key: value for key, value in features.items() if key != "supportZones"},
                    dict(features, supportVariables="true")):
            with self.subTest(features=bad):
                self.api.container["features"] = bad
                with self.assertRaisesRegex(SystemExit, "capabilities are incomplete"):
                    self.apply()
                self.assertEqual(self.api.writes, [])

    def test_non_web_container_fails_before_writes(self):
        for usage in (["server"], ["amp"], ["android"], []):
            with self.subTest(usage=usage):
                self.api.container["usageContext"] = usage
                with self.assertRaisesRegex(SystemExit, "web containers only"):
                    self.apply()
                self.assertEqual(self.api.writes, [])

    def test_disabled_capabilities_do_not_call_incompatible_endpoints(self):
        self.apply()
        for resource in ("zones", "clients", "gtag_config", "transformations"):
            self.assertFalse(any(urllib.parse.urlsplit(path).path.endswith("/" + resource)
                                 for path, _, _ in self.api.requests))

    def test_full_version_inventory_is_paginated_and_preserved(self):
        samples = {
            "variables": {"variableId": "11", "name": "Existing variable", "type": "c"},
            "folders": {"folderId": "12", "name": "Existing folder"},
            "built_in_variables": {"type": "pagePath", "name": "Page Path"},
            "zones": {"zoneId": "13", "name": "Existing zone"},
            "clients": {"clientId": "14", "name": "Existing client", "type": "test"},
            "gtag_config": {"gtagConfigId": "15", "type": "test"},
            "transformations": {"transformationId": "16", "name": "Existing transformation", "type": "test"},
        }
        self.api.container["features"] = dict.fromkeys(self.api.container["features"], True)
        self.api.extra = {kind: [entity] for kind, entity in samples.items()}
        self.api.pages = True
        self.apply(["--publish"])
        for kind, entity in samples.items():
            self.assertEqual(self.api.live[self.api.extra_keys[kind]], [entity])
            self.assertTrue(any("/" + kind + "?pageToken=" in path for path, _, _ in self.api.requests))
        self.assertEqual(self.api.live["container"], self.api.container)

    def test_unavailable_required_inventory_fails_before_writes(self):
        def dispatch(token, path, method="GET", body=None):
            if path.endswith("/variables"):
                raise SystemExit("Mock variables unavailable")
            return self.api(token, path, method, body)
        with self.assertRaisesRegex(SystemExit, "variables unavailable"):
            self.run_cli(dispatch=dispatch)
        self.assertEqual(self.api.writes, [])

    def test_changed_variable_invalidates_plan_approval(self):
        self.api.extra["variables"] = [{"variableId": "11", "name": "Existing variable", "type": "c"}]
        approval = self.approve()
        self.api.extra["variables"][0]["parameter"] = [{"key": "value", "type": "template", "value": "changed"}]
        with self.assertRaisesRegex(SystemExit, "changed plan"):
            self.run_cli(["--apply", "--approve-plan", approval])
        self.assertEqual(self.api.writes, [])

    def test_updates_and_publication_use_server_fingerprints(self):
        original = self.api.tags[0]["fingerprint"]
        output = self.apply(["--publish"])
        update = next(path for path, method, _ in self.api.writes if method == "PUT")
        publication = next(path for path, _, _ in self.api.writes if ":publish" in path)
        self.assertEqual(urllib.parse.parse_qs(urllib.parse.urlsplit(update).query), {"fingerprint": [original]})
        self.assertEqual(urllib.parse.parse_qs(urllib.parse.urlsplit(publication).query), {"fingerprint": ["version-9"]})
        self.assertIn("confirmed live", output)

    def test_concurrent_tag_change_stops_before_its_update_or_version(self):
        def dispatch(token, path, method="GET", body=None):
            if method == "GET" and path.endswith("/tags/1"):
                self.api.tags[0]["fingerprint"] = "concurrent-change"
            return self.api(token, path, method, body)
        with self.assertRaisesRegex(SystemExit, "Tag changed"):
            self.apply(dispatch=dispatch)
        self.assertFalse(any(method == "PUT" for _, method, _ in self.api.writes))
        self.assertFalse(self.has_write(":create_version"))

    def test_created_trigger_response_must_match_the_plan(self):
        def dispatch(token, path, method="GET", body=None):
            response = self.api(token, path, method, body)
            if method == "POST" and path.endswith("/triggers"):
                response["name"] = "Changed event"
                response["customEventFilter"][0]["parameter"][1]["value"] = "purchase"
                self.api.triggers[-1] = copy.deepcopy(response)
            return response
        with self.assertRaisesRegex(SystemExit, "Consent trigger response differs"):
            self.apply(dispatch=dispatch)
        self.assertFalse(self.has_write(":create_version"))
        self.assertFalse(any("/tags/1" in path and method == "PUT" for path, method, _ in self.api.writes))

    def test_created_trigger_rejects_extra_unplanned_fields(self):
        def dispatch(token, path, method="GET", body=None):
            response = self.api(token, path, method, body)
            if method == "POST" and path.endswith("/triggers"):
                response["limit"] = {"type": "template", "value": "5"}
                self.api.triggers[-1] = copy.deepcopy(response)
            return response
        with self.assertRaisesRegex(SystemExit, "Consent trigger response differs"):
            self.apply(dispatch=dispatch)
        self.assertFalse(self.has_write(":create_version"))

    def test_created_initialization_rejects_unplanned_firing_conditions(self):
        def dispatch(token, path, method="GET", body=None):
            response = self.api(token, path, method, body)
            if method == "POST" and path.endswith("/tags"):
                response["blockingTriggerId"] = ["99"]
                self.api.tags[-1] = copy.deepcopy(response)
            return response
        with self.assertRaisesRegex(SystemExit, "Initialization tag response differs"):
            self.apply(dispatch=dispatch)
        self.assertFalse(self.has_write("/triggers"))
        self.assertFalse(self.has_write(":create_version"))

    def test_created_initialization_rejects_duplicate_identity(self):
        def dispatch(token, path, method="GET", body=None):
            response = self.api(token, path, method, body)
            if method == "POST" and path.endswith("/tags"):
                response["tagId"] = "1"
            return response
        with self.assertRaisesRegex(SystemExit, "no identity"):
            self.apply(dispatch=dispatch)
        self.assertFalse(self.has_write(":create_version"))

    def test_workspace_readback_blocks_partial_or_changed_state(self):
        def dispatch(token, path, method="GET", body=None):
            response = self.api(token, path, method, body)
            if method == "PUT":
                self.api.tags[0]["consentSettings"] = {"consentStatus": "notSet"}
            return response
        with self.assertRaisesRegex(SystemExit, "Workspace readback"):
            self.apply(dispatch=dispatch)
        self.assertFalse(self.has_write(":create_version"))

    def test_new_unrelated_workspace_change_blocks_version(self):
        def dispatch(token, path, method="GET", body=None):
            response = self.api(token, path, method, body)
            if method == "PUT":
                self.api.status.setdefault("workspaceChange", []).append(
                    {"changeStatus": "updated", "variable": {"variableId": "99", "name": "Unreviewed"}})
            return response
        with self.assertRaisesRegex(SystemExit, "outside this plan"):
            self.apply(dispatch=dispatch)
        self.assertFalse(self.has_write(":create_version"))

    def test_merge_conflict_fails_before_writes(self):
        self.api.status = {"mergeConflict": [{"entityInBaseVersion": {}}]}
        with self.assertRaisesRegex(SystemExit, "merge conflicts"):
            self.apply()
        self.assertEqual(self.api.writes, [])

    def test_malformed_workspace_status_fails_before_writes(self):
        for status in ([], {"workspaceChange": {}}, {"workspaceChange": [None]},
                       {"workspaceChange": [{"changeStatus": "updated"}]}):
            with self.subTest(status=status):
                self.api.status = status
                with self.assertRaises(SystemExit):
                    self.apply()
                self.assertEqual(self.api.writes, [])

    def test_version_readback_blocks_publication(self):
        def dispatch(token, path, method="GET", body=None):
            response = self.api(token, path, method, body)
            if method == "GET" and "/versions/" in path:
                response["tag"][0]["firingTriggerId"] = [self.wire.TRIGGER_ALL_PAGES]
            return response
        with self.assertRaisesRegex(SystemExit, "Version readback"):
            self.apply(["--publish"], dispatch=dispatch)
        self.assertFalse(self.has_write(":publish"))

    def test_unapproved_version_entities_block_publication_for_every_collection(self):
        samples = {
            "variable": {"variableId": "99", "name": "Unapproved variable"},
            "folder": {"folderId": "99", "name": "Unapproved folder"},
            "builtInVariable": {"type": "pagePath", "name": "Page Path"},
            "zone": {"zoneId": "99", "name": "Unapproved zone"},
            "client": {"clientId": "99", "name": "Unapproved client"},
            "gtagConfig": {"gtagConfigId": "99", "type": "test"},
            "transformation": {"transformationId": "99", "name": "Unapproved transformation"},
        }
        for key, entity in samples.items():
            with self.subTest(collection=key):
                self.api = FakeAPI(self.wire.template_support)
                self.api.templates = [self.api.template()]
                def dispatch(token, path, method="GET", body=None):
                    response = self.api(token, path, method, body)
                    if method == "POST" and path.endswith(":create_version"):
                        version = self.api.versions[response["containerVersion"]["containerVersionId"]]
                        version[key] = [entity]
                    return response
                with self.assertRaisesRegex(SystemExit, "Version readback"):
                    self.apply(["--publish"], dispatch=dispatch)
                self.assertFalse(self.has_write(":publish"))

    def test_unknown_version_collection_blocks_publication(self):
        def dispatch(token, path, method="GET", body=None):
            response = self.api(token, path, method, body)
            if method == "GET" and "/versions/" in path:
                response["futureEntity"] = [{"id": "99"}]
            return response
        with self.assertRaisesRegex(SystemExit, "unrecognized fields or collections"):
            self.apply(["--publish"], dispatch=dispatch)
        self.assertFalse(self.has_write(":publish"))

    def test_changed_version_container_blocks_publication(self):
        def dispatch(token, path, method="GET", body=None):
            response = self.api(token, path, method, body)
            if method == "GET" and "/versions/" in path:
                response["container"]["domainName"] = ["unapproved.example"]
            return response
        with self.assertRaisesRegex(SystemExit, "container differs"):
            self.apply(["--publish"], dispatch=dispatch)
        self.assertFalse(self.has_write(":publish"))

    def test_version_fingerprint_change_blocks_publication(self):
        count = 0
        def dispatch(token, path, method="GET", body=None):
            nonlocal count
            response = self.api(token, path, method, body)
            if method == "GET" and "/versions/" in path:
                count += 1
                if count > 1:
                    response["fingerprint"] = "changed-version"
            return response
        with self.assertRaisesRegex(SystemExit, "fingerprint changed"):
            self.apply(["--publish"], dispatch=dispatch)
        self.assertFalse(self.has_write(":publish"))

    def test_version_readback_requires_requested_identity(self):
        def dispatch(token, path, method="GET", body=None):
            response = self.api(token, path, method, body)
            if method == "GET" and "/versions/" in path:
                response["containerVersionId"] = "999"
            return response
        with self.assertRaisesRegex(SystemExit, "identity differs"):
            self.apply(["--publish"], dispatch=dispatch)
        self.assertFalse(self.has_write(":publish"))

    def test_failed_update_does_not_create_version(self):
        def dispatch(token, path, method="GET", body=None):
            if method == "PUT":
                raise SystemExit("Mock write failure")
            return self.api(token, path, method, body)
        with self.assertRaisesRegex(SystemExit, "Mock write failure"):
            self.apply(dispatch=dispatch)
        self.assertFalse(self.has_write(":create_version"))

    def test_live_version_must_match_after_publication(self):
        def dispatch(token, path, method="GET", body=None):
            response = self.api(token, path, method, body)
            if path.endswith("/versions:live"):
                response["containerVersionId"] = "different-live-version"
            return response
        with self.assertRaisesRegex(SystemExit, "Live version does not match"):
            self.apply(["--publish"], dispatch=dispatch)
        self.assertTrue(self.has_write(":publish"))


if __name__ == "__main__":
    unittest.main()
