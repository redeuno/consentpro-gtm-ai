# Local verification

Run from the repository root, using only Python's standard library:

```bash
python -X utf8 -m unittest discover -s tests -v
python -X utf8 tests/mutation-controls.py
```

`test_gallery_install.py` runs the writer and auditor entry points against a fake API. It
covers simulation, a new gallery import, preservation of a manual template, pagination,
identity conflicts, invalid import responses and the existing account and publish guards.

The template fixture is synthetic. Each test replaces the expected content hash with that
fixture's hash, so the suite checks whether content changes are rejected without storing the
official template. It does not validate the production hash against Google's live response.
That hash must be checked separately against the pinned public template when it changes.

`test_inspect_site.py` supplies public HTML fixtures to the inspector entry point. It checks
normal and self-hosted Consent Pro scripts, their position in the HTML, and earlier trackers,
including resources on the same host or a host containing `consentpro`. It makes no requests
and does not simulate browser loading. Comments and escaped examples must not count as resource
elements. Invalid resource URLs must not abort inspection or hide a real earlier tracker.

`mutation-controls.py` makes temporary copies and removes ten controls: simulation, gallery
owner validation, manual content validation, ambiguity detection, template pagination and the
initialization tag's link to the verified template, the consent script's element position and
the inclusion of earlier resources on a host containing `consentpro`, resource element parsing,
and invalid URL handling. Each mutation must fail its targeted test
with an assertion failure. The working files stay unchanged.

These tests use no credentials and make no live GTM writes. They do not prove a successful
gallery installation in Google, publication, or consent behaviour in a browser.
