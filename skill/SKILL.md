---
name: consent-pro-gtm
description: Guide and carry out Google Tag Manager consent setup and repairs with Consent Pro, including account connection, template installation, consent mode, regional defaults and business triggers. Use for GTM-specific work; consent-pro leads the wider client journey.
---

# Consent Pro and Google Tag Manager

Use the instructor workflow in the [Consent Pro skill](../skills/consent-pro/SKILL.md):
adapt to the client's experience, infer completed setup, carry the conversational
checkpoint ledger forward and resume after manual actions. When invoked directly,
establish the host and available capabilities without assuming that skill delivery,
MCP authorization and the client's Google GTM connection are the same thing.
An old transcript or repository test count does not identify the loaded package.

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

If GTM is not connected, explain what that connection grants and guide the client
through [the connection flow](../docs/06-agent-readiness/operations.md#connect-google-tag-manager).
Only the client opens the returned GTM
authorization link. Then read status and the selected container before proceeding.
Reuse a working connection; never reconnect merely because onboarding has started.
While awaiting a manual step, inspect independent site evidence when useful.

## Teach and complete the missing setup

For a first installation, lead the relevant nine steps in small batches. Explain
the purpose of the template, initialization tag, default consent and update event
when each is needed. Inspect for a recognized template before requesting an import.
If installation is needed, give the Gallery route, publisher/template identity,
permission review and expected installed result from the guide. After the client
acts, read the configuration or mark their confirmation as reported, then continue
with the initialization tag. Do not end with a Gallery link and leave the rest
of the journey implicit.

For an existing setup, use evidence to start at its first missing or incorrect
step. Preserve valid settings and test fixtures. When the site is a lab, establish
which deliberately broken tags, pixels or cookies are controls before correcting
them. Do not repair controls merely to produce a clean report.

## Plan before writing

Inspect the existing configuration, template provenance, every relevant tag's
firing and blocking triggers, consent checks, and the complete regional table.
Ask the user to resolve ambiguous categories, especially Essential. A scaffold
defaults to marketing as a restrictive placeholder, not a classification. Read
the tag's actual purpose and obtain missing business decisions; a product name
does not establish legal necessity or permission.

Agree explicitly on Google Basic or Advanced mode. Read
[categories](../docs/reference/categories.md) for the distinction. Do not enable
Advanced because a tag has built-in consent checks or the client is experienced.
Preserve purchase, form and
other business-event conditions. The consent event must not replace a conversion.

Present the exact target and before/after changes, including regions, template
permissions and effects on existing behavior. Use specific authorization already
given; ask only for missing scope or a materially changed plan. Saving, creating
a version, publishing GTM, publishing Consent Pro and deploying site code are
separate actions. Never infer publication approval from setup approval.

## Choose the available execution path

| Path | Action |
| --- | --- |
| MCP read tools | Read the published container, follow pagination/details and guide each unavailable write through a concrete manual handoff. Resume after confirmation; unpublished edits need workspace/UI evidence. |
| Local API scripts | Read [run guide](../docs/04-run-it.md) and [security](../SECURITY.md); authorize, audit, scaffold, review categories, simulate, then apply only approved changes |
| GTM interface | Follow the nine steps; use the Gallery, review permissions and preserve recognized existing templates |
| Future MCP writes | Read the new contract first; require workspace reads, conflict handling, preservation, readback and separate publication. Stop where the contract is insufficient |
| No container access | Supply exact steps and values; describe user-reported state as reported, not verified |

For every manual handoff, name the target workspace, control, exact intended value,
expected result and evidence needed to resume. Do not tell a beginner to "configure
consent" without the next actionable step. After confirmation, read back what the
available path can observe and advance without asking whether to continue.
When the user has authorized a repair and a supported write path is available,
carry it out and verify it; a diagnosis or a proposed plan alone is incomplete.

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
Do not promise legal compliance or zero risk. Include the current checkpoint,
pending client actions and the next verification; keep progressing while the
requested work can be completed within the granted scope. Use
[troubleshooting](../docs/reference/troubleshooting.md) when configuration and
observed behavior disagree.
