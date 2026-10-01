import contextlib
import copy
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
import urllib.error
import urllib.parse


ROOT = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def template_data(gallery=False):
    info = {"type": "TAG", "id": "cvt_WRGND" if gallery else "cvt_temp_public_id", "displayName": "Consent Pro - GTM Template",
            "brand": {"id": "github.com_finsweet" if gallery else "finsweet_consent_pro"},
            "containerContexts": ["WEB"]}
    sections = {"INFO": json.dumps(info), "TEMPLATE_PARAMETERS": "[]",
                "SANDBOXED_JS_FOR_WEB_TEMPLATE": "data.gtmOnSuccess();", "WEB_PERMISSIONS": "[]"}
    return "\n\n".join("___%s___\n%s" % pair for pair in sections.items())


class FakeAPI:
    def __init__(self, helper):
        self.helper = helper
        self.templates = []
        self.tags = [{"tagId": "1", "name": "Analytics", "type": "html"}]
        self.triggers = []
        self.writes = []
        self.requests = []
        self.pages = False
        self.import_response = None
        self.repeat_token = False

    def template(self, gallery=True):
        result = {"templateId": "15", "name": self.helper.NAME, "templateData": template_data(gallery)}
        if gallery:
            result["galleryReference"] = {"host": self.helper.HOST, "owner": self.helper.OWNER, "repository": self.helper.REPOSITORY,
                                          "version": self.helper.VERSION, "isModified": False,
                                          "galleryTemplateId": "WRGND"}
        return result

    def __call__(self, token, path, method="GET", body=None):
        self.requests.append((path, method, body))
        parsed = urllib.parse.urlsplit(path)
        resource = parsed.path
        if method != "GET":
            self.writes.append((path, method, body))
            if resource.endswith("/templates:import_from_gallery"):
                result = self.template() if self.import_response is None else self.import_response
                if isinstance(result, dict) and result.get("templateId"):
                    self.templates.append(copy.deepcopy(result))
                return copy.deepcopy(result)
            if resource.endswith("/tags"):
                self.validate_tag_type(body)
                tag = dict(body, tagId="2")
                self.tags.append(tag)
                return tag
            if "/tags/" in resource:
                self.validate_tag_type(body)
                tag = next(tag for tag in self.tags if tag["tagId"] == resource.rsplit("/", 1)[1])
                tag.update(body)
                return tag
            if resource.endswith("/triggers"):
                trigger = dict(body, triggerId="3")
                self.triggers.append(trigger)
                return trigger
            if resource.endswith(":create_version"):
                return {"containerVersion": {"containerVersionId": "9"}}
            if resource.endswith(":publish"):
                return {}
            raise AssertionError((path, method, body))
        if resource == "/accounts/123":
            return {"name": "Lab"}
        objects = {"containers": ("container", [{"containerId": "456", "publicId": "GTM-LAB"}]),
                   "workspaces": ("workspace", [{"workspaceId": "7", "name": "Default"}]),
                   "tags": ("tag", self.tags), "triggers": ("trigger", self.triggers),
                   "templates": ("template", self.templates)}
        key, items = objects[resource.rsplit("/", 1)[1]]
        if self.pages and not parsed.query:
            return {key: [], "nextPageToken": "second page"}
        if self.repeat_token:
            return {key: items, "nextPageToken": "second page"}
        return {key: copy.deepcopy(items)}

    def validate_tag_type(self, tag):
        if str(tag.get("type", "")).startswith("cvt_"):
            valid = {"cvt_" + template["galleryReference"]["galleryTemplateId"]
                     if template.get("galleryReference") else "cvt_456_" + template["templateId"]
                     for template in self.templates}
            if tag["type"] not in valid:
                raise SystemExit("vendorTemplate.key: Unknown entity type")


