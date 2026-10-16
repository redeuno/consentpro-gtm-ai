# Start the Consent Pro instructor in your client

This is the home for client installation and package maintenance. The repository
previously had a GTM skill but no self-contained installer. The broader
[journey](../00-the-journey.md) and [operations](../06-agent-readiness/operations.md)
remain the sources for product behavior; this page covers delivery to an agent.

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
| Consent Pro access | Tool discovery and an authenticated project read for the selected workspace succeed |
| GTM access | Google connection status and the intended container are confirmed, when GTM is part of the request |
| Site access | Public inspection, authorized code/dashboard editing and browser tests are identified separately |

Successful project listing does not prove a skill is loaded or Google is connected.
Do not delete a working connector just to add missing instructions. Prefer updating the
intended plugin when that supported path preserves the connection, then verify both layers.

## Choose the client path

| Where you are | Instructions | Connection |
|---|---|---|
| ChatGPT Chat or Work | Use the intended plugin's bundled skill; creation/editing requires the available Plugin Creator and edit access | Connect its staging MCP, then verify it in the new chat |
| Claude web or Desktop chat | Upload and enable the reviewed skill ZIP through Customize, Skills | Add the custom remote connector and enable it in the conversation |
| Codex local app or CLI | Install the generated skill folders with the local commands below, or use a supported plugin | Add the remote MCP in settings or with the CLI |
| Claude Code | Install the generated skill folders in its skill directory | Add the remote MCP with the CLI and authenticate |

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
Sources: [Build plugins](https://learn.chatgpt.com/docs/build-plugins) and
[Install and use plugins](https://learn.chatgpt.com/docs/plugins), checked 2026-10-16.

### Claude web or Desktop: upload the reviewed package

In Customize, Skills, use `+`, Create skill, Upload a skill, then select the generated
`consent-pro.zip` and enable it. The primary package includes the GTM reference and its
scripts; the specialist ZIP is available for direct GTM tasks. Each ZIP must contain
its named skill folder, including `SKILL.md` and all bundled dependencies. Do not upload
the entire repository as if it were one skill.

Code execution and skill availability may need enabling in account or organization
settings. In a new chat, explicitly ask to use Consent Pro and verify the instructions
were loaded. This does not authenticate the MCP or grant access to your local computer.
Sources: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
and [Package a custom skill](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills),
checked 2026-10-16. These are documented paths, not a completed native-Claude acceptance test.

## Build once, use in either terminal client

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

Run these from the repository root, using a fresh `dist/skills` when upgrading:

```bash
python3 scripts/package-skills.py --output dist/skills
python3 scripts/package-skills.py --output dist/skills --apply
python3 -m zipfile -c dist/consent-pro.zip dist/skills/consent-pro
python3 -m zipfile -c dist/consent-pro-gtm.zip dist/skills/consent-pro-gtm
```

The ZIP commands write local archives and replace archives at those exact output paths.
They do not install into an account or connect a service. Keep the source commit with
the delivery and verify the ZIP against `package-manifest.json` before upload. The
manifest records file hashes, not a release version. Comparing it to a newly built
package from a known source establishes which content is installed. A reported number
of passing tests does not identify an installed version.

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

Select Read only for diagnosis, or Full access for supported mutations. To change
access, remove and reconnect as directed by the staging flow. Full access does not
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
| Instructions load but tools are absent | Enable the intended connector in this conversation, authenticate if required and perform a read-only project query |
| Consent Pro works but GTM is disconnected | Use GTM status and its private user-opened connection flow, then re-read status and containers |
| Expected project/container is missing | Check workspace, Google account and completed pagination; have the appropriate administrator resolve missing access |
| Changes fail with read-only access | Present the exact pending change and reconnect with the necessary scope or guide the approved manual path; do not switch credentials silently |
| Package may be outdated | Compare actual installed content with a known source package; do not infer freshness from the plugin name or a test count |
| No browser or site access | Complete supported reads, prepare the exact code/manual handoff and mark deployment and behavior unverified |

Use the [journey checkpoint](../00-the-journey.md#lead-the-next-step) to resume after the
missing layer is restored. Do not restart every connection or repeat a scan by default.

## First read-only conversation

Replace the hostname and workspace with the customer's target:

> Use Consent Pro staging. My test website is example.com in the selected workspace.
> Inspect the current setup and tell me what is missing. Ask before changes and do
> not publish anything. Distinguish measured state from checks you could not run.

Confirm that the agent resolves the exact project, follows pagination and reports
the installed runtime and remaining steps. A published GTM audit must be labeled
as published, not as the current workspace. Then ask for a draft change while
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
See [tests](../../tests/README.md) for local checks and
[source inventory](../06-agent-readiness/sources/2026-10-16/README.md) for coverage.

Capture a new sanitized MCP catalogue through the client's native discovery when
the server changes. Do not save credentials, connection links or project records.
Compare it to the dated baseline:

```bash
python3 scripts/check-mcp-catalogue.py \
  docs/06-agent-readiness/sources/2026-10-16/mcp-catalogue.json \
  /path/to/new-catalogue.json
```

A changed description, schema, annotation or tool list fails this check and
requires review. Added GTM writes are not enabled automatically. Validate their
targeting, concurrency, preservation, partial failure and publication behavior in
an isolated test container before offering them to a client. Keep the dated
baseline as evidence and record a new snapshot instead of rewriting history.
