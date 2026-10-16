# Guided onboarding conversation

Use this procedure when a customer asks to set up a site end to end, or to resume
an unfinished setup. Use the [journey](../00-the-journey.md) for dependencies and
[operations](../06-agent-readiness/operations.md) for current capabilities. Keep a
narrow diagnostic or banner-edit request within its original scope.

## Contents

- [Start and resume](#start-and-resume)
- [Sequence and completion evidence](#sequence-and-completion-evidence)
- [Tracker and GTM decisions](#tracker-and-gtm-decisions)
- [Manual handoffs](#manual-handoffs)
- [Completion record](#completion-record)
- [Client delivery](#client-delivery)

## Start and resume

1. Discover available tools and effective access. Distinguish a missing connector,
   a missing permission and an expired Google connection. Read the current MCP
   documentation before offering setup guidance.
2. Resolve the site from the request and current project inventory. If the target
   is ambiguous, show matching names and domains and ask which one to use. If the
   exact target is already known, read it without asking the customer to repeat it.
3. Record environment, CP workspace/project/site ID and hostname. Associate GTM
   only through explicit target selection or corroborated site/container evidence;
   a scanner match alone is insufficient. Record the Google account and container
   separately. Never use the first accessible container by default.
4. Read the current state before presenting a plan. Reuse existing configuration
   and tests when their scope and versions remain applicable. Do not reinstall,
   reconnect, start another scan or change a working value merely to follow a list.
5. Show a short progress table and proceed to the next dependency that can be
   resolved. Continue independent reads while another step waits for access.

Use the customer's language. Introduce the current step, its purpose and its
result in plain language. Ask only for the next decision that changes the work;
do not send a long intake form or require the customer to supply values the tools
can read. Reuse specific authorization already given. A diagnosis-only request
authorizes no configuration changes.

Maintain this record in the conversation or an authorized customer workspace:

| Step | State | Evidence and scope | Next action and owner |
|---|---|---|---|
| Example: GTM configuration | Waiting for customer | Published version read; initialization trigger differs from plan | Customer changes the named tag in GTM |

Use states **not started**, **in progress**, **waiting for customer**, **waiting for
access**, **blocked**, **verified**, and **not applicable**. State why a step is not
applicable. For every verified claim, identify whether the evidence is saved
configuration, publication or browser behavior. Saving a draft verifies the save,
not the release or the behavior. On resume, refresh relevant state before writing;
do not treat an old checklist or approval of an outdated plan as current evidence.

## Sequence and completion evidence

The sequence is a dependency guide, not a requirement to repeat completed work.
Use the existing installation as the baseline for repair. The current staging
contract permits selected CP changes but neither tracker-category editing nor
CP/GTM publication. Discover again rather than assuming these limits are permanent.

| Step | Agent work | Completion evidence or handoff |
|---|---|---|
| 1. Select and connect | Resolve the project, environment and goal; check CP access and, when relevant, Google status and containers | Exact target recorded; unresolved access does not masquerade as an empty project |
| 2. Establish baseline | Read project, diagnosis, scan report, tracker details and public installation; audit GTM if present | Prioritized findings with sources; distinguish saved data, scan observations and browser evidence |
| 3. Agree behavior | Review banner type/regions, actual plan/license, privacy page, business events, tracker purposes and Basic/Advanced mode | Concrete decisions and before/after plan; unresolved Essential classification stays pending |
| 4. Prepare Consent Pro | Perform authorized supported style/privacy/scan-setting changes; guide unsupported category/type/region edits in the dashboard | Saved values read back; draft status and manual tasks recorded separately |
| 5. Prepare site code | Compare the exact project snippet with the served core, attributes, version/environment and order; review pixels, embeds and preferences access | Authorized code change and deployment verified, or exact manual instructions; HTML presence alone does not prove enforcement |
| 6. Scan and reconcile | Use a recent relevant scan or start the requested scan; follow it to completion and compare with GTM and hardcoded sources | Scan time, coverage and errors recorded; every relevant finding reviewed or explicitly unresolved |
| 7. Prepare GTM | Audit the published version; produce a per-tag plan, preserving business-event triggers and regional rows | Manual handoff under the current MCP; unpublished changes remain customer-reported unless a separately authorized surface can read them |
| 8. Preview and release | Test the draft where available; coordinate site deployment, CP publication and GTM publication as separate actions | Each applicable release independently confirmed; preview does not establish ordinary visitor behavior |
| 9. Verify and close | Re-read relevant state and exercise the browser acceptance matrix on the ordinary site | Scoped evidence, unresolved failures and the next owner/action; no global completion claim while required tests are missing |

If there is no GTM, mark its steps not applicable with the evidence and continue
testing direct scripts and pixels. If GTM is present but inaccessible, prepare
all independent CP work and keep the GTM dependency open. If only diagnosis is
requested, stop after the findings and proposed plan, without writes or a new scan.

A scan may be needed before tracker decisions or repeated after an authorized
change. Do not promise full-site coverage or start repeated scans without a reason.
Apply the current scanner's sitemap and pinned-page limits from operations.

## Tracker and GTM decisions

Build a short table per relevant source: tracker/cookie, tag or resource, actual
purpose, provider, observed or code-defined retention, saved category, proposed
category, trigger, consent requirements and unresolved questions. Do not infer the
provider from delivery through GTM. Distinguish a local test marker, a synthetic
cookie and a third-party request before interpreting an automated audit's severity.

Review Essential decisions with the customer using the site's actual purpose.
Read the setting that the runtime resolves when stored categories and HTML
attributes disagree; never assume a marketing attribute overrides a saved category.
For image pixels, check both the markup and the observed behavior before choice,
after acceptance and after revocation. Isolate intentional negative controls in
a lab; do not silently remove them or use them to certify a normal installation.

For each GTM change, name the tag ID/name, current trigger and checks, proposed
trigger and checks, reason, owner and verification. Follow the
[nine steps](nine-steps.md), [mode guide](consent-mode.md) and
[regional defaults](regions.md). Keep these distinctions explicit:

- Set consent defaults on **Consent Initialization - All Pages**.
- Use the correct Global/regional table for the selected banners and mode.
- `consent-updated` also follows rejection. It does not grant permission itself.
- Preserve purchase, lead, form, click and SPA event conditions. Add consent
  conditions to those events; do not turn a consent choice into a conversion.
- Choose Basic or Advanced explicitly. Do not apply Basic firing restrictions to
  a native Google tag selected for Advanced mode, or extend that exception to
  third-party tags without evidence.
- Preserve recognized templates. A missing Gallery reference alone does not prove
  a broken template, and a matching name alone does not establish its identity.

## Manual handoffs

Give one actionable unit at a time: destination, exact selected object, existing
value, intended value, whether the action saves or publishes, and the evidence to
bring back. For example, identify the exact initialization tag and required
trigger instead of asking the customer to "fix GTM".

When the customer says "done", re-read the relevant state if supported. Explain
that the published-only MCP will not show an unpublished workspace edit. Keep
that edit marked as reported, and verify the live version after authorized
publication. Do not publish solely to make the audit able to see a draft.

When a Google link expires, obtain a fresh link through the supported status tool.
Only the customer opens it. A successful connection proves access, not a finished
setup. If an operation or scope is unavailable, continue useful independent work
and name the remaining blocker. Do not silently switch to broader credentials.

## Completion record

Use the [behavior procedure](verify-behaviour.md) to record named requests and
relevant storage across no choice, rejection, acceptance, category-specific
acceptance, withdrawal and reload. Exercise applicable business events and check
repeated consent updates for duplicate conversions. Record browser, resolved
region, mode, pages and versions. If acceptance cannot exercise the tracker,
mark its result inconclusive. DOM evidence alone does not prove cookie contents,
network delivery, server receipt or HttpOnly behavior.

Close with a concise record containing:

1. Target and intended behavior.
2. CP saved configuration and publication status.
3. Site deployment and installed runtime evidence.
4. GTM published version and configuration findings, when applicable.
5. Observed tests, their scope and failures or missing observations.
6. Remaining action, owner and a specific next step.

Use "configured and verified for the listed scenarios" only when both claims
have evidence. Otherwise say which part is configured, unpublished, failed or
untested. A dashboard checkbox, scan or audit score cannot substitute for behavior
tests. Configuration is not a visitor's consent or a legal compliance guarantee.
Do not request an emailed consent export/proof merely to complete onboarding.

## Client delivery

Connecting MCP exposes the permitted tools; it does not install these skills into
every chat client. Use [installation](../07-agent-installation/README.md) to deliver
the general `consent-pro` skill and the `consent-pro-gtm` specialist for the selected
client. Hosted ChatGPT/Claude delivery must be validated separately from local
Codex/Claude Code installation. An updated GitHub file does not automatically
update an already installed hosted plugin.

Keep customer IDs, credentials, private connection/preview links and raw customer
records out of this public repository. Store customer progress only in their
authorized context. Maintain this reusable procedure with generic examples.
