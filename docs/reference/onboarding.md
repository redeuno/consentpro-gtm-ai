# Guided onboarding conversation

Use this procedure when a customer asks to set up a site end to end, or to resume
an unfinished setup. Use the [journey](../00-the-journey.md) for dependencies and
[operations](../06-agent-readiness/operations.md) for current capabilities. Keep a
narrow diagnostic or banner-edit request within its original scope.

For installation, lead to [first activation](../00-the-journey.md#first-activation-then-deeper-setup)
on the chosen site, then continue with deeper setup. The initial result does not
require using every feature or completing a comprehensive audit. A named failure
that affects publication or the site's main visitor action is an immediate
dependency; unrelated personalization is later work.

## Contents

- [Start and resume](#start-and-resume)
- [Route the customer's starting state](#route-the-customers-starting-state)
- [Adapt to the delivery team](#adapt-to-the-delivery-team)
- [Sequence and completion evidence](#sequence-and-completion-evidence)
- [Tracker and GTM decisions](#tracker-and-gtm-decisions)
- [Manual handoffs](#manual-handoffs)
- [Completion record](#completion-record)
- [Transfer maintenance](#transfer-maintenance)
- [Client delivery](#client-delivery)

## Start and resume

Begin the request in the current conversation using the instructions already read.
Identify the actual client and available tools without requiring persistent skill
installation. Use the [first-reply procedure](../07-agent-installation/README.md#start-in-your-current-chat)
for a bare repository link, an unavailable connector or an explicit request to
prepare the assistant first. Keep instruction loading, Consent Pro access, Google
access and site/browser access as separate checkpoints in the working record.

1. Establish the next useful step from the request, including when the customer has
   no account yet. Use the [entry routes](#route-the-customers-starting-state). Do not
   require a purchase, connector or technical questionnaire before helping.
2. Discover available tools and effective access when a connector is available. Distinguish a missing connector,
   a missing permission and an expired Google connection. Read the current MCP
   documentation before offering setup guidance. For full setup with no route
   chosen, recommend the supported connection and offer the reusable skill once.
   Confirm the product environment before providing an endpoint; do not silently
   choose manual work because no tools are connected yet. Reuse a working route.
   Keep the recommendation brief and do not let optional skill installation or
   Google authorization delay the site's first useful result.
3. Resolve the site from the request and current project inventory or selected dashboard. If the target
   is ambiguous, show matching names and domains and ask which one to use. If the
   exact target is already known, read it without asking the customer to repeat it.
4. Record environment, CP workspace/project/site ID and hostname when established. Associate GTM
   only through explicit target selection or corroborated site/container evidence;
   a scanner match alone is insufficient. Record the Google account and container
   separately. Never use the first accessible container by default.
5. Read the current state before presenting a plan. Reuse existing configuration
   and tests when their scope and versions remain applicable. Do not reinstall,
   reconnect, start another scan or change a working value merely to follow a list.
6. Proceed to the next dependency that can be resolved. Show the next useful action
   in plain language; reserve a progress table for a requested status, complex
   checkpoint or handoff. Continue independent reads while another step waits for access.

Use the customer's language. Introduce the current step, its purpose and its
result in plain language. Ask only for the next decision that changes the work;
do not send a long intake form or require the customer to supply values the tools
can read. Reuse specific authorization already given. A diagnosis-only request
authorizes no configuration changes.

For full setup from a repository link, first use the
[connection choice](../07-agent-installation/README.md#choose-how-the-assistant-will-work)
unless the route is already known. If project reads cannot resolve the target,
ask for the site URL when needed. Inspect available evidence before asking about
platform or GTM. "I already have an account"
is a fact to retain, not a reason to issue a purchase/workspace checklist. An
explicit request to install the skill or connect MCP can proceed without the site
URL. Do not send a new starter prompt back to someone who already asked for setup.
If instructions are readable, a missing persistent skill is not a blocker.

For a beginner, give one action or a small group of clicks, explain why it is needed
and what success looks like. For an experienced customer, give the compact plan and
batch independent reads. Infer the pace and adapt without an experience questionnaire.
Experience does not select Basic or Advanced Consent Mode. The same target, permission
and verification checks apply to both audiences.

Maintain this record in the conversation. Save it elsewhere only when the customer
explicitly requests an appropriate private destination:

| Step | State | Evidence and scope | Next action and owner |
|---|---|---|---|
| Example: first publication | Waiting for customer | Exact project snippet verified; Consent Pro changes remain a draft | Customer publishes the reviewed configuration to the selected domain |

Use states **not started**, **in progress**, **changed but unverified**, **waiting for customer**,
**waiting for access**, **blocked**, **verified**, and **not applicable**. State why a step is not
applicable. For every verified claim, identify whether the evidence is saved
configuration, publication or browser behavior. Saving a draft verifies the save,
not the release or the behavior. On resume, refresh relevant state before writing;
do not treat an old checklist or approval of an outdated plan as current evidence.

Carry the exact target, current access, requested outcome, authorization limits and
recovery values with the progress record. Do not claim it persists across chats.
Provide a short resume summary without secrets or signed URLs when the customer
switches conversations, then refresh relevant state in the new conversation.

Use this copyable card at an interruption or handoff. Omit unknown fields rather
than inventing values. The customer can keep it in the conversation or choose a
private destination. It is context, not proof of current access or permission:

```text
Resume Consent Pro setup
Target: [public hostname, platform, CP workspace/project, environment]
GTM, if used: [account, container, workspace, known live version]
Goal and decisions: [first activation or deeper setup, agreed task, mode/regions if relevant, open decisions]
Current step: [state, next action, responsible person or role]
Saved: [settings and evidence, including customer-reported changes]
License: [verified entitlement for this hostname, unresolved, or not yet checked]
Live: [site deployment, CP publication, GTM publication, or unknown]
Tested: [named trackers, actions, choices, browser/region, result and date]
Open issues: [failure or unavailable evidence, attempted steps]
Prior authorization: [who approved which target/effect; publication limits]
Resume check: [state, access and versions to re-read before continuing]
```

On return, load the instructions, confirm the same target and refresh affected
state. Expired sign-in needs access recovery, not a repeated installation. A
reported manual edit needs readback; a different live version needs comparison.
If a write may have succeeded before interruption, inspect its result before
retrying. Reuse valid approval for the same person, target and unchanged effect;
the card does not transfer another person's authority or grant a successor access.

## Route the customer's starting state

Use the first relevant row, not the whole table as an intake form. Infer known
facts from the conversation and available reads. Account entry and recovery live
in [installation](../07-agent-installation/README.md); account/project/license
diagnosis lives in [operations](../06-agent-readiness/operations.md#account-workspace-and-first-project).

| Starting state | Next useful action | Evidence or dependency |
|---|---|---|
| No account, or trying the product before purchase | Explain the current official entry and verified test/preview options; the customer completes sign-up or chooses preparation first | A signed-in account or an explicit preparation task; do not promise free access or buy a plan |
| Cannot sign in | Use the official sign-in/recovery interface and distinguish login method, expired session and organization access | Customer completes recovery; never request passwords, one-time codes or tokens |
| Purchased plan or license is missing | Compare the signed-in account, selected workspace, purchase owner and public domain/license | Existing entitlement found, or a precise discrepancy for support; no automatic second purchase |
| Account works, connector absent and route undecided | Recommend the verified connection before asking for dashboard values; confirm the environment before giving an endpoint | Customer accepts connected setup or chooses manual guidance; missing tools are not a refusal |
| Connector declined or confirmed unavailable | Continue the agreed dashboard route without repeating the offer | Relevant dashboard evidence; a connector is optional for manual guidance |
| No projects appear | Confirm workspace, permissions and the complete project list before treating it as empty | Correct project selected, access requested, or an authorized first project |
| No project for this site | Confirm domain, platform and owner, then guide the documented create/connect flow | Selected project, exact snippet and remaining setup verified separately |
| Setup is already partly complete | Inspect that setup and retain valid work | Start at the first unresolved dependency |
| GTM status is unknown | Inspect available site evidence, then the selected GTM account or dashboard | Public container ID is a clue, not proof of ownership or edit access |
| No GTM, no adoption requested | Explain that Consent Pro can still require work on direct scripts, pixels and embeds; clarify adoption only if it changes the task | Direct integration route, or explicit GTM adoption decision |
| Wants to adopt GTM | Use [account and site setup](../02-tag-manager-account.md), preserving existing measurement | Selected account/container, reviewed deployment order and target access |
| Only the customer can open CP or GTM | Guide the exact screen and value, then inspect the evidence the customer chooses to share | Reported, inspected and behavior-tested states stay distinct |
| Neither party has the required access | Prepare the exact administrator request and continue independent work | Named owner and next step, not a false completion claim |

A declined Google connection is a valid choice. Continue with the
[manual GTM path](nine-steps.md), without Google Cloud, an API key, local OAuth or
a terminal. If CP and GTM are both manual, use their dashboards as the configuration
source and [browser checks](verify-behaviour.md) for behavior. An unavailable read
does not turn a customer's acknowledgement into verification.

## Adapt to the delivery team

Infer the working context from the conversation. Ask who owns a decision only when it
affects the next step; do not require a company-type questionnaire before useful reads.

| Customer context | How the agent leads |
|---|---|
| Agency with multiple clients | Work on one confirmed client/project/container at a time. Separate client approvals, policies, credentials and progress. Never copy one client's IDs or policy decisions into another client's setup. Confirm a target switch before mutations. |
| Freelancer delivering a site | Reuse the agreed setup, identify who approves policy and publication, and prepare a concise handoff with saved/live status, tested scenarios and the maintenance owner. Delivery does not require transferring credentials in chat. |
| Business configuring its own site | Explain one practical step at a time, use available access, and name the exact action for the site administrator or marketing owner when needed. Lack of terminal access is not an onboarding failure. |

Map the customer's concern to an action and evidence, rather than explaining every feature:

| Concern | Agent action and evidence |
|---|---|
| Trackers run before a choice or after refusal | Identify the source and expected consent behavior, inspect GTM and direct scripts/pixels/embeds, then test named requests and storage with an acceptance control. Keep intentionally broken lab controls separate. |
| Google Consent Mode is confusing | Explain Basic and Advanced in terms of the chosen behavior, obtain the decision, verify defaults and updates, then test the applicable Google tags. Do not promise zero requests for an explicitly selected Advanced-mode setup. |
| The customer needs evidence | Distinguish configuration evidence, observed browser behavior and consent records. Explain what the available logs/statistics actually cover; request an emailed export or proof only when explicitly asked. Never promise that every decision was logged. |
| Different audiences need different settings | Review the customer's policy decisions, banner/plan eligibility and actual regional defaults. Use current authoritative guidance when a jurisdiction-specific question arises; do not turn broad geographic labels into legal rules. |
| Someone adds a tool after delivery | Compare the new tag, direct script, pixel or embed with the last verified state; review purpose/category and repeat affected consent and business-event tests. Assign a maintenance owner and an agreed review trigger. |

A useful handoff states what is saved, what is live, what was tested, which unresolved
items remain and who acts next. Offer a review after a new tracker, template/runtime change,
regional-policy decision or site release; do not silently create a scheduled job or promise
continuous monitoring. For an agency, report completion per site, not for the whole client
portfolio from a sample. The same conversational workflow can run in chat or a terminal,
but only use tools and instructions actually available in that host.

## Sequence and completion evidence

The sequence is a dependency guide, not a requirement to repeat completed work.
Use the existing installation as the baseline for repair. Discover the current
contract and effective grants; perform only supported authorized actions. Use the
dashboard for any operation absent from the reviewed contract, including category
editing or publication. Manual customers follow the same evidence requirements.

For a first installation, use the [activation path](../00-the-journey.md#first-activation-then-deeper-setup)
to select the depth of each step. Do the minimum relevant reads to prepare and
verify that result, rather than presenting a large diagnostic report first. The
customer may choose production directly; verify entitlement and specific release
authority rather than forcing staging. Keep a private draft Preview distinct from
a published test site, and both distinct from Consent Pro's internal staging.

| Step | Agent work | Completion evidence or handoff |
|---|---|---|
| 1. Select the route and target | Resolve account/project entry, environment and goal; use available CP/Google reads or the customer's selected dashboards | Exact target recorded; unresolved access does not masquerade as an empty project; connection is optional for manual guidance |
| 2. Establish relevant baseline | Read project and installation state, reuse relevant scan results, and inspect the tracking paths affected by the setup | Concrete activation dependencies with sources; expand diagnosis when a finding requires it, not as an automatic full audit |
| 3. Agree behavior | Review the initial banner, actual plan/license and privacy page; resolve tracker purposes, business events and Basic/Advanced mode only where applicable | Concrete decisions and before/after plan; unknown classifications are not silently treated as Essential |
| 4. Prepare Consent Pro | Save the authorized settings needed for the chosen result; guide unsupported fields in the dashboard | Saved values read back; suitable appearance retained, with cosmetic refinement and unrelated settings left for later |
| 5. Prepare site code | Compare the exact project snippet with the served core, attributes, version/environment and order; review pixels, embeds and preferences access | Authorized code change and deployment verified, or exact manual instructions; HTML presence alone does not prove enforcement |
| 6. Scan and reconcile when needed | Reuse a recent relevant scan or perform one required by the selected workflow or a concrete finding; follow any started work to completion | Time, coverage and errors recorded; publication-relevant findings addressed, with broader coverage explicitly pending |
| 7. Prepare GTM when relevant | Inspect affected tags and the applicable live/workspace state; preserve business-event triggers and regional rows | Use reviewed authorized edits or manual steps; neither GTM adoption, Google authorization nor a comprehensive container audit is a universal activation gate |
| 8. Preview and release | Test the draft where available; coordinate site deployment, CP publication and GTM publication as separate actions | Each applicable release independently confirmed; preview does not establish ordinary visitor behavior |
| 9. Verify the current result and continue | Re-read relevant state, exercise applicable consent choices and the main visitor action on the ordinary site | Initial activation and named behavior reported separately; wider untested coverage and the next improvement remain explicit |

If there is no GTM and adoption is outside the agreed goal, mark its steps not
applicable with the reason and continue testing direct scripts and pixels. If the
customer wants GTM, follow account setup and review the container's published tags
before installing a previously absent snippet. If GTM is present but inaccessible, prepare
all independent CP work and keep the GTM dependency open. If only diagnosis is
requested, stop after the findings and proposed plan, without writes or a new scan.

A scan may be needed before tracker decisions or repeated after an authorized
change. Do not promise full-site coverage or start repeated scans without a reason.
Apply the current scanner's sitemap and pinned-page limits from operations.

Before recommending publication, resolve observed consent failures, conflicting
CMPs and failures of the site's main visitor action that affect the proposed setup.
Use a supported, agreed temporary change only when its consequences are clear and
retested. Do not turn a broken form, cart or login into an Essential classification
shortcut. Check the visitor action separately from its analytics or conversion
event. A narrow verified result is not a whole-site assurance.

When the MCP gains GTM editing, keep this same journey and switch only the applicable
execution path. Follow [Future GTM writes](../06-agent-readiness/operations.md#future-gtm-writes)
to verify the reviewed tool contract, workspace access, effective permissions and recovery.
Do not reconnect working accounts, reinstall templates or publish just because new tools
appeared. A partial rollout can support one edit while another still needs a manual step.

"Configure everything" means the setup required for this customer's goal. It does
not mean enabling optional storage/sharing, granting broader credentials, buying a
plan, requesting emails or publishing without corresponding authority. Include
remembered-consent duration and a maintenance owner when relevant. Distinguish that
duration from tracker expiry and analytics retention. Do not invent a privacy URL,
legal basis, tracker purpose or retention value to fill an empty setting.

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

For another CMP already on the site, use the
[transition procedure](../06-agent-readiness/operations.md#existing-cmp-and-tracking-transition).
Identify who currently sets defaults, updates consent and loads each integration.
Do not add a second CMP, remove the current one or move every direct integration
into GTM just to fit this guide. Agree the transition and recovery first.

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

Complete independent reads and prepare the exact action first. Explain why this step
needs the customer or administrator, such as OAuth, an unavailable capability or a
business decision. If the supported repair is already authorized and executable,
perform it and check it; do not make the customer carry out work the agent can finish.

Give one actionable unit at a time: destination, exact selected object, existing
value, intended value, whether the action saves or publishes, and the evidence to
bring back. For example, identify the exact initialization tag and required
trigger instead of asking the customer to "fix GTM".

Ask progressively for the evidence needed by that step: selected project/container,
relevant tag list, then a named setting. Explain what a screenshot or export shares
and exclude secrets, visitor records and unrelated clients. A full container export
is not the default first request. If the screen differs, inspect its language,
selected object, permissions and current controls before repeating instructions.
Do not invent a button or treat the mismatch as the customer failing the step.

When the customer says "done", re-read the relevant state if supported. Explain
that the published-only MCP will not show an unpublished workspace edit. Keep
that edit marked as reported, and verify the live version after authorized
publication. Do not publish solely to make the audit able to see a draft.

When a Google link expires, obtain a fresh link through the supported status tool.
Only the customer opens it. A successful connection proves access, not a finished
setup. If an operation or scope is unavailable, continue useful independent work
and name the remaining blocker. Do not silently switch to broader credentials.

For a draft the MCP cannot read, use an authorized dashboard view or ask for the
relevant setting with personal records excluded. If the action did not take, resolve
that step rather than restarting onboarding. After a successful readback, continue
the next authorized step without asking whether to proceed.

Offer a verified assistance option when it fits the issue; do not require a long
unsuccessful manual sequence first. Use the
[support handoff](troubleshooting.md#support-and-assisted-setup) for access, billing,
unsupported operations or failures that need a human. Explain any eligibility
that has actually been confirmed. Preparing a summary is not sending it or opening
a case. Name the dependency preventing the current activation result, the exact
next action and its owner. While waiting, continue independent work; do not expand
into a full personalization exercise merely to fill the pause.

## Completion record

Keep these result states separate. They can be incomplete independently; they are
not a single funnel inferred from the hostname, purchase or connection:

| Result state | Evidence required |
|---|---|
| Preview available | The actual draft preview opens for the intended project; its expiry and private scope are known |
| Core installed | The correct project snippet is served on the intended hostname and the applicable install check passes |
| Published for ordinary visits | The relevant releases are confirmed and the ordinary site outside Preview serves the intended banner/configuration |
| Named behavior checked | The recorded consent choices, named tracking paths and visitor actions passed the applicable browser checks |
| License checked | The selected project's entitlement applies to this hostname and intended use; a visible banner or production URL alone does not prove payment |

The first activation report can be brief: what is live on which site, what was
checked, and any remaining dependency. Do not say the entire setup is verified if
only the banner appeared. Offer the next useful improvement after that report,
without automatically enabling optional features. Keep progress in the authorized
conversation; these milestones do not authorize telemetry or external reporting.

Use the [behavior procedure](verify-behaviour.md) to record named requests and
relevant storage across no choice, rejection, acceptance, category-specific
acceptance, withdrawal and reload. Exercise applicable business events and check
the visitor's main action separately from its tracking event. Check repeated
consent updates for duplicate conversions. Record browser, resolved
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

## Transfer maintenance

Before calling a handoff usable, have the intended maintainer use their own account
to open the selected CP project, site editor and GTM container where applicable.
For a connected assistant, they load the intended instructions and verify their
own target read. For a manual workflow, they locate the current settings and the
next action in their dashboards. Missing access stays an assigned dependency.

Record who can change settings, who can publish each system, and who owns policy
decisions. An agency changes one confirmed client at a time; the next client's
IDs, credentials, choices and authority must be resolved separately. A handoff
does not authorize transferring secrets, revoking the previous person's access
or reusing their private Google connection.

Agree a review trigger such as a new pixel/integration, template or runtime update,
site deployment, domain change or policy decision. Compare the affected sources
with the last verified state, then repeat relevant consent and business-event
checks. Offer scheduled scanning only when its capability, plan, costs and any
report delivery are understood and authorized. A schedule does not promise
continuous monitoring, automatic classification or automatic repair.

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
