---
name: consent-pro-gtm
description: Configure or diagnose Google Tag Manager consent with Consent Pro, including consent mode, regional defaults, conversion triggers and tags firing before consent. Use for GTM-specific work; use consent-pro for the wider installation journey.
---

# Consent Pro and Google Tag Manager

Read [operations](../docs/06-agent-readiness/operations.md) for the target, available
tools and permission boundaries. Read the [nine steps](../docs/reference/nine-steps.md)
before configuring a container. Resolve document and script links relative to the
file containing the link, not the user's working directory. Run scripts using the
absolute path obtained from that link.

## Establish the target and evidence

- Identify the Consent Pro workspace, project, public hostname and installed engine.
  Use [inspect-site.py](../scripts/inspect-site.py) for public HTML if terminal access exists. HTML
  inspection does not observe browser behavior. Otherwise use MCP setup details
  and evidence from the user, and label what remains unverified.
- Identify the Google account, container and workspace separately. Read back their
  live names. Never infer a target from the first result or a scanner match hint.
- Discover the connected server's actual tools and schemas. The recorded staging
  catalogue has GTM read tools for the published container, not workspace writes.
  Do not invent future tool names or treat a published audit as an unpublished audit.
- Use local Google OAuth only when the user selects that broader access path.
  An MCP permission denial is not approval to switch credentials or use the UI.

## Plan before writing

Inspect the existing configuration, template provenance, every relevant tag's
firing and blocking triggers, consent checks, and the complete regional table.
Ask the user to resolve ambiguous categories, especially Essential. A scaffold
defaults to marketing as a restrictive placeholder, not a classification.

Agree explicitly on Google Basic or Advanced mode. Read
[categories](../docs/reference/categories.md) for the distinction. Do not enable
Advanced because a tag has built-in consent checks. Preserve purchase, form and
other business-event conditions. The consent event must not replace a conversion.

Present the exact target and before/after changes, including regions, template
permissions and effects on existing behavior. Use specific authorization already
given; ask only for missing scope or a materially changed plan. Saving, creating
a version, publishing GTM, publishing Consent Pro and deploying site code are
separate actions. Never infer publication approval from setup approval.

## Choose the available execution path

| Path | Action |
| --- | --- |
| MCP read tools | Diagnose the published container, follow pagination and details, then give the concrete manual plan |
| Local API scripts | Read [run guide](../docs/04-run-it.md) and [security](../SECURITY.md); authorize, audit, scaffold, review categories, simulate, then apply only approved changes |
| GTM interface | Follow the nine steps; use the Gallery, review permissions and preserve recognized existing templates |
| Future MCP writes | Read the new contract first; require workspace reads, conflict handling, preservation, readback and separate publication. Stop where the contract is insufficient |
| No container access | Supply exact steps and values; describe user-reported state as reported, not verified |

The local writer is deliberately conservative. Check its `--help` and simulation
before applying. If it refuses an unsupported event, regional table or existing
setting, explain the reason and prepare a manual plan; do not bypass its checks.
After a partial failure, inspect what actually saved before retrying. Do not
publish half-applied state or retry a write with an unknown result blindly.

New Gallery imports are pinned to `finsweet/gtm-template-consent-pro`, SHA
`8a551897e5bfdecf03de59fa00058be442b7ac29`. Preserve recognized existing manual or
Gallery imports. Modified or unknown templates need review, not automatic replacement.
Gallery availability is not evidence of Google CMP certification.

## Verify and hand off

Re-read the workspace after writes and the published version after publication.
Then follow [behavior checks](../docs/reference/verify-behaviour.md): named trackers,
real business actions, before choice, rejection, acceptance, partial choice,
revocation and reload. Use acceptance as a positive control that the tracker can
actually be exercised and observed. Record browser, region, mode and tested scope.

Report saved configuration, version creation, publication and browser evidence
separately. A scan, checkbox, preview or cookie count does not prove blocking.
Do not promise legal compliance. Include pending dashboard actions and concrete
next checks. Use [troubleshooting](../docs/reference/troubleshooting.md) when
configuration and observed behavior disagree.
