# Install the client skills

This is the home for client installation and package maintenance. The repository
previously had a GTM skill but no self-contained installer. The broader
[journey](../00-the-journey.md) and [operations](../06-agent-readiness/operations.md)
remain the sources for product behavior; this page covers delivery to an agent.

## Build once, use in either terminal client

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

## Connect Consent Pro staging separately

The tested endpoint is `https://mcp-staging.consentpro.com/mcp`, using Streamable
HTTP and OAuth. Use the Finsweet staging account and the intended workspace.
No API key is required. Do not infer a production URL from this staging address.

- Codex: Settings, MCP, Add MCP Server; name it `Consent Pro staging`, select
  Streamable HTTP, enter the endpoint, save and authenticate. The terminal
  alternative is `codex mcp add consent-pro-staging --url https://mcp-staging.consentpro.com/mcp`,
  followed by `codex mcp login consent-pro-staging`. Use `codex mcp --help` if the
  installed client differs.
- Claude web or Desktop: Settings, Connectors, Add custom connector; use the same
  name and endpoint. Sign in using Claude Published Identity when offered, then
  finish Finsweet authorization. Enable or mention the connector in the conversation.
- ChatGPT: add the remote MCP through the custom app/plugin controls available
  to your account and workspace, then complete OAuth. UI labels and availability
  vary by account. The local installer above does not deliver a hosted ChatGPT
  plugin or upload skills. Use the connected MCP with the starter prompt below;
  packaging a hosted plugin is a separate delivery step.

Select Read only for Consent Pro diagnosis without GTM. GTM is excluded from that
preset: choose Custom with **View Google Tag Manager**, or Full access, then link
the Google account separately. Google access through this MCP remains read-only.
Use Full access or the necessary Custom scopes for supported CP changes. See the
[MCP permissions](https://docs.consentpro.com/mcp/) and
[Google connection guide](https://docs.consentpro.com/mcp/google-tag-manager).
To change access, remove and reconnect as directed by the staging flow. Full access does not
authorize an agent to make unsolicited changes. A missing permission requires
reconnection or a guided manual path, not an automatic credential fallback.

Use the dedicated test dashboard:
`https://mcp-docs-and-ui-consentpro-web-app-staging.finsweet.workers.dev/`.
Keep the project's dashboard open to compare saved state. The complete dated
[capability contract](../06-agent-readiness/operations.md) distinguishes drafts,
scans, email requests and unsupported publication/category edits.

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
