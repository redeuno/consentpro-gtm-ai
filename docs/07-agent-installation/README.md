# Start the Consent Pro instructor in your client

This guide covers account entry, assistant installation and package updates. The
[journey](../00-the-journey.md) and [operations](../06-agent-readiness/operations.md)
remain the sources for product behavior; this page covers delivery to an agent.

For "install Consent Pro on my site", use client setup only to support the
[first activation](../00-the-journey.md). Reuse working access. Offer supported
connection once, and keep guided dashboard work available when it is declined,
deferred or unavailable. Persistent instructions are optional. For an explicit
"install the skill" or "connect MCP" request, complete that requested setup first.

## Optional: get the ready package

Download the reviewed assets from [release 0.3.12](https://github.com/redeuno/consentpro-gtm-ai/releases/tag/v0.3.12):

| Asset | Use |
|---|---|
| `consent-pro-0.3.12-preview.zip` | Start here for the whole Consent Pro journey, including GTM guidance |
| `consent-pro-gtm-0.3.12-preview.zip` | Optional specialist for focused GTM work |
| `SHA256SUMS` | Compare the downloaded bytes with the release checksums |

This is a preview distribution. Follow the host-specific procedure below and verify
the loaded instructions and available operations in the current conversation.
The installed guides and runtime scripts work without repository access. A ZIP is
not itself a connector or a hosted plugin installation. Check its
[checksum and manifest](#verify-the-package) before installation.

## Account, purchase and workspace

For an existing production Web App account, open [Consent Pro](https://app.consentpro.com/)
and retain the customer's selected workspace. For account creation or recovery,
use the [official Finsweet Account page](https://finsweet.com/products/account).
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
When the customer already chose Preview without buying, retain that choice and
continue the installation and tests it supports. Do not reopen purchase or require
a publication license for an independent Preview step. Check the actual operation's
requirements and returned errors; do not promise that every project can use Preview.
Record ordinary publication and its license separately as pending.
Preview does not publish its draft or prove that ordinary visitors see no banner.
An existing published banner may still appear. Before claiming what visitors see,
read the published state and check the ordinary URL without Preview in a permitted
browser. Report the observed scope; if either check is unavailable, keep that state
unverified.

## Choose the environment

| Environment | Entry and scope |
|---|---|
| Consent Pro production service | Web App: `https://app.consentpro.com/`. MCP: `https://mcp.consentpro.com/mcp`. Use the customer's production Finsweet account and selected workspace |
| Consent Pro product staging | Retain a separately named staging connection and the approved staging dashboard supplied for that testing round. It has separate account/workspace data; do not repoint it to production |
| Customer test website | The customer's own test hostname, project and container. It does not identify the Consent Pro account environment or imply a free production license |
| Customer production website | Confirm the project, license and publication authority before making changes that reach ordinary visitors |

Reuse the confirmed product environment, dashboard and project. If that evidence
is missing or conflicts, ask which service the customer is using before connecting
or changing anything. Do not redirect an agreed staging target to production. A public
site, a test hostname, a runtime URL or a comment in website code does
not authorize migration to another product environment. An unavailable
connector does not stop guided Consent Pro or GTM dashboard work. Installing
instructions, signing in to Consent Pro, connecting Google and editing the site
are separate steps.

For production integration testing, use a test website, workspace and GTM container
you own and can safely change. Do not use a customer's live project as a test fixture.
Testing access does not authorize project changes, publication or rollback.

For current custom-site setup, explain the
[three activation checkpoints](../06-agent-readiness/operations.md#current-first-installation-handoffs):
the script goes in the selected hostname's shared head, including its home page;
the initial banner and Consent Pro publication use reviewed MCP operations when
available and authorized, or that environment's dashboard for each missing step.
Do not assume that all three actions must be manual or that one available write
enables every other write. A landing-page URL does not establish
support for page-only installation. A subdomain uses its own home page, not the
parent domain's. Keep the original page URL for verification.

## Start in your current chat

The customer's ordinary request and repository link are enough to start. Read the
main skill and this procedure, then load other references only as the next step
needs them. Conduct the request in this conversation. Do not answer a setup request
with a repository overview, another prompt to copy, or a requirement to install
the skill before proceeding.
The longer procedure is for the agent, not an intake form for the customer.
A request to only consult limits changes; it does not turn setup into a repository
review. Honor narrower permissions and explain risks relevant to the current step.

Use known package/repository locations and available tool descriptions to establish
the host and access. Inspect the active manifest or instruction source once if
available; record a version mismatch without making reinstallation a gate. Recheck
after an update or conflicting instructions, not on every turn. Keep these checks
in the working record.

Use the relevant project read to resolve the target when possible. If the site or
environment is still unknown, ask for it before researching snippets, scanning a
whole account or delegating a full setup review. A documentation timeout must not
delay that question; retry or use a relevant maintained source when the operation
needs it. Do not infer a wrong account merely because only a test project appears.
Keep the first reply within about 100 words, with one question or one immediate
action. Explain only what that next step needs, not the whole installation journey
or a list of future warnings. A proposed change that requires a complete review
can exceed this limit; do not omit its effects to fit the word count.
Use the known evidence to choose that next step:

| Evidence already available | Next reply or action |
|---|---|
| Full setup request and this repository URL, connection route undecided | Read the guidance and briefly recommend supported connected setup with its dashboard alternative. Ask only the next fact needed to advance toward a first banner, such as the site or product environment. Offer the reusable skill at a useful pause |
| Website URL supplied | Keep the exact URL/path as the verification target alongside the project hostname. Inspect available evidence and reuse the project if connected. Offer the supported connection before asking for values it could read, but do not hold progress on optional installation. Ask for a missing platform only when the site-editing step needs it |
| Customer says they already have a Consent Pro account | Keep that fact as reported and continue the current step. Do not restart signup or send an unrelated purchase/workspace checklist |
| Customer asks to install the skill or connect MCP first | Prepare that requested client setup, using the Claude or other host procedure below. Do not block it on a website URL |
| Consent Pro tools already work | Read the relevant project; resolve ambiguity rather than asking the customer to reconnect |
| Customer asks about the panel or its menus | Use [project data and documented navigation](../06-agent-readiness/operations.md#dashboard-data-and-menus); do not imply that API results show the visual interface |
| Consent Pro tools are absent and a verified connector route applies | Recommend that connection for full setup, explain what it lets the agent do, and guide it when accepted or already requested. If unavailable or declined, continue through the dashboard |
| Customer already declined or deferred a connector, or cannot add it | Keep that choice, guide the manual route and continue independent reads; do not repeatedly offer reconnection |
| Customer reports a skill or connector was installed | Refresh the relevant discovery/read, state what is actually verified, and resume the existing step without requesting the same known details |

Use the connection choice below for a full setup request. Missing tools alone do
not select a manual route, but an unanswered optional skill offer is not a waiting
gate. A supplied URL or a request to test first does not select the manual route.
Do not end by waiting for connector setup unless the customer chose that route.
Ask for the missing site URL when that advances the current step and inspect it.
Adapt the next action to actual evidence; do not claim a read that did not happen
or invent an installation duration.

If reading GitHub fails, describe that retrieval failure accurately. A fetch
failure or a 404 does not establish whether the repository is private, deleted
or misspelled. When available, try one alternative public-content reader, such as
Firecrawl for a public URL, or the repository's known raw README path. Do not send
private files or authentication credentials to a scraping service. If the content
still cannot be read, request the reviewed ZIP or relevant guide once and explain
the limitation. Do not guess GTM container imports or snippets from the repo name.

Instructions read from the repository or a supplied package can guide this chat.
Persistent installation is optional unless the customer requested it. Explain MCP
as the Consent Pro connection when it becomes relevant; introduce the separate
Google and site-editing access at the step that needs them. Keep technical detail
and full progress tables for a requested status report, a material handoff or a
genuinely complex situation. Experience does not choose Basic or Advanced Consent Mode.

Before saying setup is ready, the agent must distinguish these checks:

| Layer | Evidence in this conversation |
|---|---|
| Instructions | The agent can read the Consent Pro entrypoint and its linked references from the repository, provided files or actual installed package |
| Consent Pro access | An authenticated project read succeeds, or the manual route records the workspace/project and what dashboard evidence was inspected |
| GTM access | The intended container and available Google/dashboard access are confirmed, when GTM is part of the request |
| Site access | Public inspection, authorized code/dashboard editing and browser tests are identified separately |

Successful project listing does not prove a skill is loaded or Google is connected.
For missing instructions, read the repository or supplied guides and continue here.
Do not delete a working connector. If the customer requests or accepts persistent
installation, update the intended plugin when that supported path preserves the
connection, then verify both layers.

### Choose how the assistant will work

For full setup, recommend connecting Consent Pro so the assistant can read the
selected project and perform supported changes within the customer's authorization.
Explain MCP as that account connection. Offer the reviewed skill once to keep the
procedure available in future chats; reading it already supports this conversation.
Make the skill offer at a natural pause without requiring an answer before site
setup can continue. These are recommendations, not conditions for getting help
or proof of any access.

Use [one next decision at a time](../reference/onboarding.md#ask-for-the-next-decision).
Prefer a native question tool when available and permitted, with ordinary text as
the fallback. The same procedure applies in terminal and web chat; installing this
skill does not add question controls. A URL request usually needs free text,
while a connection choice can use two short options.

Choose the next action from the known state:

- If the connector already works, reuse it and resolve the project. Offer missing
  persistent instructions without reinstalling a working connection or stopping
  the first-publication path.
- If the environment and endpoint are verified, recommend connecting now and ask
  about the route only when the next step needs project access. If a missing site
  URL enables a useful public read first, ask for that URL instead. Do not combine
  the URL request with a connection choice. If connection is already accepted or
  requested, proceed to the host's setup steps without asking again.
- If the environment is unknown, ask which Consent Pro dashboard/service the
  customer is using, without private URL parameters. For confirmed production,
  use the official URL in [Connect Consent Pro](#connect-consent-pro). For product
  staging, retain that environment's approved entry. If the route is unavailable,
  explain the limit and continue through its dashboard. Do not substitute environments.
- If connection was declined, deferred or is restricted, preserve that choice. Continue
  useful reads and manual steps. Do not make the reusable skill mandatory either.

When the next step needs project access and the route is undecided, explain:
"Connecting Consent Pro lets me read your project and carry out changes you authorize."
Then ask: "How would you like to continue?" Offer "Connect Consent Pro (recommended)"
and "Guide me in the dashboard" through the permitted question control or text.
Keep the optional skill offer for a useful pause instead of adding another decision.
If a missing site URL enables the next useful public read, ask for that URL first.
Keep the route undecided; a URL does not select dashboard setup or reject connection.
Verify the product environment before giving a connector endpoint. When unknown,
ask the one question needed to identify it at that step. Do not ask about the
website, skill, Google and licensing together.

After the customer accepts, guide MCP setup, complete the customer-operated login,
refresh discovery and verify a project read. Return to the first incomplete site
step. Supply the ready ZIP if wanted, without making upload the next compulsory
task. If declined or deferred, continue using the loaded guide.
Google authorization follows when GTM is relevant. Record the route so a later
"done" resumes the task rather than reopening every choice.

For a customer who wants the banner first, a reply can be:
"We can get the initial banner working and adjust its appearance afterward.
Connecting Consent Pro lets me read the project and carry out supported changes;
I can also guide you through its dashboard. What is the website address?"
Adapt this to known facts; do not ask for an address already supplied or offer an
unverified endpoint. If the customer explicitly requests connection first, honor it.

## Choose the client path

| Where you are | Instructions | Connection |
|---|---|---|
| ChatGPT Chat or Work | Use the instructions already read; optionally save them in the intended plugin with available Plugin Creator and edit access | Connect the approved environment if available, or use the guided dashboard route |
| Claude web or Desktop chat | Use the instructions already read for this chat; optionally upload the reviewed ZIP to reuse them | Reuse a working connector, guide the supported account setup, or continue manually |
| Codex local app or CLI | Use the instructions already read; optionally install the reviewed skill folders or a supported plugin | Add the approved remote MCP in settings/CLI, or continue manually |
| Claude Code | Use the instructions already read; optionally install the reviewed skill folders | Add the approved remote MCP with the CLI, or continue manually |

Use the controls available to the actual account. Organization policies can restrict skills,
plugins or connectors; explain the required administrator action instead of promising a
menu that is not available. A file installed on a laptop is not automatically uploaded to
a hosted chat. Browser automation, question controls and local scripts are also
host-dependent capabilities. Do not assume Claude Code tools exist in Claude web,
or that a Codex question tool is enabled in every operating mode. Respect the
actual tool contract, including whether it accepts approval requests.

### ChatGPT: keep instructions and MCP in the intended plugin

Use this section when connection or persistent installation is requested or accepted.
Otherwise, read the guides and continue website setup in the current conversation.
Inspect the intended plugin first. Reuse its authenticated Consent Pro connection
and update its instructions when requested, instead of creating a second lookalike.

For a new production connection in ChatGPT Work on the web, use the native account
flow documented in the [plugin quickstart](https://developers.openai.com/plugins/quickstart):

1. Open **Plugins**, select **Add** (`+`), then **Add custom MCP server**.
2. Enter **Consent Pro**, server URL `https://mcp.consentpro.com/mcp`, and **OAuth** authentication.
   If a transport choice appears, use **Streamable HTTP**.
3. Have the customer review the trust notice and choose **Create as a plugin**.
   If **Connect Consent Pro** appears afterward, continue through it. The customer
   completes **Continue with Finsweet**, selecting the intended workspace and
   [access level](#choose-access-and-authorize). Creating the plugin alone does not
   complete this authorization.
4. Open the resulting plugin under personal plugins and install it if prompted.
5. Start a new **Work** conversation, select the plugin with `@`, and verify an authenticated project read.

After creation, obtain the resulting `plugin_asdk_app...` ID from the plugin page
or supported metadata. With Plugin Creator and edit access, add the reviewed skills
to that registered connection. Preserve its App mapping and OAuth configuration.
Do not invent an ID, copy a staging binding or replace the authenticated connection
with a standalone archive. Use a request such as:

> Update this Consent Pro plugin from the reviewed consentpro-gtm-ai source. Use the
> primary consent-pro skill and bundle the GTM specialist, linked guides and runtime
> scripts with working relative paths. Preserve the existing approved MCP and connection
> configuration. Do not delete or recreate the connector. Identify the source commit
> or package you used and any installation you could not verify. This request changes
> the assistant package only, not a customer's Consent Pro project, GTM or website.

If the existing plugin is bound to staging and the customer requests production,
keep staging clearly named and configure a separate production connection using
the host's supported account controls. Do not relabel a staging App as production
or replace an App binding through a skill-only update. Add the reviewed instructions
to the intended production plugin when that workflow is supported. If the host
requires the customer to add or authorize the connection, guide that step and
verify it afterward. A saved plugin is not an authenticated connection.

Verify the resulting instructions and authenticated project read separately in the
intended host. A standalone package may exist alongside the registered connection.
Saving it, opening its page or seeing an MCP entry does not prove installation or
availability in the Work web picker. If only a desktop launch is offered, check
that package's supported host and installation state. Do not infer that all
standalone plugins are incompatible with web chat from that observation.

Report which checks succeeded: package saved, plugin selectable, instructions loaded
and authenticated read. Keep any incomplete check explicit. Updating this repository
does not update an existing hosted plugin. The registered connection and skill
mapping are documented in [Package your plugin](https://developers.openai.com/plugins/build/plugins);
host and account availability are described in
[Plugins in ChatGPT](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt).
These OpenAI sources were checked on 2026-10-29. If controls differ or are restricted,
inspect the available account controls and continue the guided dashboard route when needed.

### Claude web or Desktop: upload the reviewed package

Use this section when the customer asks or accepts the offer to save the skill
for future chats. Keep website setup in the current conversation when persistent installation is not
requested. The default Claude chat path is guided installation through account
settings. Do not assume it has ChatGPT's Plugin Creator or permission to operate
its own account settings. If a supported account-management or browser tool is
actually present, inspect its capabilities and use it within the user's scope;
otherwise prepare the files and guide only the clicks the customer must perform.

When download and file tools are available, retrieve the primary reviewed ZIP and
its checksum, validate them, inspect its manifest, and provide the ready file or
the exact release asset link. If a read-only tool cannot download binary files,
give the direct download action without claiming a completed download or checksum.
Do not make the customer prepare the archive or upload the whole repository.
Tell them which of these steps succeeded in one brief sentence, then guide upload.

When file tools are available, first verify the reviewed ZIP and manifest using
the checks below. Otherwise provide the reviewed asset link and keep byte
verification marked unavailable. In Customize,
Skills, open Add Skill (`+`) and choose Upload Skill, then select the reviewed
`consent-pro-0.3.12-preview.zip` and enable it. The primary package includes the GTM reference and its
scripts; the specialist ZIP is available for direct GTM tasks. Each ZIP must contain
its named skill folder, including `SKILL.md` and all bundled dependencies. Do not upload
the entire repository as if it were one skill.

Code execution and skill availability may need enabling in account or organization
settings. Explicitly ask to use Consent Pro and verify the instructions were loaded;
use a new chat only if the host needs it to load the change. This does not
authenticate the MCP or grant access to your local computer.
Some interfaces put upload under Create skill. Match the customer's screen.
Sources: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)
and [Package a custom skill](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills),
checked 2026-10-16. Verify loading in the customer's current host before reporting
installation complete.

After the customer says "installed", inspect the active skill or manifest if the
host exposes it. If this conversation cannot refresh its skills, give a short
resume message for a new chat containing the already-known site and current step.
Do not force a new chat solely to repeat onboarding when the loaded instructions
already work. A user report without inspection remains reported, not verified.

For an update, preserve the previous reviewed ZIP and any local customization,
verify the replacement, and inspect the existing skill's available update controls.
If the host offers no replacement control, disable the old copy before uploading
the new one. Do not leave two active copies with the same purpose. Verify the
loaded manifest, using a new conversation only if the host needs it to load the
update, before retiring the old copy. If a
name conflict prevents import, keep the previous ZIP for recovery and confirm the
exact old skill before removing it and retrying the upload.

To stop using a skill, open its details in Customize, Skills and turn its toggle
off. For removal, open the adjacent `...` menu, select Delete and confirm the exact
skill. This affects instructions, not separately connected accounts. Re-upload the
previous reviewed ZIP to restore the skill if needed. Shared or organization-managed
skills may require their owner to update them. If controls differ, inspect the
current screen rather than deleting another item. Verify the resulting loaded
revision after an update or recovery.

### Claude web or Desktop: connect when available

Missing Consent Pro tools in the current chat does not prove that the account
cannot add connectors. Recommend the connected route for full setup using the
choice above. Once accepted or already requested, use the verified
environment's endpoint and guide Customize, Connectors, Add. Inspect the actual
controls before choosing Add custom connector or Custom, Web; labels vary. In an
organization, an owner may need to add the connector before a member can connect
their account. After authentication, enable it for the conversation and perform a
read to verify the intended workspace. For confirmed production, use
`https://mcp.consentpro.com/mcp`; for staging, preserve its separate entry.
Do not ask for secrets in chat or treat a saved connector as an authenticated read.

If the customer cannot find Add, ask what controls are visible and whether this is
an organization-managed account only if that changes the next step. Do not infer
plan limits from a missing tool, request an upgrade without evidence, or repeatedly
send the same unavailable menu. For a confirmed restriction, give a concise owner
request when wanted and continue the manual route. If the customer declines the
connection, preserve that choice. The current host paths are documented in
[Claude's connector guide](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).

Use [Connect Consent Pro](#connect-consent-pro) with the exact approved endpoint.
When no approved connector is available, continue through the official product dashboard.

### Codex and Claude Code: install the ready folder

Use this procedure only for requested or accepted persistent installation. An
assistant already running in the terminal can read the repository and begin the
website setup without it. An ordinary shell is not an AI assistant; if no client
is installed, use an available web chat or follow the chosen client's official
installation instructions before sending the setup request.

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

Sources for local skill locations:
[Codex skills](https://learn.chatgpt.com/docs/build-skills) and
[Claude Code skills](https://code.claude.com/docs/en/skills), checked 2026-10-16.

## Verify the package

Download the archive and `SHA256SUMS` from the reviewed release. Compare the archive
checksum, then extract it and inspect `package-manifest.json`. Confirm the expected
version, preview channel and source revision, and compare each bundled file's
SHA-256 with the manifest. A package name or successful extraction alone does not
establish that the expected instructions were installed.

Updating a package does not repair an existing GTM configuration. When resuming a
setup made with earlier helper scripts, read the Consent Pro tag's current trigger
and compare it with [Consent Initialization](../06-agent-readiness/operations.md#runtime-diagnosis).
Review any correction before applying or publishing it; a package update alone
does not authorize those changes or require a full audit.

Compute the hash of the ZIP you downloaded and compare it with the line for that
exact filename in `SHA256SUMS`. For the primary package, use
`shasum -a 256 consent-pro-0.3.12-preview.zip` on macOS,
`sha256sum consent-pro-0.3.12-preview.zip` on Linux, or
`Get-FileHash consent-pro-0.3.12-preview.zip -Algorithm SHA256` on Windows.
Substitute the specialist ZIP's filename if that is the package you chose.

If you downloaded both ZIPs listed in `SHA256SUMS` into the same directory, you
can check both with `shasum -a 256 -c SHA256SUMS` on macOS or
`sha256sum -c SHA256SUMS` on Linux. These full-list checks fail if a listed archive
is missing, including the optional specialist ZIP.

A checksum detects changed bytes; obtain the checksum and archive from the
reviewed release or trusted maintainer. These commands do not install into an
account or connect a service.

## Connect Consent Pro

The [official setup guide](https://docs.consentpro.com/mcp/setup), checked on
2026-10-29, identifies the production endpoint as `https://mcp.consentpro.com/mcp`.
Use **Consent Pro** as its display name and `consent-pro` in terminal commands.
It uses Streamable HTTP and Finsweet OAuth. The matching Web App is
`https://app.consentpro.com/`. No API key or manually copied bearer token is needed.

Reuse an existing working production connection. Keep any `consent-pro-staging`
entry separate, with its own approved endpoint and workspace. Adding production
does not migrate a project, replace the installed core or authorize site changes.
A staging connection can return documentation about production; match the selected
endpoint and account rather than inferring the environment from that documentation.

### Codex CLI or app

Inspect the existing entry first. If production is missing, run:

```bash
codex mcp add consent-pro --url https://mcp.consentpro.com/mcp
```

If adding it did not complete sign-in, run:

```bash
codex mcp login consent-pro
```

The customer completes browser sign-in. In Codex, use `/mcp` to check the connection.
For the app route, open Settings, MCP, Add, Add MCP Server. Name it Consent Pro,
select Streamable HTTP, enter the production URL, save and authenticate.
The CLI and app share configuration on the same Codex host; do not add a duplicate.
Use `codex mcp --help` if the installed client's controls differ.

### Claude web or Desktop

Open Settings, Connectors, Add custom connector. Some versions use Customize,
Connectors, Add, Custom, Web. Name it Consent Pro and enter the production URL.
Save, choose Sign in now and select **Claude Published Identity** if that choice
appears. The customer completes Finsweet authorization, then enables the connector
for the conversation. Account plans or organization settings can restrict custom
connectors; inspect the available controls rather than assuming access.

### Claude Code

In the intended project, inspect existing servers before adding production:

```bash
claude mcp add --transport http consent-pro https://mcp.consentpro.com/mcp
```

Start Claude Code, enter `/mcp`, select consent-pro and authenticate. The customer
completes browser sign-in. See [Claude Code MCP](https://code.claude.com/docs/en/mcp)
for client-specific configuration scope.

### ChatGPT

Follow the native **Add custom MCP server** flow in the
[intended plugin procedure](#chatgpt-keep-instructions-and-mcp-in-the-intended-plugin)
for the production URL and OAuth. The customer completes authorization; a skill
or saved archive does not authenticate the connection. Preserve staging separately,
then verify selection and a production read in the intended ChatGPT host.

### Choose access and authorize

Explain the access choice before the customer approves it:

| Choice | What it enables |
|---|---|
| Full access | The release's available permissions for end-to-end setup, including drafts, scans, publishing and GTM. Each change still needs the customer's instruction or approval |
| Read only | Consent Pro inspection without changes. It excludes GTM and consent export/proof requests |
| Custom | The specific permissions the customer chooses. Include View Google Tag Manager for the separate Google connection and read tools |

For requested end-to-end connected setup, recommend Full access and explain its
scope. Do not recommend Read only solely because diagnosis is the first step of
that setup. Honor an explicit read-only or narrower choice. Explain that granted
permissions make operations available; the customer's instructions authorize their
use, with publication separately approved. The customer signs in with the account
used in the production Web App, selects the intended workspace and approves access.
Never request passwords, authorization codes, callback URLs or tokens in chat.

Full access does not bypass Google roles or grant permissions introduced after an
older authorization. New tools under an existing granted permission can appear
without reconnecting. A new permission needs a new grant. Missing Google scopes
need a separate user-opened Google authorization; the selected container's role
still decides which operations succeed. See the
[GTM capability path](../06-agent-readiness/operations.md#future-gtm-writes).

When the customer's permitted route includes the dashboard, keep the selected
project open to compare saved state. For API/MCP-only work, use authoritative
reads and retain any unavailable UI or browser evidence as unverified.
The [operations guide](../06-agent-readiness/operations.md) distinguishes drafts,
scans, email requests and separate publication authority. Discover the operations
actually available to this connection before choosing a supported path.

After sign-in, list the projects, resolve the intended workspace/project/hostname and
read that project's setup. If none match, verify workspace and pagination before offering
project creation. Do not create a duplicate to work around an access problem. For GTM,
continue with [Connect Google Tag Manager](../06-agent-readiness/operations.md#connect-google-tag-manager),
which is separate from Finsweet OAuth. Confirm the returned containers after Google login.

### Verify the connected environment and tool set

Use `consentpro_projects_list` for a harmless account/workspace check. Inspect the
current tools and schemas exposed by the selected production connection, following
discovery pagination. Count only that endpoint's tools, including its documentation
tools. Do not sum staging, production and duplicated host integrations.

The 2026-10-29 production testing release expects **48 tools with Full access**:
46 Consent Pro tools and two documentation tools. This is a dated release check,
not a permanent capability contract. Read only and Custom can expose fewer tools.
If the host cannot enumerate the complete catalogue, report the count as unverified
instead of repeating the expected number as a measurement.

If that production release still shows fewer tools after a client discovery refresh
with Full access, follow its reconnect procedure. Retain the intended account and
workspace, remove only that production connector, add the same production URL and
authorize it again. Keep staging and other connections intact. Then recount and
run the account read. If the result still differs, inspect missing operations and
permissions; do not repeat reconnection blindly or substitute another environment.

A matching count does not prove every permission works or that edits and publishing
were tested. Read each operation's contract when needed. A later release can change
the count; prefer current server evidence and official documentation over a frozen
number. Report connection, tool discovery, effective reads and untested writes separately.

## Recover a missing layer

| Symptom | Next action and success check |
|---|---|
| Tools work but instructions are absent | Read the repository or supplied guides and continue in this conversation, preserving the working connector. Install or update persistent instructions only when requested or accepted; use a new conversation only if the host needs it to load that change |
| Instructions load but tools are absent | Enable/authenticate the intended connector if the customer wants it; otherwise continue with dashboard guidance and label reported versus inspected evidence |
| Consent Pro works but GTM is disconnected | Use GTM status and its private user-opened connection flow, then re-read status and containers |
| Expected project/container is missing | Check workspace, Google account and completed pagination; have the appropriate administrator resolve missing access |
| Changes fail with read-only access | Present the exact pending change and reconnect with the necessary scope or guide the approved manual path; do not switch credentials silently |
| A release announces tools that are absent here | Refresh discovery, check the selected environment and available permission evidence. Absence alone does not distinguish an undeployed operation, an older client catalogue or an insufficient grant |
| Package may be outdated | Compare actual installed content with a known source package; do not infer freshness from the plugin name or a test count |
| No browser or site access | Complete supported reads, prepare the exact code/manual handoff and mark deployment and behavior unverified |

Use the [onboarding checkpoint](../reference/onboarding.md#start-and-resume) to resume after the
missing layer is restored. Do not restart every connection or repeat a scan by default.

### When reauthorization helps

First refresh the client's tool discovery, or start a new conversation if that is
the host's supported refresh path. Keep the working connector and selected
workspace. Compare the missing operation with current server documentation,
advertised permissions and the account's effective grant when those are available.
An advertised permission means the server offers it, not that this connection has
it or that the corresponding operation has passed a live test.

- New tool, existing permission: refresh discovery; do not reinstall the skill or
  revoke the connection just because the tool is new.
- New Consent Pro permission: explain the exact access needed and use the supported
  reauthorization flow for the existing connection. Remove and re-add it only when
  the service requires that, after identifying the environment and workspace to restore.
- Missing Google scope: use a new user-opened Google connection link for the intended
  account. A new Consent Pro grant does not refresh Google scopes or container roles.
- Expanded testing access: check tracker import/review, suggestions, translation
  edits, setup acknowledgements, Consent Pro publication, GTM edits, entity management,
  publication and rollback separately when the server advertises them. A translation
  read tool is not an editing permission. Do not claim the entire testing workflow
  is available merely because some new tools appeared.
- Missing deployment or unresolved cause: preserve working access, report what is
  unverified and continue supported work. Reauthorization cannot deploy a tool.

After authorization, rediscover tools and perform a relevant read before continuing
the previously approved task. A successful login, tool listing or Full access label
does not prove editing or publishing. Do not test a write merely to discover whether
it is permitted. Removing a client connector does not remove a separately saved
Google connection or undo earlier changes.

## First read-only conversation

Replace the hostname and workspace with the customer's target:

> Use my connected Consent Pro account. My website is example.com in the selected workspace.
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
