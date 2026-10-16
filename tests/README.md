# Local verification

Run from the repository root, using only Python's standard library:

```bash
python3 -B -m unittest discover -s tests -p 'test_*.py' -v
python3 -B tests/mutation-controls.py
```

`test_authorise.py` tests the OAuth entry point without a real browser, socket,
credential or Google request. It verifies the default dry run, state binding,
PKCE S256 against the RFC example, callback validation and listener cleanup,
exact granted scopes before persistence, private atomic token replacement,
preservation of an existing token after failure, and rejection of token-endpoint
redirects. These checks do not establish that a live Google account has granted
access. The protocol follows [Google's installed-app OAuth documentation](https://developers.google.com/identity/protocols/oauth2/native-app)
and [PKCE's S256 example](https://www.rfc-editor.org/rfc/rfc7636#appendix-B).

`test_skill_packages.py` validates the generated client skill packages, their
bundled references and scripts, and command help without authorising an account.
It runs through the same test discovery command above.
The same file verifies catalogue drift detection and rejects duplicate tool names
that could otherwise hide a changed MCP contract.

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
Current runtime cases also verify attributes on the core script itself, the expected
project ID, agreement between the script URL and site-ID attribute, duplicate runtimes,
and image trackers using plural category attributes without an active `src`.

`test_wire_safety.py` exercises writer behavior using a fake GTM API. It covers
trigger identity and ambiguity, preservation of business-event triggers, complete
category maps, multi-region preservation, reviewed plan hashes, concurrent changes,
fingerprint checks, workspace/version readback and partial failures. It requires
unsafe or changed inputs to stop before the relevant write or publication step.
Publication assertions inspect a simulated API response, never a live container.

`mutation-controls.py` makes temporary copies and removes or changes selected
controls. Coverage includes simulation, Gallery identity and content, pagination,
initialization-template linkage, resource parsing and the writer's safety gates.
Each mutation must fail its targeted test with an assertion failure. A missing or
ambiguous mutation target is an error, not a passing control. The working files
stay unchanged. Use the command output for the current mutation count rather than
assuming that a historical count still describes the suite.

`test_skill_packages.py` also exercises the catalogue and repository checker CLI
exit statuses. Broken local links, changed contracts and duplicate tool names must
be distinguishable from a successful check.

The [CI workflow](../.github/workflows/checks.yml) runs the offline unit/package
suite, mutation controls, documentation checks, archive verification and asset
collector tests. It does not run the optional native client check below.

These tests use no credentials and make no live GTM writes. The captured import reached
Google, but these local tests do not prove a completed live configuration, publication, or
consent behaviour in a browser.

## Optional native client smoke check

This check is separate from the offline suite and is not a CI prerequisite. It
requires the Codex CLI and Git on the local machine.

| Script | Operation and flag | Repetition and rollback |
|---|---|---|
| `client-smoke.py` | READS local sources and the native Codex `skills/list` API. With `--run`, creates packages and an empty Git project in a temporary directory, then checks skill discovery. The default only prints instructions. No model request or business tool is called. | Safe to repeat. Removes the temporary project and stops its app-server process. Does not modify existing agent configuration or installed skills. |

```bash
python3 -B tests/client-smoke.py --run
```

Native discovery confirms that Codex can find the generated skill packages outside
this checkout. It does not validate a Google or Consent Pro authorisation, tool
permissions, business operations, or every other AI client.

## Coverage and final local checks

Coverage is optional development tooling, not a runtime dependency. With `uv` available:

```bash
uv run --with coverage python -m coverage run --data-file /tmp/consent-pro-coverage --source=scripts -m unittest discover -s tests -p 'test_*.py'
uv run --with coverage python -m coverage report --data-file /tmp/consent-pro-coverage
python3 -B scripts/check-repository.py
python3 -B docs/06-agent-readiness/checks/verify-snapshot.py --self-check
python3 -B docs/06-agent-readiness/tools/test-asset-headers.py
python3 -B docs/06-agent-readiness/tools/test-asset-collector.py
```

The coverage commands write only the chosen local coverage file. Delete it to
remove the report data. Measured release evidence and remaining live acceptance
work are recorded in [agent readiness](../docs/06-agent-readiness/README.md).
