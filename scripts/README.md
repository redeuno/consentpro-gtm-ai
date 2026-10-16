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
| `package-skills.py` | Reads this checkout and creates self-contained local skill folders | `--apply` | Identical packages are unchanged; different existing output is refused. Remove only a reviewed generated folder to uninstall |
| `check-mcp-catalogue.py` | Compares local tool schemas, annotations and descriptions | None, read only | Safe to repeat; exit 1 requests review, never activates tools |
| `check-repository.py` | Checks local guide links and authored punctuation | None, read only | Safe to repeat; source content remains untouched |

Public documentation asset collection has its own
[catalogue](../docs/06-agent-readiness/tools/README.md). The
[snapshot checks](../docs/06-agent-readiness/checks/README.md) read local evidence.
