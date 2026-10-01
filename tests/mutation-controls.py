"""Confirma que os testes recusam controles removidos em cópias temporárias."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
MUTATIONS = [
    ("dry-run", "wire-consent.py", "elif a.apply:\n        imported =", "elif True:\n        imported =",
     "test_dry_run_never_writes"),
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
    ("consent-script-position", "inspect-site.py", "return label, trail, position", "return label, trail, position + len(src)",
     "test_inspect_site.InspectSiteTests.test_self_hosted_consent_script_does_not_precede_itself"),
    ("consent-host-exemption", "inspect-site.py", "host = parsed.hostname", 'host = parsed.hostname\n                if host and "consentpro" in host:\n                    continue',
     "test_inspect_site.InspectSiteTests.test_tracker_on_consentpro_named_host_is_not_exempt"),
    ("resource-elements", "inspect-site.py", "for position, src in elements.resources:",
     'for position, src in [(match.start(), match.group(1)) for match in re.finditer(r\'src="([^"]+)"\', html)]:',
     "test_inspect_site.InspectSiteTests.test_escaped_example_before_real_runtime_is_not_a_resource"),
    ("invalid-resource-url", "inspect-site.py", "except ValueError:\n        return None", "except ValueError:\n        raise",
     "test_inspect_site.InspectSiteTests.test_invalid_resource_url_does_not_abort_or_hide_real_tracker"),
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
    if survivors:
        raise SystemExit("Mutations survived: " + ", ".join(survivors))


if __name__ == "__main__":
    main()
