# Local analysis checks

These tools support the [agent readiness analysis](../README.md). They do not
configure a real site, authorise an account or publish changes.

| File | Operation | Command | Repetition and rollback |
|---|---|---|---|
| `reproduce-writer.py` | Reads the current writer and local safety tests; runs six selected regressions against the fake API with network and sockets blocked. Test files are temporary. | `python3 -B docs/06-agent-readiness/checks/reproduce-writer.py .` | Safe to repeat. Temporary files are removed. Exit status zero requires passing safety expectations, not reproducing a known bug. |
| `writer-results.json` | Historical observations captured from baseline `d33d2e06bfa07b5dd2fda4d8d9e3ad7962b8899b`, with field names translated to English. | Reference only. | Records unsafe pre-fix behavior. It is not a passing regression result or an approval of current configuration. |
| `writer-regression-results.json` | Captured output from the current safety regression command, with source hashes. | Re-run `reproduce-writer.py` and compare the source hashes before relying on this capture. | Describes offline fake-API results only. A source change makes the capture historical. |
| `verify-snapshot.py` | Reads an explicitly selected private archive, compares sitemap/pages/links and checks asset sizes, hashes and PNG signatures. | `python3 -B docs/06-agent-readiness/checks/verify-snapshot.py --root /path/to/private/archive --self-check` | No writes or network access. Negative controls remove a page/reference or alter response metadata/hash only in memory and must be rejected. |

The current writer regressions require a same-name wrong-event trigger to stop
before writes, a verified trigger to be reused, a business-event trigger to be
preserved with consent checks, existing regional defaults to be preserved, and
explicit replacement of a multi-region configuration to stop before writes.
The single-region control verifies that unrelated initialization settings remain.

Passing these tests does not prove live GTM publication, browser consent behavior
or legal compliance. The archive checks establish the documented scope and
local integrity, not the correctness of every statement in the source material.

## Private evidence and portable tests

The original source collection is preserved outside the repository. CI exercises
the same verifier with synthetic pages, a sitemap, assets and a tool catalogue in
`tests/test_source_archive.py`. Missing pages, changed assets and path escapes must
fail. `tests/test_public_boundary.py` rejects accidental raw-evidence reintroduction.
These tests need neither the private archive nor authenticated documentation.
The verifier requires an explicit archive location and does not guess a local path.
