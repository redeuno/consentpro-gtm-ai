# 0. The installation journey

The agent acts as an instructor and operator: explain the next step, carry out supported
authorized work, verify the result and continue. For a first conversation, start with
[client setup](07-agent-installation/README.md#start-in-your-current-chat).

Start from the customer's current state, not from an empty installation. Read the connected
workspace and project or guide their selected dashboard, inspect the site, and identify what already exists before proposing
changes. The [operations guide](06-agent-readiness/operations.md) supplies the capability
checks, runtime checks and recovery paths for each stage.

No account yet, a missing purchase, a login problem or a missing connector belongs
to the [entry routes](reference/onboarding.md#route-the-customers-starting-state).
A customer can begin without buying first, connecting Google or using a terminal.
Product access and production-domain licensing are still checked for the selected
platform. The [support route](reference/troubleshooting.md#support-and-assisted-setup)
is available when the customer needs human guidance or implementation assistance.

Use the [guided onboarding conversation](reference/onboarding.md) to turn these
stages into a customer-facing sequence with progress, manual handoffs and explicit
completion evidence. Resume existing work rather than starting the list again.

## Choose the available path

Discover the current server's tools and effective access when using a connector.
Do not infer its environment, scope or supported writes from an earlier session.
See the [capability matrix](06-agent-readiness/operations.md#capabilities-and-targets).

| Path | Requirements | What it covers |
|---|---|---|
| Consent Pro MCP | Connected account, workspace and relevant scopes | Available project reads and selected writes; current GTM reads |
| Consent Pro interface | Customer's account and target workspace/project access | Guided project, banner, tracker, preview and publication steps, without a connector |
| GTM interface | Google account with target container access | Manual template and container configuration |
| Local GTM scripts | Terminal, Python, own Google OAuth client and token | Audit, simulation and explicitly approved container configuration |
| Site code and browser | Customer code and test-domain access | Core installation, pixels, preferences and observed behaviour |

An MCP permission does not authorise a broader local Google credential. A declined
connector leaves the manual path available for both CP and GTM. If an operation is
unavailable, explain the alternative and use only the customer's chosen route.
Use the [evolving GTM path](06-agent-readiness/operations.md#future-gtm-writes) when
new operations appear; confirm their reviewed contract, scopes and workspace evidence
before replacing the corresponding manual step.

## The installation stages

| Stage | Required result | Agent path and remaining decision |
|---|---|---|
| Enter | Correct account/workspace or a precise access dependency | Use official entry/recovery, investigate existing purchases and support manual dashboard work |
| Identify | Workspace, project, hostname, platform and goal agree | Read project state and inspect the installed engine; resolve ambiguous matches |
| Connect domain | Correct custom-site project and public hostname | MCP can create a project or update its domain when authorised; Webflow onboarding uses the dashboard |
| Configure banner | Type, regions, style and privacy link reviewed | MCP supports selected style and privacy-link edits; do not infer type, region or category writes |
| Install core | Exact project snippet deployed and checked | Read the snippet, edit the shared head, deploy with the corresponding authority and verify the domain |
| Scan | Completed scan with stated coverage | Detect targets, review settings, start an authorised scan and follow its report |
| Review trackers | Categories and descriptions reflect actual use | Review detected and missing trackers with the customer; guide dashboard edits when the reviewed connector lacks the operation |
| Decide and configure GTM | No GTM by choice, or the selected container's mode, regions, triggers and checks match the plan | Guide manual setup, use reviewed supported operations, or explicitly selected local scripts; preserve direct integrations |
| Preview and test | Draft behaviour observed on the intended site | Use the signed preview and exercise named trackers, choices and page actions |
| Publish | Site code, Consent Pro configuration and GTM version accounted for | Separate releases and authority; guide the dashboard when the reviewed connector does not expose publication |
| Operate | Preferences, revocation, logs and future scans checked | Follow the operations guide and report remaining limits |

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

For a custom site, Preview is not a free production domain or blanket staging
entitlement. The documented Webflow test on a `*.webflow.io` domain is a separate
platform path. See [Webflow licensing](https://docs.consentpro.com/webflow/licenses).
Neither path implies access to a product development MCP environment.

## Scan and review

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

Choose [Basic or Advanced Consent Mode](reference/consent-mode.md) explicitly. Preserve
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

Report what was read, saved, published and observed, with target and limitations. The
[source review](06-agent-readiness/README.md) records evidence and source conflicts.
Use the [resume card](reference/onboarding.md#start-and-resume) when interrupted and
[verify the successor's access](reference/onboarding.md#transfer-maintenance) before
calling maintenance handed over. A summary preserves context, not authority.
