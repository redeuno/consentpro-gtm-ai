# Script catalogue

Run scripts from a reviewed checkout with Python 3.10 or newer. All use the standard
library. Keep tokens and customer maps outside the repository. Read
[security](../SECURITY.md) and the [run guide](../docs/04-run-it.md) first.

| Script | System and effect | Apply flag | Repeat and recovery |
| --- | --- | --- | --- |
| `inspect-site.py` | Reads public site HTML | None, read only | Safe to repeat; no browser behavior proof |
| `authorise.py` | Requests Google OAuth and saves a local refresh token | `--apply`; `--write` requests broader scopes | Starts a new authorization; preserve old token on error, revoke grants in Google account settings |
| `audit-container.py` | Reads Google GTM account and workspace | None, read only; report output is explicit | Safe to repeat; delete optional local report to remove it |
| `wire-consent.py` | Reads GTM; applies approved configuration and creates a version | `--apply` plus approved plan; `--publish` is separate | Re-simulate against current state; inspect partial writes before retry; restore reviewed prior configuration through GTM |
| `consent-template.py` | Shared local template identity and pinned-content checks | No executable write path | Safe to import; no automatic template upgrade |
| `package-skills.py` | Reads an explicit list of local runtime files and Git provenance; creates self-contained skill folders, optional versioned ZIPs and checksums | `--apply`; `--archives DIR` includes ZIPs; `--channel preview` requires a clean source commit | Identical output is unchanged; different files, extra installed files and symbolic destinations are refused. Build into fresh directories for an upgrade. Remove only generated folders and archives to undo |
| `check-mcp-catalogue.py` | Compares local tool schemas, annotations and descriptions | None, read only | Safe to repeat; exit 1 requests review, never activates tools |
| `check-repository.py` | Checks local guide links and authored punctuation | None, read only | Safe to repeat; source content remains untouched |

Public documentation asset collection has its own
[catalogue](../docs/06-agent-readiness/tools/README.md). The
[snapshot checks](../docs/06-agent-readiness/checks/README.md) read explicitly selected local evidence.

## Package builds

Customers use the supplied artifact or the [installation route](../docs/07-agent-installation/README.md).
These commands are for maintainers. The builder never publishes artifacts or updates
a hosted plugin, connector or installed account.

Preview a development build, then write folders and archives explicitly:

```bash
python3 -B scripts/package-skills.py --output dist/skills --archives dist
python3 -B scripts/package-skills.py --output dist/skills --archives dist --apply
```

The default `development` channel accepts work in progress and records its base
commit, `dirty` state and source-content hash. Its filenames end in
`-0.2.0-development.zip`. This is not a claim that the base commit contains every
packaged change. An unversioned copy records a null commit and a dirty source.

The tracked `package-release.json` selects version `0.2.0` and intended release
channel `preview`. From the final clean commit, use fresh output directories:

```bash
python3 -B scripts/package-skills.py --output dist/preview/skills --archives dist/preview --channel preview
python3 -B scripts/package-skills.py --output dist/preview/skills --archives dist/preview --channel preview --apply
```

This creates `consent-pro-0.2.0-preview.zip`, `consent-pro-gtm-0.2.0-preview.zip`
and `SHA256SUMS`. Each ZIP contains its named skill folder. Fixed entry order,
timestamps, file modes and uncompressed storage make its bytes reproducible from
the same source and channel. Storage uses more space than compression, avoiding
compression-library differences between machines.

Tracked `.gitattributes` keeps bundled text and build inputs in LF format,
including checkouts with `core.autocrlf=true`. The package allowlist uses POSIX
paths on every platform. Output paths are normalized before checking that archives
cannot be placed inside an installed skill; symbolic destinations remain refused.
The boundary conservatively treats case changes, equivalent Unicode spellings and
trailing dots or spaces as aliases on every platform, including case-sensitive
filesystems. Choose a separate release directory instead of an alias of a skill.

The manifest identifies version, channel, exact source commit, dirty state,
source-content hash and each packaged file's SHA-256. A preview or stable build
requires a clean checkout and compares every included source, builder, release
configuration and line-ending attributes against the recorded commit. The requested
release channel must match the tracked configuration. This establishes provenance, not successful
installation or behavior in every client.

The source list is explicit. Private archives, readiness research, customer data,
test fixtures and newly added guide files are not implicitly included. Required
local links must target bundled files. The approved informational references to
maintainer readiness, tests and this catalogue become plain text in the package;
unknown dependencies, escaping paths and mutable repository links fail the build.
Keep essential operating instructions in the bundled guides. Regenerate packages
after changing canonical sources and test the actual resulting ZIPs before release.