class GalleryInstallTests(unittest.TestCase):
    def setUp(self):
        self.wire = load("wire-consent")
        self.audit = load("audit-container")
        for module in (self.wire, self.audit):
            module.template_support.CONTENT_HASH = module.template_support.content_hash(template_data())
        self.api = FakeAPI(self.wire.template_support)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.mapping = Path(self.temp.name) / "categories.json"
        self.mapping.write_text('{"Analytics": "analytics"}', encoding="utf-8")

    def run_main(self, apply=False, publish=False, audit=False, confirm="Lab"):
        module = self.audit if audit else self.wire
        args = [module.__file__, "--account", "123", "--container", "GTM-LAB", "--confirm-name", confirm]
        if not audit:
            args += ["--map", str(self.mapping)]
        if apply:
            args += ["--apply"]
        if publish:
            args += ["--publish"]
        output = io.StringIO()
        with mock.patch.object(sys, "argv", args), mock.patch.object(module, "access_token", return_value="fake"), \
                mock.patch.object(module, "read" if audit else "call", self.api), contextlib.redirect_stdout(output):
            module.main()
        return output.getvalue()

    def test_dry_run_never_writes(self):
        output = self.run_main()
        self.assertIn("would import gallery finsweet/gtm-template-consent-pro", output)
        self.assertEqual(self.api.writes, [])

    def test_new_install_pins_gallery_and_requires_separate_publish(self):
        self.run_main(apply=True)
        imports = [entry for entry in self.api.writes if "import_from_gallery" in entry[0]]
        self.assertEqual(len(imports), 1)
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(imports[0][0]).query)
        self.assertEqual(query, {"galleryOwner": ["finsweet"], "galleryRepository": ["gtm-template-consent-pro"],
                                 "gallerySha": [self.wire.template_support.VERSION], "acknowledgePermissions": ["true"]})
        self.assertIsNone(imports[0][2])
        self.assertFalse(any(path.endswith(":publish") for path, _, _ in self.api.writes))
        self.assertEqual(self.api.tags[1]["type"], "cvt_WRGND")
        self.assertEqual(self.api.tags[0]["consentSettings"]["consentStatus"], "needed")

    def test_legacy_is_preserved_and_repeated_run_does_not_duplicate(self):
        original = self.api.template(gallery=False)
        self.api.templates = [copy.deepcopy(original)]
        output = self.run_main(apply=True)
        self.run_main(apply=True)
        self.assertIn("origin and version unverified", output)
        self.assertEqual(self.api.templates, [original])
        self.assertEqual(len(self.api.tags), 2)
        self.assertEqual(self.api.tags[1]["type"], "cvt_456_15")
        self.assertFalse(any("/templates" in path for path, _, _ in self.api.writes))

    def test_renamed_gallery_init_is_reused(self):
        self.api.templates = [self.api.template()]
        self.api.tags += [{"tagId": "2", "name": "Existing consent", "type": "cvt_WRGND"}]
        self.run_main(apply=True)
        self.assertEqual(len(self.api.tags), 2)
        self.assertEqual(self.api.tags[1]["name"], "Existing consent")

    def test_every_inventory_is_paginated_before_writes(self):
        self.api.pages = True
        self.api.templates = [self.api.template()]
        self.run_main(apply=True)
        self.assertFalse(any("/templates" in path for path, _, _ in self.api.writes))
        for resource in ("containers", "workspaces", "tags", "triggers", "templates"):
            self.assertTrue(any("/" + resource + "?pageToken=" in path for path, _, _ in self.api.requests))

    def test_wrong_gallery_owner_fails_before_writes(self):
        self.api.templates = [self.api.template()]
        self.api.templates[0]["galleryReference"]["owner"] = "imposter"
        with self.assertRaisesRegex(SystemExit, "owner or repository"):
            self.run_main(apply=True)
        self.assertEqual(self.api.writes, [])

    def test_wrong_version_and_modified_gallery_fail_before_writes(self):
        for field, value in (("version", "unreviewed"), ("isModified", True)):
            with self.subTest(field=field):
                self.api.templates = [self.api.template()]
                self.api.templates[0]["galleryReference"][field] = value
                with self.assertRaises(SystemExit):
                    self.run_main(apply=True)
                self.assertEqual(self.api.writes, [])

    def test_ambiguity_fails_before_writes(self):
        self.api.templates = [self.api.template(), self.api.template(gallery=False)]
        self.api.templates[1]["templateId"] = "16"
        with self.assertRaisesRegex(SystemExit, "Multiple Consent Pro"):
            self.run_main(apply=True)
        self.assertEqual(self.api.writes, [])

    def test_modified_manual_template_fails_before_writes(self):
        self.api.templates = [self.api.template(gallery=False)]
        self.api.templates[0]["templateData"] = template_data().replace("gtmOnSuccess", "gtmOnFailure")
        with self.assertRaisesRegex(SystemExit, "differ"):
            self.run_main(apply=True)
        self.assertEqual(self.api.writes, [])

    def test_invalid_import_response_stops_before_tags_or_versions(self):
        for response in ({}, [], {"templateId": "15", "name": self.wire.TEMPLATE_NAME}):
            with self.subTest(response=response):
                self.api = FakeAPI(self.wire.template_support)
                self.api.import_response = response
                with self.assertRaises(SystemExit):
                    self.run_main(apply=True)
                self.assertEqual(len(self.api.writes), 1)
                self.assertIn("import_from_gallery", self.api.writes[0][0])

    def test_wrong_account_and_publish_guard_prevent_writes(self):
        with self.assertRaises(SystemExit):
            self.run_main(apply=True, confirm="Production")
        with self.assertRaises(SystemExit):
            self.run_main(publish=True)
        self.assertEqual(self.api.writes, [])

    def test_explicit_publish_is_separate(self):
        self.run_main(apply=True, publish=True)
        self.assertTrue(self.api.writes[-1][0].endswith(":publish"))

    def test_unknown_template_referenced_by_init_prevents_writes(self):
        self.api.tags += [{"tagId": "2", "name": self.wire.INIT_TAG_NAME, "type": "cvt_456_999"}]
        with self.assertRaisesRegex(SystemExit, "unverified template"):
            self.run_main(apply=True)
        self.assertEqual(self.api.writes, [])

    def test_audit_does_not_accept_generic_consent_or_unrelated_init(self):
        self.api.templates = [{"templateId": "99", "name": "Other consent manager", "templateData": "consent"}]
        self.api.tags += [{"tagId": "2", "name": "Other", "type": "cvt_456_99",
                          "firingTriggerId": [self.audit.TRIGGER_CONSENT_INIT]}]
        output = self.run_main(audit=True)
        self.assertIn("TEMPLATE SOURCE: missing", output)
        self.assertIn("no verified Consent Pro tag", output)
        self.assertEqual(self.api.writes, [])

    def test_audit_identifies_gallery_and_links_init(self):
        self.run_main(apply=True)
        self.api.writes.clear()
        output = self.run_main(audit=True)
        self.assertIn("source=gallery", output)
        self.assertIn("version=" + self.wire.template_support.VERSION, output)
        self.assertIn("5 of 5 configuration signals", output)
        self.assertEqual(self.api.writes, [])

    def test_audit_rejects_unrelated_init_even_with_valid_template(self):
        self.api.templates = [self.api.template()]
        self.api.tags += [{"tagId": "2", "name": "Other", "type": "cvt_456_99",
                          "firingTriggerId": [self.audit.TRIGGER_CONSENT_INIT]}]
        output = self.run_main(audit=True)
        self.assertIn("source=gallery", output)
        self.assertIn("no verified Consent Pro tag", output)

    def test_import_wrong_workspace_stops_before_tag_writes(self):
        self.api.import_response = dict(self.api.template(), containerId="999")
        with self.assertRaisesRegex(SystemExit, "different workspace"):
            self.run_main(apply=True)
        self.assertEqual(len(self.api.writes), 1)

    def test_repeated_pagination_token_stops(self):
        self.api.repeat_token = True
        with self.assertRaisesRegex(SystemExit, "repeated page token"):
            self.run_main(apply=True)
        self.assertEqual(self.api.writes, [])

    def test_write_server_error_is_not_retried(self):
        error = urllib.error.HTTPError("https://example.test", 500, "failure", {}, io.BytesIO(b"failed"))
        with mock.patch.object(self.wire.urllib.request, "urlopen", side_effect=error) as request:
            with self.assertRaises(SystemExit):
                self.wire.call("fake", "/templates:import_from_gallery", "POST")
        self.assertEqual(request.call_count, 1)

    def captured_template(self):
        template = json.loads((ROOT / "tests" / "fixtures" / "gallery-import-2026-10-01.json").read_text(encoding="utf-8"))
        expected = load("consent-template").CONTENT_HASH
        for module in (self.wire, self.audit):
            module.template_support.CONTENT_HASH = expected
        return template

    def test_captured_gallery_response_uses_production_hash(self):
        template = self.captured_template()
        helper = self.wire.template_support
        self.assertEqual(helper.content_hash(template["templateData"]), helper.CONTENT_HASH)
        self.assertEqual(helper.inspect(template)["status"], "verified")
        self.api.import_response = template
        try:
            self.run_main(apply=True)
        except SystemExit as exc:
            self.fail("Captured Gallery response must configure successfully: " + str(exc))
        self.assertEqual(self.api.tags[1]["type"], "cvt_WRGND")
        self.assertTrue(any(path.endswith(":create_version") for path, _, _ in self.api.writes))
        self.assertFalse(any(path.endswith(":publish") for path, _, _ in self.api.writes))

    def test_captured_gallery_can_resume_without_reimport(self):
        self.api.templates = [self.captured_template()]
        self.run_main(apply=True)
        self.assertFalse(any("/templates" in path for path, _, _ in self.api.writes))
        self.api.writes.clear()
        self.assertIn("source=gallery", self.run_main(audit=True))
        self.assertEqual(self.api.writes, [])

    def test_gallery_brand_without_link_is_not_manual(self):
        template = self.captured_template()
        for missing in (True, False):
            with self.subTest(missing=missing):
                unlinked = copy.deepcopy(template)
                if missing:
                    del unlinked["galleryReference"]
                else:
                    unlinked["galleryReference"] = None
                self.api.templates = [unlinked]
                with self.assertRaisesRegex(SystemExit, "INFO identity"):
                    self.run_main(apply=True)
                self.assertEqual(self.api.writes, [])

    def test_captured_gallery_requires_complete_origin(self):
        template = self.captured_template()
        for field in ("host", "owner", "repository", "version"):
            for value in (None, "unexpected"):
                with self.subTest(field=field, value=value):
                    changed = copy.deepcopy(template)
                    if value is None:
                        del changed["galleryReference"][field]
                    else:
                        changed["galleryReference"][field] = value
                    self.api.templates = [changed]
                    with self.assertRaises(SystemExit):
                        self.run_main(apply=True)
                    self.assertEqual(self.api.writes, [])

    def test_captured_gallery_modified_content_stops(self):
        template = self.captured_template()
        for section in ("TEMPLATE_PARAMETERS", "SANDBOXED_JS_FOR_WEB_TEMPLATE", "WEB_PERMISSIONS"):
            with self.subTest(section=section):
                changed = copy.deepcopy(template)
                parts = self.wire.template_support.sections(changed["templateData"])
                parts[section] = "[]" if section != "SANDBOXED_JS_FOR_WEB_TEMPLATE" else "data.gtmOnFailure();"
                changed["templateData"] = "\n\n".join("___%s___\n%s" % pair for pair in parts.items())
                self.api.templates = [changed]
                with self.assertRaisesRegex(SystemExit, "differ"):
                    self.run_main(apply=True)
                self.assertEqual(self.api.writes, [])

    def test_captured_gallery_modified_flag_stops(self):
        template = self.captured_template()
        for value in (True, None, "false", 0):
            with self.subTest(value=value):
                changed = copy.deepcopy(template)
                changed["galleryReference"]["isModified"] = value
                self.api.templates = [changed]
                with self.assertRaisesRegex(SystemExit, "modified"):
                    self.run_main(apply=True)
                self.assertEqual(self.api.writes, [])

    def test_gallery_public_id_must_match_pinned_info(self):
        template = self.captured_template()
        for field in ("galleryTemplateId", "INFO.id", "both"):
            for value in (None, "OTHER"):
                with self.subTest(field=field, value=value):
                    changed = copy.deepcopy(template)
                    if field in ("galleryTemplateId", "both"):
                        changed["galleryReference"]["galleryTemplateId"] = value
                    if field in ("INFO.id", "both"):
                        parts = self.wire.template_support.sections(changed["templateData"])
                        info = json.loads(parts["INFO"])
                        info["id"] = "cvt_" + value if value else None
                        parts["INFO"] = json.dumps(info)
                        changed["templateData"] = "\n\n".join("___%s___\n%s" % pair for pair in parts.items())
                    self.api.templates = [changed]
                    self.assertEqual(self.wire.template_support.inspect(changed)["status"], "blocked")
                    with self.assertRaisesRegex(SystemExit, "public template id"):
                        self.run_main(apply=True)
                    self.assertEqual(self.api.writes, [])

    def test_fake_api_rejects_manual_type_for_gallery_template(self):
        self.api.templates = [self.captured_template()]
        with self.assertRaisesRegex(SystemExit, "Unknown entity type"):
            self.api("fake", "/accounts/123/containers/456/workspaces/7/tags", "POST",
                     {"name": "Consent Pro Init", "type": "cvt_456_5"})


if __name__ == "__main__":
    unittest.main()
