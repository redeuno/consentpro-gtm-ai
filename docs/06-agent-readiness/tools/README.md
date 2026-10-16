# Public source collectors

| Script | Operation and usage | Repetition and rollback |
|---|---|---|
| `collect-assets.py` | READS images and the template referenced by the public scrape JSON files, only from `docs.consentpro.com`. Dry run by default; `--collect` writes local files and `assets-index.json`. Sends no private data and does not modify the service. | Verifies size and SHA-256 before reusing a download. Refuses to replace mismatched or unindexed assets. To undo the collection, remove that date's `assets/` and `assets-index.json`, preserving the source JSON files. |
| `test-asset-headers.py` | Tests the collector's header guards offline. Does not access the network or write files. | Can run repeatedly without changing the snapshot. No rollback needed. |
| `test-asset-collector.py` | Tests recovery from mismatched files, truncated chunked HTTP responses, redirects and exhausted transfer budgets. Uses in-memory HTTP responses and temporary files. | Does not access the network or change the snapshot; removes its temporary files on completion. |

From the repository root:

```bash
python3 docs/06-agent-readiness/tools/collect-assets.py
python3 docs/06-agent-readiness/tools/collect-assets.py --collect
python3 docs/06-agent-readiness/tools/test-asset-headers.py
python3 docs/06-agent-readiness/tools/test-asset-collector.py
```

The index records the URL, local file, size, SHA-256, final URL, content type,
input sources, limits and errors. Repeated runs explicitly update the index and
report how many files were reused. The collector allows at most 80 URLs, 10 MiB
per file and 120 MiB in total. Each request uses a 30-second timeout and at most
one retry after a transient failure. All redirects are rejected, including those
to the same host, and their responses are closed without reading the body.
Importing the module does not access the network or write files.

The index is saved after every success or failure. When a local file differs,
its previous record retains the expected size and SHA-256 with status
`verification_failed`. It does not count as a success, and the file is preserved.
Restoring the original bytes allows reuse on the next run. Previous records that
have not yet been checked receive status `not_checked`. Truncated HTTP responses
are recorded in `failures`; their partial bodies are not saved as assets, and
previous successes remain indexed for recovery.

For truncated responses, the transfer budget conservatively sums partial bodies
across causal exceptions without revisiting an exception or following cycles.
Before every request, retry and read, the collector checks the remaining budget
and limits reads to that amount. At the limit, it stops without another request.
Without `Content-Length`, a response that consumes exactly the limit may be
rejected because its end has not yet been verified.

The collector rejects multiple `Content-Length` headers, even when equal,
multiple `Transfer-Encoding` headers, their combination, and any
`Transfer-Encoding` value other than exactly `chunked`. It does not trim spaces
to accept a value. Headers are checked as exposed by Python's HTTP parser.
These guards were added and tested offline after the 2026-10-16 collection.
The original headers were not archived, so the tests do not retroactively prove
that existing downloads passed these checks. Collected files were verified by
size and SHA-256.

The `.tpl` file is an archived source, not an instruction to install or execute
the template. Operational installation still follows the reviewed version in
this repository.

Return to the [agent readiness study](../README.md).
