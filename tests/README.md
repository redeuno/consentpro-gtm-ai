# Local verification

Run from the repository root, using only Python's standard library:

```bash
python -X utf8 -m unittest discover -s tests -v
python -X utf8 tests/mutation-controls.py
```

`test_gallery_install.py` runs the writer and auditor entry points against a fake API. It
covers simulation, a new gallery import, preservation of a manual template, pagination,
identity conflicts, invalid import responses and the existing account and publish guards.

The original template fixture is synthetic. Those tests replace the expected content hash
with the synthetic hash to exercise the workflow and its guards.

[`fixtures/gallery-import-2026-10-01.json`](fixtures/gallery-import-2026-10-01.json) is a
selected capture from a real GTM Gallery import on 2026-10-01. It retains the template ID,
name, Gallery host/owner/repository/version/ID, the INFO fields used for identity, and the
actual parameters, code and permissions. Account and workspace metadata, signature, image,
descriptive INFO fields and unrelated template sections are omitted. No credential is stored.
The capture showed `INFO.brand.id=github.com_finsweet`, while the public file used for manual
imports has `finsweet_consent_pro`. The first real run imported the template but stopped at
the INFO check before configuring tags or creating a version.
After that check was corrected, the next attempt exposed a second mismatch: a Gallery tag
uses the public type `cvt_WRGND`, not `cvt_{containerId}_{templateId}`. Google rejected the
initialization tag before creating it. The shared helper now requires both the pinned
`galleryTemplateId=WRGND` and `INFO.id=cvt_WRGND`. The fake API rejects the incorrect manual
type for a Gallery template, and the legacy manual test still requires its original type.

The captured-response tests keep the production content hash unchanged. They exercise new
import and reuse through the writer, reject missing or wrong Gallery provenance, reject the
Gallery brand without its link, and reject modified content or a modified flag. The fixture
proves compatibility with that captured response, not future Gallery releases or browser
behaviour. Recheck the pinned template and live response when updating the version.

`test_inspect_site.py` supplies public HTML fixtures to the inspector entry point. It checks
normal and self-hosted Consent Pro scripts, their position in the HTML, and earlier trackers,
including resources on the same host or a host containing `consentpro`. It makes no requests
and does not simulate browser loading. Comments and escaped examples must not count as resource
elements. Invalid resource URLs must not abort inspection or hide a real earlier tracker.

`mutation-controls.py` makes temporary copies and changes sixteen controls: simulation, gallery
owner validation, manual content validation, ambiguity detection, template pagination and the
initialization tag's link to the verified template, the consent script's element position and
the inclusion of earlier resources on a host containing `consentpro`, resource element parsing,
and invalid URL handling. It also restores the rejected pre-fix Gallery brand check, accepts
the Gallery brand without a link, skips the host check and skips content validation against
the captured response. Two further mutations restore the wrong manual tag type for Gallery
templates and remove the pinned Gallery ID check. Each mutation must fail its targeted test
with an assertion failure. The working files stay unchanged.

These tests use no credentials and make no live GTM writes. The captured import reached
Google, but these local tests do not prove a completed live configuration, publication, or
consent behaviour in a browser.
