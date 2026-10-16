# consentpro-gtm-ai

Help a client's agent install, diagnose and operate Consent Pro, including the
Google Tag Manager configuration that makes tags respect consent.

Start with [the client journey](docs/00-the-journey.md). Install the
[`consent-pro` and `consent-pro-gtm` skills](docs/07-agent-installation/README.md)
for Codex or Claude Code, or follow the guides with a connected web-chat assistant.
The two skills share the same product references and scripts.

## Choose the path available to the customer

| Path | Available work | Requirements |
| --- | --- | --- |
| Consent Pro staging MCP | Read setup, trackers, scans, statistics and published GTM; supported project, scan and draft changes | Finsweet OAuth, correct workspace and tool-specific access |
| Local Google API scripts | Audit and configure a selected web GTM workspace, create a version and optionally publish | Python 3.10+, reviewed Google OAuth scopes, confirmed account/container/workspace and approved simulation |
| Product and GTM interfaces | Guided configuration, Consent Pro publication and tracker categories | Customer access and decisions |
| Site repository and browser | Install the exact project snippet, handle image pixels, preferences and verify behavior | Access to the customer's site and test environment |

The [2026-10-16 staging catalogue](docs/06-agent-readiness/sources/2026-10-16/mcp-catalogue.json)
announces 25 tools, including four GTM read tools. GTM writes through MCP are future
work until a real tool contract is available and tested. Consent Pro publication
and category editing are not exposed in that catalogue. Discover capabilities
again each session; access is not permission to make unsolicited changes.

Staging endpoint: `https://mcp-staging.consentpro.com/mcp`.
Use the dedicated [staging test dashboard](https://mcp-docs-and-ui-consentpro-web-app-staging.finsweet.workers.dev/).
Do not assume production has the same endpoint or capabilities.

## Start safely

1. Install the [skills and connector](docs/07-agent-installation/README.md), or open
   the [manual GTM procedure](docs/reference/nine-steps.md).
2. Identify the workspace, project, public hostname, installed engine and goal.
3. Read the current state. Choose Basic or Advanced Google Consent Mode explicitly.
4. Review exact changes, including tag business events and every regional default.
5. Apply authorized changes, read them back and test behavior.
6. Report saved drafts, GTM versions, publications and site deployment separately.

For public HTML inspection, without credentials:

```bash
python3 scripts/inspect-site.py https://example.com
```

This reports declared runtime, required attributes, site ID, script order and image
tracker candidates. It cannot prove what ran in the browser. Finish with the
[behavior checks](docs/reference/verify-behaviour.md), including rejection,
acceptance as a positive control, partial choice, revocation and reload.

For local GTM automation, follow [Google Cloud setup](docs/01-google-cloud-setup.md),
[GTM account setup](docs/02-tag-manager-account.md), [authorization](docs/03-authorise.md)
and the [run guide](docs/04-run-it.md). This broader credential path is optional;
an MCP read-only restriction does not authorize switching to it.

The GTM [Community Template Gallery](https://tagmanager.google.com/gallery/#/owners/finsweet/templates/gtm-template-consent-pro)
provides the manual template installation. API imports pin the reviewed publisher
version and preserve recognized existing templates. Gallery availability does not
establish Google CMP certification.

## What is covered

- [Operations](docs/06-agent-readiness/operations.md): capability discovery,
  project targeting, installation, scan limits, previews, licenses, logs and recovery.
- [Beyond GTM](docs/05-what-gtm-does-not-cover.md): hardcoded scripts, image pixels,
  preferences and reconciliation with the scan.
- [GTM references](docs/reference/nine-steps.md): regions, categories, checks and troubleshooting.
- [Script catalogue](scripts/README.md): reads, writes, apply flags and recovery.
- [Tests](tests/README.md): offline checks, mutation controls and verification limits.
- [Evidence and implementation status](docs/06-agent-readiness/README.md): the complete
  Web App documentation collection, dated MCP contract and remaining release gates.

Detection is not blocking. A successful scan, setup checkbox, preview or unchanged
cookie count does not establish that tags respected a visitor's choice. Report
only the trackers and actions actually tested, without compliance guarantees.

## Security and contribution

Read [SECURITY.md](SECURITY.md) before authorizing scripts. A Google write scope can
reach every container the account can access. The writer simulates by default,
ties application to an approved current-state plan, preserves business events and
regional tables, and keeps publication separate. Failures require inspection
before retrying; a partial application is not a finished version.

Repository documentation, skill instructions, scripts and tests are authored in
English. Source snapshots retain original bytes for provenance. Update canonical
files and regenerate installed packages, rather than editing generated copies.
Run the documented checks before a pull request. Keep credentials and customer
records out of commits. This repository does not send telemetry.
