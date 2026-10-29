# 0. The installation journey

The agent acts as an instructor and operator: explain the next step, carry out supported
authorized work, verify the result and continue. For a first conversation, start with
[client setup](07-agent-installation/README.md#start-in-your-current-chat).

Start from the customer's current state, not from an empty installation. Read the connected
workspace and project or guide their selected dashboard, inspect the site, and identify what already exists before proposing
changes. The [operations guide](06-agent-readiness/operations.md) supplies the capability
checks, runtime checks and recovery paths for each stage.

For production setup, use the [production connection procedure](07-agent-installation/README.md#connect-consent-pro):
connect `https://mcp.consentpro.com/mcp`, let the customer sign in and select the
workspace, then verify the connection with a project read. Compare results in
[the production Web App](https://app.consentpro.com/). If an existing target uses
product staging, retain it until the customer selects a separate production target.
Connection alone does not migrate projects, runtime scripts or Google access.

No account yet, a missing purchase, a login problem or a missing connector belongs
to the [entry routes](reference/onboarding.md#route-the-customers-starting-state).
A customer can begin without buying first, connecting Google or using a terminal.
Product access and production-domain licensing are still checked for the selected
platform. The [support route](reference/troubleshooting.md#support-and-assisted-setup)
is available when the customer needs human guidance or implementation assistance.

Use the [guided onboarding conversation](reference/onboarding.md) to turn these
stages into a customer-facing sequence with progress, manual handoffs and explicit
completion evidence. Resume existing work rather than starting the list again.
For each missing decision, follow the shared [question procedure](reference/onboarding.md#ask-for-the-next-decision).
Use permitted host controls with a text fallback, retain answers and keep publication
authorization separate. Do not turn these stages into a questionnaire.

## First activation, then deeper setup

For an installation request, the first result is a working banner on the customer's
chosen test or production site. Personalization and broader review follow that
result. Reuse valid setup and make only the decisions needed for this site; do not
turn every feature or reference below into a prerequisite for the first publication.

The [Web App setup guide](https://docs.consentpro.com/web-app/) separates the initial
wizard from the Data Privacy Check. Its wizard connects a domain, configures a
banner and installs the core. **Do it later** can defer appearance customization;
it does not verify installation or tracker behavior. Retain suitable existing or
product-provided appearance while checking the banner choices, privacy link and
preferences relevant to the customer's intended behavior.

| Next result | Necessary work for this site |
|---|---|
| Target and available route | Identify the exact requested URL, selected hostname, project and intended product environment. Explain the required hostname-wide core installation, including its home page, and resolve scope before deployment. Reuse working access, recommend the supported Consent Pro connection once when relevant, or guide the selected dashboard. A persistent skill and Google authorization are not activation requirements. |
| Project ready for installation | Select or create the correct project, confirm the domain and applicable entitlement, and review the initial banner and policy choices. Ask only for missing decisions; do not start with visual customization. |
| Correct core installed | Use the exact project snippet in the shared head for the selected hostname, including `/` and inner pages. Preserve a working installation; resolve a conflicting CMP or deployment dependency rather than adding another runtime. |
| Initial behavior checked | Test the visible banner, preferences and the site's main visitor action. Check the named tracking paths affected by the setup, including refusal and acceptance where applicable. Investigate relevant failures without requiring a complete site audit. |
| Authorized publication reaches the chosen site | Review the exact target and live effect, obtain any missing publication authorization, and coordinate only the applicable site, Consent Pro and GTM releases. Recheck an ordinary visit outside Preview. |
| Activation result and next action | Record what is installed, published and observed, plus any unresolved issue. Continue with the customer's next useful improvement; wider untested coverage remains explicitly pending. |

The customer can choose production directly. Do not force a test-domain detour,
but check the applicable license and publication authority. A customer's test
hostname is not Consent Pro's product development staging. A signed Preview is a
separate draft result, not publication to ordinary visitors. Keep purchase and
license evidence separate: a production hostname or visible banner does not prove
payment, and a test hostname does not prove the absence of a purchase.

Retain the customer's selected product environment and target throughout follow-up
questions. After a reported save or install, verify that change and resume the
next missing activation dependency. A question about what the MCP can do calls
for a brief capability answer plus the next concrete step. A saved banner should
lead toward installation consistency, entitlement, preview and authorized release,
not an unsolicited appearance exercise. Missing release authority remains a
separate decision even when the customer asked for the overall installation.

Use the [three activation checkpoints](06-agent-readiness/operations.md#current-first-installation-handoffs)
to choose the next actionable step: site installation, initial banner and reviewed
publication. Explain that step when needed; do not present the full list as an
opening checklist.
Site installation requires separate site access or customer action. Discover banner
setup and publication separately and use each reviewed, authorized MCP operation
when available; guide the dashboard only for the missing or declined operation.
Project creation and script retrieval do not complete these checkpoints. Install
the core first in the shared head without `async` or `defer`.

Do not require a new GTM installation, Google connection, complete tracker inventory,
fresh comprehensive scan or full GTM audit merely to advance the checklist. Reuse
relevant results and perform a scan when the selected workflow or a concrete
finding requires one. Existing GTM or direct integrations still need attention if
they affect the intended consent behavior. Do not recommend publication with a
known competing CMP, observed tracking contrary to the agreed choice, or a broken
main visitor action. Resolve the cause or agree a supported temporary change,
then retest; do not classify unknown resources as Essential to get past a failure.

After the initial result, offer relevant appearance refinements, broader tracker
review, additional integrations, regional configuration, statistics or maintenance.
The stages below remain the reference for that work. Missing wider coverage is a
named follow-up, not a claim that every page or tracker has been verified.

## Choose the available path

Discover the current server's tools and effective access when using a connector.
Do not infer its environment, scope or supported writes from an earlier session.
Use the [connection verification](07-agent-installation/README.md#verify-the-connected-environment-and-tool-set)
to count only that endpoint's exposed tools and verify its workspace. Complete
Google authorization separately when the chosen GTM path needs it.
See the [capability matrix](06-agent-readiness/operations.md#capabilities-and-targets).

| Path | Requirements | What it covers |
|---|---|---|
| Consent Pro MCP | Connected account, workspace and relevant scopes | Reviewed operations available to the current connection; inspect GTM read and write scope separately |
| Consent Pro interface | Customer's account and target workspace/project access | Guided project, banner, tracker, preview and publication steps, without a connector |
| GTM interface | Google account with target container access | Manual template and container configuration |
| Local GTM scripts | Terminal, Python, own Google OAuth client and token | Audit, simulation and explicitly approved container configuration |
| Site code and browser | Customer code and test-domain access | Core installation, pixels, preferences and observed behaviour |

An MCP permission does not authorise a broader local Google credential. A declined
connector leaves the manual path available for both CP and GTM. If an operation is
unavailable, explain the alternative and use only the customer's chosen route.
Use the [GTM editing and publication path](06-agent-readiness/operations.md#future-gtm-writes) when
new operations appear; confirm their reviewed contract, scopes and workspace evidence
before replacing the corresponding manual step.

## The installation stages

Use this full reference for the agreed scope. The first-activation path above
selects the stages and depth needed now; it does not require completing every row
before an initial publication.

| Stage | Required result | Agent path and remaining decision |
|---|---|---|
| Enter | Correct account/workspace or a precise access dependency | Use official entry/recovery, investigate existing purchases and support manual dashboard work |
| Identify | Workspace, project, hostname, platform and goal agree | Read project state and inspect the installed engine; resolve ambiguous matches |
| Connect domain | Correct custom-site project and public hostname | MCP can create a project or update its domain when authorised; Webflow onboarding uses the dashboard |
| Configure banner | Initial behavior, applicable regions and privacy link reviewed; appearance can follow | Use available reviewed banner operations; if the required operation is absent, give the exact dashboard step, read back the result and continue |
| Install core | Exact project snippet deployed across the selected hostname and checked | Read the snippet, agree hostname-wide placement including its home page, deploy with the corresponding authority and verify `/`, the requested inner URL and the supported domain check |
| Scan | Completed scan with stated coverage | Detect targets, review settings, start an authorised scan and follow its report |
| Review trackers | Categories and descriptions reflect actual use | Review detected and missing trackers with the customer; guide dashboard edits when the reviewed connector lacks the operation |
| Decide and configure GTM | No GTM by choice, or the selected container's mode, regions, triggers and checks match the plan | Guide manual setup, use reviewed supported operations, or explicitly selected local scripts; preserve direct integrations |
| Preview and test | Draft behaviour observed on the intended site | Use the signed preview and exercise named trackers, choices and page actions |
| Publish | Site code, Consent Pro configuration and GTM version accounted for | Separate releases and authority; guide the dashboard when the reviewed connector does not expose publication |
| Operate | Preferences, revocation, logs and future scans checked | Follow the operations guide and report remaining limits |

## Identity, installation and licence

Use the public hostname, including the domain visible through a reverse proxy. Match the
project site ID against the script URL and `data-consentpro-site-id`; keep
`data-consentpro-script="runtime"`. The custom-site core is one project-specific script
at the top of the site's shared `<head>`, before trackers and tag managers.
Current custom-site onboarding requires it across the selected hostname,
including the home page (`/`); placing it only on `/campaign/` is not a supported
single-page installation. Explain this requirement and agree the scope before
deploying when the customer requested only one page. Banner page-visibility
settings, when available, do not replace hostname-wide core installation.
For `shop.example.com/campaign/`, the home page is `https://shop.example.com/`.
Do not substitute the parent `https://example.com/` or modify it without authority.
If the selected hostname's root belongs to another application or cannot be edited,
resolve that ownership/deployment dependency instead of promising a path-only setup.
Do not reuse another project's snippet or replace it with a generic two-script
runtime example.

**Check script** verifies the published domain. In the wizard, **Finish setup** remains
disabled until **Verify installation** passes; **Do it later** leaves this outstanding.
Source: [Install the Core Script](https://docs.consentpro.com/web-app/install).

Keep that result separate from evidence for the customer's exact page URL. A
negative domain check and a script present on a landing-page path may refer to
different responses. A missing core on the selected hostname's home page is an
incomplete installation even if the inner page has it. That does not establish
which URL the checker fetched or the cause of every failed check.
Inspect the checked URL when available, redirects, snippet
identity and environment before recommending a change. Do not infer a broken
runtime from a hostname difference alone. Follow the
[installation reconciliation](06-agent-readiness/operations.md#core-installation-and-licence)
and retain any unresolved checker result as a specific dependency.

Production domains and subdomains require their own licences. A preview hostname must be
connected to the project. A signed preview can temporarily show a saved draft before a
production licence is active. Preview does not publish that draft. It does not establish
whether an earlier published banner exists or what ordinary visitors currently see.
Anyone holding an unexpired preview link can open the draft; keep the link private.
Read publication state and check the ordinary URL without Preview before claiming
what visitors see. Without those checks, say: "Preview does not publish this draft.
I have not checked the ordinary site's published banner."

For "test first", give only the next unresolved step toward Preview. Do not assume
the project, script or banner is missing before inspecting the selected target.
Basic plans apply Global instances; Premium supports regional instances. Read the
actual plan before promising regional behaviour. Source:
[Licenses](https://docs.consentpro.com/web-app/licenses).

For a custom site, Preview is not a free production domain or blanket staging
entitlement. The documented Webflow test on a `*.webflow.io` domain is a separate
platform path. See [Webflow licensing](https://docs.consentpro.com/webflow/licenses).
Neither path implies access to a product development MCP environment.

## Scan and review

Before a new scan, [check access](06-agent-readiness/operations.md#before-starting-or-retrying-a-scan):
the selected site must be published and reachable, and its robots rules and security
controls may prevent scanning. Explain a known blocker and guide its correction
before retrying. Continue independent setup work while it is resolved; an existing
relevant scan may already be sufficient.

A sitemap improves discovery. Without one, the scanner follows discoverable same-origin
links; authenticated pages, disallowed paths, unlinked pages and interaction-only trackers
can remain outside the scan. A sitemap does not prove full coverage.
Sources: [Sitemap Setup](https://docs.consentpro.com/web-app/sitemap),
[Scanner](https://docs.consentpro.com/scanner).

Check the actual scanner contract rather than assuming every saved setting is
implemented. If pinned pages replace discovery, explain the resulting coverage
before changing them. Follow the current
[scan contract](06-agent-readiness/operations.md#scan-and-tracker-review).

Compare scan trackers with GTM tags, embedded scripts and image pixels. Review missing
information and proposed Essential categories with the customer. Guide category
changes in the dashboard when no reviewed write is available; saving and publication
remain separate.

## GTM configuration

Explain [when Google measurement starts](reference/consent-mode.md#explain-the-choice-before-asking)
and obtain the explicit choice when it affects the setup. Preserve
business events such as purchase and form submission; never replace them wholesale with a
consent event. Consent is a permission condition, not evidence that a purchase occurred.

If GTM is absent, keep the direct-integration route unless adoption is requested.
For adoption or an existing container missing from the site, follow
[account-to-site setup](02-tag-manager-account.md#connect-the-container-to-the-site).
Inspect published tags before installing an absent snippet, and use the
[CMP transition procedure](06-agent-readiness/operations.md#existing-cmp-and-tracking-transition)
when another consent system is already installed.

For the interface, follow the [nine steps](reference/nine-steps.md). Google OAuth
to the assistant is optional. If chosen, use the
[connection flow](06-agent-readiness/operations.md#connect-google-tag-manager).
For explicitly selected local scripts, start
with [Google Cloud setup](01-google-cloud-setup.md), [authorisation](03-authorise.md) and
[the execution guide](04-run-it.md). New templates use the pinned Gallery version; recognised
existing templates are preserved. Review [categories](reference/categories.md) and
[regional defaults](reference/regions.md) before applying.

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

Report what was read, saved, published and observed, with target and limitations.
Use the official sources linked beside each procedure and record any conflict with
the actual project or connected operation.
Use the [resume card](reference/onboarding.md#start-and-resume) when interrupted and
[verify the successor's access](reference/onboarding.md#transfer-maintenance) before
calling maintenance handed over. A summary preserves context, not authority.
