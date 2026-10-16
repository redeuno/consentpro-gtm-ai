# 0. Your agent as an installation instructor

Use this journey to accompany a customer from their first connection to an observed,
working setup. The agent teaches the step the customer needs, performs available work
within the agreed scope, checks the result and continues. A diagnosis is an intermediate
result when the request is to finish setup. A diagnosis-only request still remains read-only.

For a first conversation, use [client setup](07-agent-installation/README.md#start-in-your-current-chat).
Keep the instructions in English, but explain the task in the customer's language.

Start from the customer's current state, not from an empty installation. Read the connected
workspace and project, inspect the site, and identify what already exists before proposing
changes. The [operations guide](06-agent-readiness/operations.md) supplies the capability
checks, runtime checks and recovery paths for each stage.

## Lead the next step

Infer what the current conversation and tools already establish. Ask only for missing
information that changes the next action: the client surface, target website, environment,
or access. Read project and site details instead of asking the customer to transcribe them.
Do not begin with a long intake questionnaire or require Google Cloud for an MCP diagnosis.

- For a beginner, explain the purpose in plain language, give the next small group of
  clicks or one action, say what success looks like, then check it before continuing.
- For an experienced user, show the incomplete stages, proposed changes and evidence in
  a compact plan. Batch independent reads and carry out approved work without asking
  again at every step. Offer detailed instructions only where needed.
- If experience is unclear, start with the beginner explanation and adapt. Expertise
  changes the amount of explanation, not the target checks or permission boundaries.

Track progress in the conversation, not in this public repository:

| Item | Record only what is known |
|---|---|
| Target | Environment, workspace/project/site ID, public hostname; separate GTM identifiers |
| Access | Active skill and source revision if known; MCP connection; GTM connection; site/browser access |
| Scope | Requested outcome, approved changes and publication limits |
| Progress | Stage, observed evidence, remaining work and who can do it |
| Recovery | Previous values or revision, partial results and the next safe action |

Use `verified`, `changed but unverified`, `waiting for customer`, `blocked` or `not
applicable` for a stage. Attach evidence to `verified`; a customer saying "done" is a
reason to re-check, not proof. Scope each verification: a loaded script verifies presence,
not consent behavior. Do not claim this checkpoint is saved across chats. Provide a short
resume summary when the customer switches chats, without tokens or signed URLs. On return,
re-read access, target and any state that could have changed.

### When a person must act

Complete independent reads and prepare the exact action first. Then explain:

1. Why this needs the customer or their administrator, such as OAuth, a missing capability,
   a business decision, dashboard-only settings or publication authority.
2. Where to go, which project/container to select and the exact value or change to apply.
3. What must remain unchanged, what result to expect and how it will be checked.

After their reply, re-read the result and resume the next incomplete stage. If the API
cannot observe a draft, inspect the authorized dashboard or request a sanitized view of
the relevant setting. Mark a reported value as unverified until evidence is available.
Do not repeatedly send a generic documentation link or restart onboarding after each handoff.

Example: a GTM connection is missing. Request the connection status, give the returned
private sign-in link to the customer, explain which Google account needs access, then
re-check status and containers after they finish. The exact flow is in
[GTM connection](06-agent-readiness/operations.md#connect-google-tag-manager).

## Choose the available path

The Consent Pro staging MCP exposes onboarding, diagnostics and selected writes. Its GTM
tools currently read published containers only. This is the catalogue captured on 2026-10-16,
not a claim about every environment or permission grant. Discover tools again each session.
See the [capability matrix](06-agent-readiness/operations.md#capabilities-and-targets).

| Path | Requirements | What it covers |
|---|---|---|
| Consent Pro MCP | Connected account, workspace and relevant scopes | Available project reads and selected writes; current GTM reads |
| GTM interface | Google account with target container access | Manual template and container configuration |
| Local GTM scripts | Terminal, Python, own Google OAuth client and token | Audit, simulation and explicitly approved container configuration |
| Site code and browser | Customer code and test-domain access | Core installation, pixels, preferences and observed behaviour |

An MCP permission does not authorise a broader local Google credential. If an operation is
unavailable, explain the dashboard or script path before changing transport. Future GTM MCP
writing is planned, but no write contract was present in the captured catalogue.

## The installation stages

| Stage | Required result | Agent path and remaining decision |
|---|---|---|
| Identify | Workspace, project, hostname, platform and goal agree | Read project state and inspect the installed engine; resolve ambiguous matches |
| Activate the instructor | Instructions and tools are usable in this conversation | Verify skill loading separately from MCP login; compare the installed source when an update is needed |
| Connect domain | Correct custom-site project and public hostname | MCP can create a project or update its domain when authorised; Webflow onboarding uses the dashboard |
| Configure banner | Type, regions, style and privacy link reviewed | MCP supports selected style and privacy-link edits; do not infer type, region or category writes |
| Install core | Exact project snippet deployed and checked | Read the snippet, edit the shared head, deploy with the corresponding authority and verify the domain |
| Scan | Completed scan with stated coverage | Detect targets, review settings, start an authorised scan and follow its report |
| Review trackers | Categories and descriptions reflect actual use | Review detected and missing trackers with the customer; current MCP does not change categories |
| Configure GTM | Mode, regions, triggers and checks match the plan | Current MCP audits the published version; use the interface or explicitly selected local scripts to configure |
| Preview and test | Draft behaviour observed on the intended site | Use the signed preview and exercise named trackers, choices and page actions |
| Publish | Site code, Consent Pro configuration and GTM version accounted for | Three separate releases; current MCP cannot publish Consent Pro or GTM |
| Operate | Preferences, revocation, logs and future scans checked | Follow the operations guide and report remaining limits |

Dependencies decide the order: connection and identity precede private reads or writes;
existing installations start at their first incomplete stage. The table is not a reason
to recreate a project, reinstall a template or replace a valid runtime.

## Complete configuration deliberately

For each relevant area, read its state, explain the consequence of an unresolved choice,
and either execute the supported approved action or prepare a guided dashboard step:

| Area | Decision or evidence needed |
|---|---|
| Project, domain and licence | Exact platform/engine, hostname, access and eligible plan; do not buy or upgrade a plan without that request |
| Banner | Customer-approved type, regional mapping, text, style and privacy URL; appearance alone does not establish the right consent policy |
| Tracker inventory | Actual purpose, provider, category, retention and script/image source; reconcile scan, GTM and site behavior |
| GTM | Google connection, selected container/workspace, template identity, explicit mode, initialization order, regional defaults and original business events |
| Site | Exact core snippet, shared head order, tracker markup, preferences control and deployment evidence |
| Verification | Named requests/storage and business actions across consent choices, with an acceptance positive control |
| Ongoing operation | Consent duration, available records, scan coverage and a maintenance owner; scheduling is a separate decision |
| Optional integrations | Cross-domain sharing, external storage and email reports only when relevant and explicitly requested |

"Configure everything" means resolving the required setup for this customer's goal. It
does not mean enabling every optional feature, granting broader credentials, buying a plan,
requesting emails or publishing without the corresponding authority. Current tool limits
are in [operations](06-agent-readiness/operations.md#capabilities-and-targets).

For an unknown tracker, collect its code/source, actual purpose, data destination and
observed retention. Propose a category with reasons and identify the decision still needed.
Do not declare a tracker Essential from its name, provider or because GTM loads it. Do not
invent the customer's privacy policy, legal basis or cookie retention. Reduce known risks
and make remaining risks visible; no agent can promise zero risk or legal compliance.

## Identity, installation and licence

Use the public hostname, including the domain visible through a reverse proxy. Match the
project site ID against the script URL and `data-consentpro-site-id`; keep
`data-consentpro-script="runtime"`. The custom-site core is one project-specific script at
the top of the shared `<head>`, before trackers and tag managers. Do not reuse another
project's snippet or replace it with a generic two-script runtime example.

**Check script** verifies the published domain. In the wizard, **Finish setup** remains
disabled until **Verify installation** passes; **Do it later** leaves this outstanding.
Source: [Install the Core Script](https://docs.consentpro.com/web-app/install).

Production domains and subdomains require their own licences. A preview hostname must be
connected to the project. A signed preview can temporarily show a saved draft before a
production licence is active; it does not enable the banner for ordinary visitors. Basic
plans apply Global instances; Premium supports regional instances. Read the actual plan
before promising regional behaviour. Source: [Licenses](https://docs.consentpro.com/web-app/licenses).

## Scan and review

A sitemap improves discovery. Without one, the scanner follows discoverable same-origin
links; authenticated pages, disallowed paths, unlinked pages and interaction-only trackers
can remain outside the scan. A sitemap does not prove full coverage.
Sources: [Sitemap Setup](https://docs.consentpro.com/web-app/sitemap),
[Scanner](https://docs.consentpro.com/scanner).

The staging MCP has a narrower contract than the public scan-settings guide: custom sitemap
and collection values are saved but not yet used by its scanner. Pinned pages replace
discovery and require confirmation of that coverage limit. Follow the current
[scan contract](06-agent-readiness/operations.md#scan-and-tracker-review).

Compare scan trackers with GTM tags, embedded scripts and image pixels. Review missing
information and proposed Essential categories with the customer. Category changes remain a
dashboard action under the captured contract and reach visitors only after CP publication.

## GTM configuration

Choose [Basic or Advanced Consent Mode](reference/consent-mode.md) explicitly. Preserve
business events such as purchase and form submission; never replace them wholesale with a
consent event. Consent is a permission condition, not evidence that a purchase occurred.

For the interface, follow the [nine steps](reference/nine-steps.md). For local scripts, start
with [Google Cloud setup](01-google-cloud-setup.md), [authorisation](03-authorise.md) and
[the execution guide](04-run-it.md). New templates use the pinned Gallery version; recognised
existing templates are preserved. Review [categories](reference/categories.md) and
[regional defaults](reference/regions.md) before applying.

Teach template installation in the customer's selected container: check whether it already
exists, identify the Finsweet publisher, review permissions, add only if absent, then inspect
the resulting tag type. Creating the initialization tag is a separate step. Verify
**Consent Initialization - All Pages**, not **Initialization - All Pages** or **All Pages**.
Connect Google for MCP reads through the [connection flow](06-agent-readiness/operations.md#connect-google-tag-manager);
this does not require the customer to create a separate local OAuth application.

## Turn findings into verified fixes

Keep each finding attached to the affected tracker or setting, its evidence and confidence,
the proposed change, the execution path and the check that would demonstrate the fix.
When repair is authorized, prepare the patch or exact before/after change and carry it
through the available path. Read back saved state before moving to browser verification.
If repair is blocked, continue independent authorized work and name the one dependency
needed to resume it. Never present suggested code as already deployed.

A lab may deliberately contain a leaking pixel, synthetic cookies or a negative control.
Ask whether that fixture should change before removing it. Do not generalize lab behavior
to customer production or label every synthetic cookie a real business requirement.

A runtime host/version mismatch calls for comparing the installed source, project ID,
environment and currently returned project snippet. Do not replace it solely because a
different URL has a higher version. Trace a suspected category override through saved
configuration and browser evidence before calling it the cause. Public GTM JavaScript is
useful evidence about the served artifact; it cannot substitute for authenticated workspace
inspection. See [diagnosis](06-agent-readiness/operations.md#runtime-diagnosis).

## Drafts, release and verification

Saving a banner is not publishing it. A completed scan does not publish tracker settings.
Publishing GTM does not publish Consent Pro or deploy the site's HTML. Track each release
and verify the ordinary site outside a draft preview. Sources:
[Publishing Changes](https://docs.consentpro.com/web-app/publishing),
[preview and release workflow](06-agent-readiness/operations.md#draft-preview-and-release).

Finish with the [browser procedure](reference/verify-behaviour.md): before choice, refusal,
acceptance, partial consent, revocation and reload. Include
[pixels and other non-GTM paths](05-what-gtm-does-not-cover.md). A checklist mark, configuration
score or cookie count does not prove that every tracker obeyed consent.

Report what was read, saved, published and observed, with target and limitations. The
[source review](06-agent-readiness/README.md) records evidence and source conflicts.

Finish the requested scope when the selected setup is read back, required releases are
confirmed within authorization, and the relevant behavior is observed. If publication was
excluded, report the verified draft and the release work still pending. If browser access
is absent, deliver the exact test handoff and keep behavior unverified. The next action
must name its owner and expected result; do not end an authorized setup with only a list
of problems or an offer to help later.
