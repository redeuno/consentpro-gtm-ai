"""Verify that tests reject removed safety controls in temporary repository copies."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
MUTATIONS = [
    ("dry-run", "wire-consent.py", "if not a.apply:\n        return 0", "if False:\n        return 0",
     "test_dry_run_never_writes"),
    ("trigger-event", "wire-consent.py", 'if trigger.get("name") == TRIGGER_NAME and not valid:', "if False:",
     "test_wire_safety.WireSafetyTests.test_wrong_named_trigger_fails_before_writes"),
    ("business-event", "wire-consent.py", "desired = entity_body(tag)",
     'desired = entity_body(tag)\n        desired["firingTriggerId"] = [tid]',
     "test_wire_safety.WireSafetyTests.test_business_event_keeps_trigger_and_gains_consent_checks"),
    ("page-lifecycle", "wire-consent.py",
     "or not all(business_trigger(known_triggers[identifier]) for identifier in original_triggers)", "or False",
     "test_wire_safety.WireSafetyTests.test_page_lifecycle_and_unknown_triggers_fail_before_writes"),
    ("web-container-only", "wire-consent.py", 'if container.get("usageContext") != ["web"]:', "if False:",
     "test_wire_safety.WireSafetyTests.test_non_web_container_fails_before_writes"),
    ("regional-preservation", "wire-consent.py", "if not init or banner is not None or regions is not None:", "if True:",
     "test_wire_safety.WireSafetyTests.test_multiregion_and_optional_parameters_are_preserved"),
    ("regional-replacement", "wire-consent.py", "if len(rows) > 1 and (banner is not None or regions is not None):", "if False:",
     "test_wire_safety.WireSafetyTests.test_explicit_multiregion_replacement_fails_before_writes"),
    ("map-completeness", "wire-consent.py", "if set(mapping) != set(names):",
     'mapping.update({name: "skip" for name in names if name not in mapping})\n    if set(mapping) != set(names):',
     "test_wire_safety.WireSafetyTests.test_unmapped_tags_cannot_be_silently_skipped"),
    ("plan-approval", "wire-consent.py", "if a.apply and a.approve_plan != approval:", "if False:",
     "test_wire_safety.WireSafetyTests.test_apply_requires_approval_hash"),
    ("created-trigger-response", "wire-consent.py",
     'if consent_trigger([trg]) is None or entity_body(trg) != dict(trigger_body, triggerId=trg["triggerId"]):', "if False:",
     "test_wire_safety.WireSafetyTests.test_created_trigger_response_must_match_the_plan"),
    ("created-init-response", "wire-consent.py", 'if entity_body(updated) != dict(init_body, tagId=updated["tagId"]):', "if False:",
     "test_wire_safety.WireSafetyTests.test_created_initialization_rejects_unplanned_firing_conditions"),
    ("workspace-readback", "wire-consent.py",
     'if normalized_state(actual) != normalized_state(expected):\n        raise SystemExit("Workspace readback',
     'if False:\n        raise SystemExit("Workspace readback',
     "test_wire_safety.WireSafetyTests.test_workspace_readback_blocks_partial_or_changed_state"),
    ("workspace-unrelated-change", "wire-consent.py",
     "if {k: v for k, v in old.items() if k not in written} != {k: v for k, v in new.items() if k not in written}:", "if False:",
     "test_wire_safety.WireSafetyTests.test_new_unrelated_workspace_change_blocks_version"),
    ("version-readback", "wire-consent.py",
     'if normalized_state(actual) != normalized_state(expected):\n        raise SystemExit("Version readback',
     'if False:\n        raise SystemExit("Version readback',
     "test_wire_safety.WireSafetyTests.test_version_readback_blocks_publication"),
    ("version-variable-inventory", "wire-consent.py",
     'actual = {kind: version.get(key, []) for kind, (key, _) in STATE_KEYS.items()}',
     'actual = {kind: version.get(key, []) for kind, (key, _) in STATE_KEYS.items()}\n    actual["variables"] = expected["variables"]',
     "test_wire_safety.WireSafetyTests.test_unapproved_version_entities_block_publication_for_every_collection"),
    ("version-container", "wire-consent.py", 'container_body(version.get("container")) != container_body(container)', "False",
     "test_wire_safety.WireSafetyTests.test_changed_version_container_blocks_publication"),
    ("version-unknown-collection", "wire-consent.py", "if set(version) - allowed:", "if False:",
     "test_wire_safety.WireSafetyTests.test_unknown_version_collection_blocks_publication"),
    ("version-fingerprint", "wire-consent.py", 'if fresh.get("fingerprint") != saved.get("fingerprint"):', "if False:",
     "test_wire_safety.WireSafetyTests.test_version_fingerprint_change_blocks_publication"),
    ("live-version", "wire-consent.py", 'if published.get("containerVersionId") != vid:', "if False:",
     "test_wire_safety.WireSafetyTests.test_live_version_must_match_after_publication"),
    ("gallery-owner", "consent-template.py", 'gallery.get("owner") != OWNER', "False",
     "test_wrong_gallery_owner_fails_before_writes"),
    ("manual-content", "consent-template.py", "if content_hash(data) != CONTENT_HASH:", "if False:",
     "test_modified_manual_template_fails_before_writes"),
    ("gallery-import-brand", "consent-template.py", '"github.com_finsweet" if gallery is not None else "finsweet_consent_pro"',
     '"finsweet_consent_pro"', "test_captured_gallery_response_uses_production_hash"),
    ("gallery-brand-without-link", "consent-template.py", 'else "finsweet_consent_pro"',
     'else "github.com_finsweet"', "test_gallery_brand_without_link_is_not_manual"),
    ("gallery-host", "consent-template.py", 'gallery.get("host") != HOST', "False",
     "test_captured_gallery_requires_complete_origin"),
    ("captured-gallery-content", "consent-template.py", "if content_hash(data) != CONTENT_HASH:", "if False:",
     "test_captured_gallery_modified_content_stops"),
    ("gallery-public-tag-type", "consent-template.py", 'if identity["source"] == "gallery":', "if False:",
     "test_captured_gallery_response_uses_production_hash"),
    ("gallery-public-id-link", "consent-template.py", 'gallery.get("galleryTemplateId") != GALLERY_TEMPLATE_ID', "False",
     "test_gallery_public_id_must_match_pinned_info"),
    ("ambiguity", "consent-template.py", "if len(candidates) != 1:", "if False:",
     "test_ambiguity_fails_before_writes"),
    ("pagination", "consent-template.py", "items.extend(batch)", 'items.extend(batch)\n        if key == "template":\n            return items',
     "test_every_inventory_is_paginated_before_writes"),
    ("init-template", "audit-container.py", 'if tag_type and t.get("type") == tag_type', 'if tag_type',
     "test_audit_rejects_unrelated_init_even_with_valid_template"),
    ("audit-trigger-filter", "audit-container.py", 'and not t.get("filter") and not t.get("autoEventFilter")', "and True",
     "test_audit_rejects_inexact_consent_event_conditions"),
    ("consent-script-position", "inspect-site.py", "if position < pos_consent:", "if position <= pos_consent:",
     "test_inspect_site.InspectSiteTests.test_self_hosted_consent_script_does_not_precede_itself"),
    ("consent-host-exemption", "inspect-site.py", "host = parsed.hostname", 'host = parsed.hostname\n                if host and "consentpro" in host:\n                    continue',
     "test_inspect_site.InspectSiteTests.test_tracker_on_consentpro_named_host_is_not_exempt"),
    ("resource-elements", "inspect-site.py", "for position, src in elements.resources:",
     'for position, src in [(match.start(), match.group(1)) for match in re.finditer(r\'src="([^"]+)"\', html)]:',
     "test_inspect_site.InspectSiteTests.test_escaped_example_before_real_runtime_is_not_a_resource"),
    ("invalid-resource-url", "inspect-site.py", "except ValueError:\n        return None", "except ValueError:\n        raise",
     "test_inspect_site.InspectSiteTests.test_invalid_resource_url_does_not_abort_or_hide_real_tracker"),
    ("valueless-image-src", "inspect-site.py", 'img.get("src") or ""', 'img.get("src", "")',
     "test_inspect_site.InspectSiteTests.test_valueless_or_empty_image_src_does_not_hide_a_tracker"),
]


def main():
    survivors = []
    for name, filename, before, after, test in MUTATIONS:
        with tempfile.TemporaryDirectory(prefix="consent-gallery-mutation-") as directory:
            target = Path(directory)
            shutil.copytree(ROOT / "scripts", target / "scripts", ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copytree(ROOT / "tests", target / "tests", ignore=shutil.ignore_patterns("__pycache__"))
            path = target / "scripts" / filename
            source = path.read_text(encoding="utf-8")
            if source.count(before) != 1:
                raise SystemExit("Mutation target is no longer unique: " + name)
            path.write_text(source.replace(before, after, 1), encoding="utf-8")
            test_name = test if "." in test else "test_gallery_install.GalleryInstallTests." + test
            result = subprocess.run([sys.executable, "-X", "utf8", "-m", "unittest", test_name],
                                    cwd=target / "tests", capture_output=True, text=True,
                                    encoding="utf-8", errors="replace", timeout=30)
            caught = result.returncode != 0 and "FAIL:" in result.stderr and "ERROR:" not in result.stderr
            print(name + ": " + ("REJECTED" if caught else "SURVIVED"))
            if not caught:
                survivors.append(name)
                print(result.stderr)
    if survivors:
        raise SystemExit("Mutations survived: " + ", ".join(survivors))


if __name__ == "__main__":
    main()
