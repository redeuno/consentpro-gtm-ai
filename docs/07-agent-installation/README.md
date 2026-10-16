# Start the Consent Pro instructor in your client

This is the home for account entry, client installation and package maintenance. The
[journey](../00-the-journey.md) and [operations](../06-agent-readiness/operations.md)
remain the sources for product behavior; this page covers delivery to an agent.

## Get the ready package

Download the reviewed assets from [release 0.2.0](https://github.com/redeuno/consentpro-gtm-ai/releases/tag/v0.2.0):

| Asset | Use |
|---|---|
| `consent-pro-0.2.0-preview.zip` | Start here for the whole Consent Pro journey, including GTM guidance |
| `consent-pro-gtm-0.2.0-preview.zip` | Optional specialist for focused GTM work |
| `SHA256SUMS` | Compare the downloaded bytes with the release checksums |

This is a preview distribution. Consult the release's measured client coverage
before relying on a particular host or operation. While the repository is private,
downloads require repository access; the maintainer can supply the same reviewed
ZIP directly. A customer does not need to build it. The installed guides and
runtime scripts work without repository access. A ZIP is not itself a connector
or a hosted plugin installation.

## Account, purchase and workspace

Start from the [official Finsweet Account page](https://finsweet.com/products/account).
Choose **Create Account** if new or **Log in** if an account already exists. Complete
sign-in on the official page, never in chat. Use the same sign-in method originally
used for the purchase. If it fails, use the recovery controls actually shown there;
do not invent a password-reset address or ask for a verification code.

After login, open Consent Pro from the account/product interface and check the
workspace shown. The [Web App guide](https://docs.consentpro.com/web-app/) describes
Projects and Billing. If a purchase is missing, check the account, workspace and
domain assignment in [Plans](https://my.finsweet.com/plans), following the
[license guide](https://docs.consentpro.com/web-app/licenses). Investigate the existing
purchase before suggesting another. Changing a license assignment needs its own
confirmed target and authorization.

For an unresolved access problem, use [Talk to Expert](https://consentpro.com/talk-to-expert)
or the [official forum](https://forum.finsweet.com/). Do not post receipts, tokens,
private account details or a full container export in a public forum. Assisted
implementation has a [public service page](https://consentpro.com/implement-for-us);
confirm the customer's current entitlement and service terms before saying it is
included. The agent can prepare a private handoff but sends nothing unless asked.

You can begin planning or inspecting a site before buying. Current public
[Web App licensing](https://docs.consentpro.com/web-app/licenses) describes temporary
Preview in the open tab, not a free custom-site domain for visitors. The separate
[Webflow test-domain rule](https://docs.consentpro.com/webflow/licenses) must not be
generalized to custom sites. These public sources were checked on 2026-10-16.

## Choose the environment

| Environment | Entry and scope |
|---|---|
| Customer service | Use the official account/product entry above. This release has not verified a production MCP endpoint; use the dashboard route when no approved connector is available |
| Consent Pro product development staging | Only for an invited tester using the [staging connection instructions](#connect-consent-pro-staging-separately); separate account/workspace data may apply |
| Customer test website | The customer's own test hostname, project and container. It does not become Consent Pro's internal staging and does not imply a free production license |

Confirm the environment before connecting or changing anything. An unavailable
connector does not stop guided Consent Pro or GTM dashboard work. Installing
instructions, signing in to Consent Pro, connecting Google and editing the site
are separate steps.

## Start in your current chat

You do not need to understand MCP or write code before beginning. MCP is the connection
to Consent Pro; the skill is the procedure your assistant follows. A plugin can bundle
both. Google access for GTM is another connection, and site editing needs its own access.

Paste this into the assistant you want to use, replacing the website:

> Help me set up Consent Pro for example.com using
> https://github.com/redeuno/consentpro-gtm-ai. Read its current README and client journey.
> First check which instructions, Consent Pro tools, Google connection and site access
> are available in this conversation. Guide me through anything missing one step at a
> time, explain what success looks like and verify each result. Inspect what already
> exists before proposing changes. Prepare the exact changes for approval, then carry
> out the approved work and continue. Do not publish or send reports by email unless
> I explicitly request it. Speak in my language.

If the assistant cannot open the repository, give it the reviewed skill package or
relevant guide through its supported upload path. It must say when it cannot read the
instructions. Reading a document for one chat is useful but is not a persistent installation.

For an experienced customer, add: "Use a concise plan, skip already verified setup,
and show exact changes and remaining dependencies." This changes the explanation style;
it does not choose Basic or Advanced Google Consent Mode.

Before saying setup is ready, the agent must distinguish these checks:

| Layer | Evidence in this conversation |
|---|---|
| Instructions | The agent can load the Consent Pro entrypoint and its linked references from the actual installed package or provided files |
| Consent Pro access | An authenticated project read succeeds, or the manual route records the workspace/project and what dashboard evidence was inspected |
| GTM access | The intended container and available Google/dashboard access are confirmed, when GTM is part of the request |
| Site access | Public inspection, authorized code/dashboard editing and browser tests are identified separately |

Successful project listing does not prove a skill is loaded or Google is connected.
Do not delete a working connector just to add missing instructions. Prefer updating the
intended plugin when that supported path preserves the connection, then verify both layers.

## Choose the client path

| Where you are | Instructions | Connection |
|---|---|---|
| ChatGPT Chat or Work | Use the intended plugin's bundled skill; creation/editing requires the available Plugin Creator and edit access | Connect the approved environment if available, or use the guided dashboard route |
| Claude web or Desktop chat | Upload and enable the reviewed skill ZIP through Customize, Skills | Add the custom remote connector and enable it in the conversation |
| Codex local app or CLI | Extract the reviewed skill folders into the skill directory below, or use a supported plugin | Add the approved remote MCP in settings/CLI, or continue manually |
| Claude Code | Extract the reviewed skill folders into its skill directory | Add the approved remote MCP with the CLI, or continue manually |

Use the controls available to the actual account. Organization policies can restrict skills,
plugins or connectors; explain the required administrator action instead of promising a
menu that is not available. A file installed on a laptop is not automatically uploaded to
a hosted chat. Browser automation and local scripts are also host-dependent capabilities.

### ChatGPT: keep instructions and MCP in the intended plugin

Open Plugins and inspect the intended plugin's contents. If it already has the authenticated
Consent Pro MCP, edit that plugin to add or update the instructions rather than creating a
second lookalike. With Plugin Creator and edit access, use a request such as:

> Update this Consent Pro plugin from the reviewed consentpro-gtm-ai source. Use the
> primary consent-pro skill and bundle the GTM specialist, linked guides and runtime
> scripts with working relative paths. Preserve the existing staging MCP and connection
> configuration. Do not delete or recreate the connector. Identify the source commit
> or package you used and any installation you could not verify. This request changes
> the assistant package only, not a customer's Consent Pro project, GTM or website.

Review the saved plugin, install it if prompted, start a new conversation and select it
with `@`. Test instruction loading and a read-only project query separately. Only report
the update complete after inspecting the resulting plugin; a builder's promise is not
evidence. Updating this GitHub repository does not update an existing hosted plugin.
Where the host supports an onboarding skill, the plugin maintainer can set
`extensions.com.openai.onboardingSkill` to `./skills/consent-pro/SKILL.md` in the
existing legacy plugin manifest. Preserve its App/MCP binding and presentation.
Test the actual installation/update flow and a new conversation: this host feature
does not turn a standalone MCP connection into a universal automatic agent. See
[onboarding skills](https://developers.openai.com/plugins/build/plugins#add-an-onboarding-skill).
Sources: [Build plugins](https://learn.chatgpt.com/docs/build-plugins) and
[Install and use plugins](https://learn.chatgpt.com/docs/plugins), checked 2026-10-16.

### Claude web or Desktop: upload the reviewed package

First verify the reviewed ZIP and manifest using the checks below. In Customize,
Skills, open Add Skill (`+`) and choose Upload Skill, then select the generated
`consent-pro-0.2.0-preview.zip` and enable it. The primary package includes the GTM reference and its
scripts; the specialist ZIP is available for direct GTM tasks. Each ZIP must contain
its named skill folder, including `SKILL.md` and all bundled dependencies. Do not upload
the entire repository as if it were one skill.

Code execution and skill availability may need enabling in account or organization
settings. In a new chat, explicitly ask to use Consent Pro and verify the instructions
were loaded. This does not authenticate the MCP or grant access to your local computer.
The web interface inspected on 2026-10-16 offered Upload Skill directly in Add Skill;
some documented interfaces put upload under Create skill. Match the customer's screen.
Sources: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
and [Package a custom skill](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills),
checked 2026-10-16. These are documented paths, not a completed Claude web/Desktop
acceptance test.

For an update, preserve the previous reviewed ZIP and any local customization,
verify the replacement, and inspect the existing skill's available update controls.
If the host offers no replacement control, disable the old copy before uploading
the new one. Do not leave two active copies with the same purpose. Start a new
conversation and verify the loaded manifest before retiring the old copy. If a
name conflict prevents import, keep the previous ZIP for recovery and confirm the
exact old skill before removing it and retrying the upload.

To stop using a skill, open its details in Customize, Skills and turn its toggle
off. For removal, open the adjacent `...` menu, select Delete and confirm the exact
skill. This affects instructions, not separately connected accounts. Re-upload the
previous reviewed ZIP to restore the skill if needed. Shared or organization-managed
skills may require their owner to update them. If controls differ, inspect the
current screen rather than deleting another item. This update/recovery procedure
still requires host-specific acceptance.

### Codex and Claude Code: install the ready folder

1. Download and extract the primary ZIP. Its top-level folder is `consent-pro`.
2. Before installation, verify `package-manifest.json` and the archive checksum:
   version, channel, source commit and file hashes must match the reviewed delivery.
3. For Codex, place that folder in `~/.agents/skills/`, or `.agents/skills/` in the
   intended project. For Claude Code, use `~/.claude/skills/` or the project's
   `.claude/skills/`. The specialist can be installed beside it in the same way.
4. Start a new session. Invoke `$consent-pro` in Codex or `/consent-pro` in Claude
   Code. Ask it to read the bundled installation and onboarding references.
5. Ask the agent to read the installed manifest and confirm the expected revision.
   Discovery alone does not prove the instructions were followed or an account
   connected. Continue with the applicable connector or manual route.

If that folder already exists, compare it with the new package and preserve local
changes before replacement. To remove the skill, delete only its reviewed folder.
This does not revoke account connections. Do not edit either host's other skills
or global settings as part of this installation.

## Maintainers: build reproducible packages

This section is for an agent or maintainer with a terminal and a reviewed repository
checkout. A beginner in web chat can use a supplied package and the UI paths above.
If no package or terminal is available, follow the guides for this conversation and ask
the maintainer for the package; do not pretend a persistent skill has been installed.

Review the checkout, then use Python 3.10 or newer. The installer copies only
explicit runtime scripts and authored guides. It excludes credentials, customer
maps, test fixtures and the source archive. Each skill contains its dependencies
and a checksum manifest. Neither package needs the original checkout at runtime.

From the repository root, preview the local installation:

```bash
python3 scripts/package-skills.py --output ~/.agents/skills
```

For Codex, apply that same destination:

```bash
python3 scripts/package-skills.py --output ~/.agents/skills --apply
```

For Claude Code, preview and apply its skill directory:

```bash
python3 scripts/package-skills.py --output ~/.claude/skills
python3 scripts/package-skills.py --output ~/.claude/skills --apply
```

Project-scoped alternatives are `.agents/skills` for Codex and `.claude/skills`
for Claude Code, inside the client's project. Start a new session after installing.
Invoke `$consent-pro` or `$consent-pro-gtm` in Codex; use `/consent-pro` or
`/consent-pro-gtm` in Claude Code. Open the installed `SKILL.md` if discovery fails.
An organization may restrict custom skills. Installing a local folder does not
install it into a hosted chat account or grant any MCP permission.

Locations verified against [Codex skills](https://learn.chatgpt.com/docs/build-skills)
and [Claude Code skills](https://code.claude.com/docs/en/skills) on 2026-10-16.

The installer refuses to replace different existing files. For an upgrade, build
into a fresh output directory, compare with the installed package, preserve any
local customization, then deliberately replace the old skill folder. Identical
runs are no-ops. To uninstall, remove only the two reviewed package folders.
This does not revoke OAuth grants or disconnect MCP accounts.

### Produce uploadable ZIP files

Use a clean reviewed commit. Preview first, then explicitly write the output:

```bash
python3 scripts/package-skills.py --output dist/skills --archives dist --channel preview
python3 scripts/package-skills.py --output dist/skills --archives dist --channel preview --apply
```

The builder writes named version/channel archives and `SHA256SUMS`, and refuses
different existing output. Use a fresh output directory for upgrades. The manifest
records release version, channel, source commit, dirty state and hashes. Preview
and stable builds require clean source; use `--channel development` for local work
in progress and do not relabel that output as a reviewed release. Rebuild twice
from the same clean commit and compare hashes before distribution.

After extracting the ZIP, compare each file with its manifest before installation.
On macOS, `shasum -a 256 -c SHA256SUMS` checks the archives; on Linux use
`sha256sum -c SHA256SUMS`. On Windows, `Get-FileHash <archive> -Algorithm SHA256`
can be compared with the corresponding entry. A checksum detects changed bytes;
obtain the checksum and archive from the reviewed release or trusted maintainer.
These commands do not install into an account or connect a service.

## Connect Consent Pro staging separately

The tested endpoint is `https://mcp-staging.consentpro.com/mcp`, using Streamable
HTTP and OAuth. Use the Finsweet staging account and the intended workspace.
No API key is required. Do not infer a production URL from this staging address.

- Codex: Settings, MCP, Add MCP Server; name it `Consent Pro staging`, select
  Streamable HTTP, enter the endpoint, save and authenticate. The terminal
  alternative is `codex mcp add consent-pro-staging --url https://mcp-staging.consentpro.com/mcp`,
  followed by `codex mcp login consent-pro-staging`. Use `codex mcp --help` if the
  installed client differs.
- Claude web or Desktop: Customize, Connectors, Add, Custom, Web; use the same
  name and endpoint. Older client instructions may call this Settings, Connectors,
  Add custom connector. Review the detected authentication, choose Sign in now and
  Claude's published identity when offered, then complete Finsweet authorization.
  Enable the connector for the conversation. See [Claude connectors](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities).
- Claude Code: in the intended project, run
  `claude mcp add --transport http consent-pro-staging https://mcp-staging.consentpro.com/mcp`.
  Open `/mcp` in Claude Code to authenticate. If the server already exists, inspect it
  rather than adding a duplicate. See [Claude Code MCP](https://code.claude.com/docs/en/mcp).
- ChatGPT: add the remote MCP through the custom app/plugin controls available
  to your account and workspace, then complete OAuth. UI labels and availability
  vary by account. The local installer above does not deliver a hosted ChatGPT
  plugin or upload skills. Use the hosted plugin instructions above and verify both
  the loaded instructions and the connected tools in a new chat.

Read the actual authorization screen. Read-only Consent Pro access may exclude
GTM; select the specific GTM permission when offered, or the intended broader
preset, then connect Google separately. Full access does not bypass Google roles
or add permissions that did not exist when an older connection was authorized.
For editing releases, verify the real tools and both grants through
[the evolving GTM path](../06-agent-readiness/operations.md#future-gtm-writes).
If public MCP documentation is unavailable, inspect the connected tool contracts
and server documentation. Do not infer production permission parity from staging.
To change access, remove and reconnect as directed by the staging flow. Full access does not
authorize an agent to make unsolicited changes. A missing permission requires
reconnection or a guided manual path, not an automatic credential fallback.

Use the dedicated test dashboard:
`https://mcp-docs-and-ui-consentpro-web-app-staging.finsweet.workers.dev/`.
Keep the project's dashboard open to compare saved state. The complete dated
[capability contract](../06-agent-readiness/operations.md) distinguishes drafts,
scans, email requests and unsupported publication/category edits.

After sign-in, list the projects, resolve the intended workspace/project/hostname and
read that project's setup. If none match, verify workspace and pagination before offering
project creation. Do not create a duplicate to work around an access problem. For GTM,
continue with [Connect Google Tag Manager](../06-agent-readiness/operations.md#connect-google-tag-manager),
which is separate from Finsweet OAuth. Confirm the returned containers after Google login.

## Recover a missing layer

| Symptom | Next action and success check |
|---|---|
| Tools work but instructions are absent | Inspect the selected plugin/skill, add or enable the reviewed package, start a new conversation and confirm its references can be read; preserve the working connector |
| Instructions load but tools are absent | Enable/authenticate the intended connector if the customer wants it; otherwise continue with dashboard guidance and label reported versus inspected evidence |
| Consent Pro works but GTM is disconnected | Use GTM status and its private user-opened connection flow, then re-read status and containers |
| Expected project/container is missing | Check workspace, Google account and completed pagination; have the appropriate administrator resolve missing access |
| Changes fail with read-only access | Present the exact pending change and reconnect with the necessary scope or guide the approved manual path; do not switch credentials silently |
| Package may be outdated | Compare actual installed content with a known source package; do not infer freshness from the plugin name or a test count |
| No browser or site access | Complete supported reads, prepare the exact code/manual handoff and mark deployment and behavior unverified |

Use the [onboarding checkpoint](../reference/onboarding.md#start-and-resume) to resume after the
missing layer is restored. Do not restart every connection or repeat a scan by default.

## First read-only conversation

Replace the hostname and workspace with the customer's target:

> Use Consent Pro staging. My test website is example.com in the selected workspace.
> Inspect the current setup and tell me what is missing. Ask before changes and do
> not publish anything. Distinguish measured state from checks you could not run.

Confirm that the agent resolves the exact project, follows pagination and reports
the installed runtime and remaining steps. With the separate GTM permission and
Google connection available, a published GTM audit must be labeled as published,
not as the current workspace. Then ask for a draft change while
connected read-only: the agent should explain missing access without performing it.
With no connector, it should offer connection instructions and public inspection,
not pretend it listed private websites.

After granting a specific draft edit, compare the saved value with the dashboard.
Preview links are private and temporary. Separately verify behavior in the browser.
Do not run export/proof email tests unless the customer explicitly requests them.

## Maintain the package and capability boundary

These are maintainer-checkout commands. The installed skill intentionally excludes
the builder, drift checker, test suite and source archive. Use the original
repository to maintain or rebuild packages, not the installed skill folder.

Edit the canonical skills under `skills/consent-pro/` and `skill/`, and their
shared guides/scripts. Regenerate packages instead of editing generated copies.
See [tests](../../tests/README.md) for local checks. Raw source collections and
authenticated catalogues belong in the maintainer's approved private evidence home,
outside this repository and every customer package.

Capture a new sanitized MCP catalogue through the client's native discovery when
the server changes. Do not save credentials, connection links or project records.
Compare it to the dated baseline:

```bash
python3 scripts/check-mcp-catalogue.py \
  /path/to/private/reviewed-catalogue.json \
  /path/to/new-catalogue.json
```

A changed description, schema, annotation or tool list fails this check and requires
review. Classify each changed operation by effect and required grants. Added GTM writes
are not enabled merely by discovery. Follow the operation-specific
[acceptance contract](../06-agent-readiness/operations.md#future-gtm-writes) in an isolated
test container before offering them to a client. Record the reviewed server/environment,
contract hash or revision, operations, permission requirements, observed results and
remaining manual paths. A release announcement is not this evidence. Keep the dated
baseline and record a new snapshot instead of rewriting history. Update the shared
guides, rebuild both packages and update the hosted plugin separately; then verify
loaded instructions and the actual connected contract in a new client session.
