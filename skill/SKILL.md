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
Instructions already read can guide the current chat without persistent skill
installation. Use the [first-reply procedure](../docs/07-agent-installation/README.md#start-in-your-current-chat)
instead of sending another starter prompt or a mandatory upload detour. For full
setup, recommend the verified connection once and explain the manual alternative;
preserve a declined or deferred route. Use an MCP URL approved for the product
environment and supplied by Consent Pro or the customer when connection is needed;
never derive an endpoint from a hostname. Offer the reusable skill at a useful pause,
without interrupting the installation unless requested. Ask for the site when needed,
without bundling platform, GTM and license questions. A narrow audit does not
require client installation. Assistant setup can proceed without the website URL.

Use the shared [question procedure](../docs/reference/onboarding.md#ask-for-the-next-decision)
for container selection, connection choices and consent decisions. Prefer an available,
permitted host question tool with concise options; otherwise ask in ordinary text.
Keep known answers and declined routes. A recommendation, default selection or
silence does not authorize edits, publication or rollback.

When supporting a first Consent Pro installation, solve the relevant GTM dependency
and return to the [first-activation journey](../docs/00-the-journey.md). Do not expand
it into a container redesign or require Google authorization when the customer can
complete the same step in GTM. Known consent failures in the initial path need
treatment; broader inventory and optional improvements can follow publication.

If reconciliation needs a new scan, follow the shared
[scan access check](../docs/06-agent-readiness/operations.md#before-starting-or-retrying-a-scan)
before starting or retrying. A robots or firewall block is a site-access dependency,
not a reason to reconnect Google or change GTM triggers. Reuse a relevant scan and
continue independent configuration while the site owner resolves a known blocker.

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
- Discover the connected server's actual tools and schemas when a connector is used.
  Determine whether reads cover the published container or the selected workspace.
  Do not invent future tool names or treat a published audit as an unpublished audit.
- Use local Google OAuth only when the user selects that broader access path.
  An MCP permission denial is not approval to switch credentials or use the UI.

If GTM is not connected, offer the manual interface path or explain the optional
[connection flow](../docs/06-agent-readiness/operations.md#connect-google-tag-manager).
Declining OAuth leaves a complete manual path; do not insist, create a local OAuth
application or require a terminal. CP itself may also be entirely manual. If the
customer chooses connection, follow the supported flow.
Only the client opens the returned GTM
authorization link. Then read status and the selected container before proceeding.
Reuse a working connection; never reconnect merely because onboarding has started.
While awaiting a manual step, inspect independent site evidence when useful.

If GTM does not exist, confirm whether adoption is part of the requested outcome.
Use [account setup](../docs/02-tag-manager-account.md) when it is. Otherwise continue
with direct scripts and pixels through the main Consent Pro workflow. An existing
but uninstalled container needs a live-version review before its snippet reaches
the site; its already-published tags can run immediately. Coordinate configuration,
test deployment and publication. Another CMP requires the
[transition procedure](../docs/06-agent-readiness/operations.md#existing-cmp-and-tracking-transition).

## Teach and complete the missing setup

For a first installation, lead the relevant nine steps in small batches. Explain
the purpose of the template, initialization tag, default consent and update event
when each is needed. Inspect for a recognized template before requesting an import.
If installation is needed, use a supported, reviewed import operation when authorized,
including its publisher/template identity and permission review. Otherwise give the
Gallery route and expected installed result from the guide. Verify the saved template
and initialization tag; if only the client can act, read the configuration afterward
or mark their confirmation as reported, then continue. Do not end with a Gallery link
and leave the rest of the journey implicit.

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

Explain [waiting for acceptance versus sending limited measurements](../docs/reference/consent-mode.md#explain-the-choice-before-asking)
before asking when Google measurement should start. Use Basic/Advanced as secondary
labels; Advanced still sends data before acceptance. Agree explicitly and keep
an explanation request pending. Do not enable Advanced because a tag has built-in
consent checks or the client is experienced.
Preserve purchase, form and
other business-event conditions. The consent event must not replace a conversion.

Present the exact target and before/after changes, including regions, template
permissions and effects on existing behavior. Use specific authorization already
given; ask only for missing scope or a materially changed plan. Saving, creating
a version, publishing GTM, publishing Consent Pro and deploying site code are
separate actions. Never infer publication approval from setup approval.
MCP edits belong in its dedicated **Consent Pro MCP** workspace, never Default.
For tag, trigger or variable changes, review the exact resource IDs, dependencies
and before/after fields; preserve unrelated fields and business-event conditions.
An authorized paused test tag remains paused. A test request does not authorize
editing similarly named production resources or publishing the test artifact.

## Choose the available execution path

| Path | Action |
| --- | --- |
| MCP read tools | Discover whether the read covers the live version or selected workspace; follow pagination/details. Guide unavailable writes through a concrete manual handoff and verify the affected state. A live-only read cannot verify unpublished edits. |
| Local API scripts | Read [run guide](../docs/04-run-it.md) and [security](../SECURITY.md); authorize, audit, scaffold, review categories, simulate, then apply only approved changes |
| GTM interface | Guide account/site setup and the nine steps, using the customer's selected workspace; no API, Google Cloud or terminal requirement. Use the Gallery and preserve recognized templates |
| Discovered MCP editing | Follow [GTM capability path](../docs/06-agent-readiness/operations.md#future-gtm-writes): require a reviewed contract, matching scopes, workspace evidence, concurrency protection and saved-state verification. Reads or reliable edit-tool previews/results can supply that evidence; stop only dependent work where it is insufficient |
| No container access | Supply exact steps and values; describe user-reported state as reported, not verified |

For every manual handoff, name the target workspace, control, exact intended value,
expected result and evidence needed to resume. Do not tell a beginner to "configure
consent" without the next actionable step. After confirmation, read back what the
available path can observe and advance without asking whether to continue.
When the user has authorized a repair and a supported write path is available,
carry it out and verify it; a diagnosis or a proposed plan alone is incomplete.
Refresh discovery after capability or permission changes. A prior read-only
contract is not a permanent restriction, and a promised release date is not a
write grant. A new tool under an existing permission does not require reconnection;
a newly required permission needs a grant upgrade. Confirm any required Google scope
upgrade separately and preserve the selected container's access limits. If a write
times out, inspect the workspace before retrying; never repeat a create/import
blindly or publish unrelated pending changes with the requested fix.

Rollback is a separate live change, with its own operation, permission and user
approval. Identify the exact prior version, review its full differences from the
current live container, and verify the live version after restoration. Do not
assume publishing authority includes rollback or that undoing a workspace edit
restores the live version. A rollback does not reset Google's latest version used
for workspace synchronization; inspect live, latest and saved workspace state
before resuming edits or an interrupted publication.

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

When this task is part of onboarding, maintain the shared
[progress record](../docs/reference/onboarding.md). Give manual GTM changes by
exact tag, before/after values and verification step. Re-check after the customer
acts; distinguish a reported workspace edit from a verified published version.

Verify the saved workspace through supported reads or authoritative edit results,
then re-read the published version after publication. A preview or acknowledgement
alone does not prove a saved draft.
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

At interruption, use the shared [resume card](../docs/reference/onboarding.md#start-and-resume)
and refresh the affected workspace/live version before continuing. A successor
uses their own authorized access; agency clients do not share scope or approval.
Use the [support handoff](../docs/reference/troubleshooting.md#support-and-assisted-setup)
for the precise unresolved dependency without sending a message or promising
implementation services unless the customer requested them and eligibility is verified.
