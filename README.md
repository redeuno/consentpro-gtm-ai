# Set up Consent Pro with your AI

Send this repository link to your assistant and say: "I want to install Consent
Pro on my website." The assistant should start helping in that conversation.
You do not need a perfect prompt, an installed skill, a connector or a terminal
before you can begin.

The first outcome is a working banner on the website you choose, with publication
and the checks performed clearly confirmed. Start with the necessary configuration;
personalize and explore additional features afterward. A temporary Preview is a
separate result from a banner served to ordinary visitors.

Custom-site setup currently covers the whole selected hostname, including its
home page (`/`). Put the project script in the site's shared `<head>`, not only
on a landing-page path. For `shop.example.com`, this means that subdomain's own
home page and pages, not automatically `example.com`.

There are [three activation checkpoints](docs/06-agent-readiness/operations.md#current-first-installation-handoffs):
site installation, banner creation and publication in the selected environment.
The MCP supplies the script; separate authorized site tools or the customer install
it first in the shared head, without `async` or `defer`. Banner setup and publishing
can use reviewed MCP operations when exposed and authorized. Otherwise, the assistant
guides that specific dashboard step. Discover each operation separately: an older
connection can expose banner creation while still lacking publication permission.

If the assistant cannot retrieve this GitHub page, share the
[plain-text entry](https://raw.githubusercontent.com/redeuno/consentpro-gtm-ai/main/README.md)
in the same conversation. This is another reading route, not a different setup.
If that also fails, share the relevant guides as text, or attach the reviewed
primary ZIP linked below if the chat can read archives. Using the guides as a
reference does not require installing a persistent skill.

## For the assistant: begin the requested setup

Read the [Consent Pro instructions](skills/consent-pro/SKILL.md) and the
[first-reply procedure](docs/07-agent-installation/README.md#start-in-your-current-chat),
then act on the customer's request. Reading these files provides guidance for this
conversation; it does not install a persistent skill or connect an account.

- Use the customer's language and the facts already given. Do not summarize this
  repository, send another starter prompt, or ask the customer to restart before helping.
- Read only the entry instructions and inspect the available connection before
  asking for a missing site URL. Load operation-specific guidance when that action
  becomes relevant. Check a loaded package's version once; an older installed
  copy must not silently override the current guidance you have verified.
- Check the tools actually available. For full setup, recommend the supported
  Consent Pro connection once and reuse it when working. Confirm the product
  environment before giving an endpoint. Explain the guided dashboard alternative;
  missing tools are not a customer's decision to work manually. If connection is
  unavailable, declined or deferred, continue the installation through that path.
- Offer the ready skill once for reuse in future chats, explaining that the
  instructions already read can guide this conversation. Make this a brief offer
  at a useful pause, not an upload task before the first banner. An explicit
  request to install it still takes precedence.
- Use connected project reads to resolve the target. Otherwise ask for the site
  URL when needed; inspect available evidence before asking for platform or GTM
  details. A narrow public-site inspection does not require account setup.
- When the customer explicitly asks to install the skill or connect MCP, complete
  that setup step first; a website URL is not needed to prepare the assistant.
- Do the authorized work your tools support. For a customer-only action, give one
  short sequence of clicks and the expected result, then verify and continue.
- If Claude cannot add a connector in that account, keep the guided dashboard
  route available. Do not turn missing connector tools into a demand to install a
  skill or into proof that the account cannot use connectors.

See the [guided onboarding](docs/reference/onboarding.md) for resumption and the
[client journey](docs/00-the-journey.md) for the full procedure. The customer sees
the next useful action, not the whole procedure at once.

## Save the instructions for future conversations

The [ready preview packages](https://github.com/redeuno/consentpro-gtm-ai/releases/tag/v0.3.5)
contain the instructions and references for optional persistent installation.
The [installation guide](docs/07-agent-installation/README.md)
distinguishes ChatGPT, Claude chat, Codex and Claude Code. Both skills share the
same product references and scripts. Installing instructions, connecting Consent
Pro, authorizing Google and installing code on the website are separate actions.

## Choose the path available to the customer

| Path | Available work | Requirements |
| --- | --- | --- |
| Connected Consent Pro MCP | Inspect the selected project and use the operations actually available to this connection | Verified environment, Finsweet OAuth, correct workspace and operation-specific access |
| Local Google API scripts | Audit and configure a selected web GTM workspace, create a version and optionally publish | Python 3.10+, reviewed Google OAuth scopes, confirmed account/container/workspace and approved simulation |
| Product and GTM interfaces | Complete guided configuration and verification, including when the assistant has no connector | Customer dashboard access and decisions; no Google Cloud/API setup required |
| Site repository and browser | Install the exact project snippet, handle image pixels, preferences and verify behavior | Access to the customer's site and test environment |

Discover capabilities in each session; access is not permission to make unsolicited
changes. A successful connection does not install the instructions, prove Google
access or authorize publication. If a tool is missing, continue through the dashboard
where the customer has access. Use only reviewed and tested operations.
The [GTM capability path](docs/06-agent-readiness/operations.md#future-gtm-writes)
prepares for editing releases: use reviewed draft operations when available, retain
manual steps for missing operations and verify publication authority separately.

The [connection guide](docs/07-agent-installation/README.md#connect-consent-pro)
uses the exact MCP URL approved for the customer's product environment, supplied
by Consent Pro or the customer. Do not invent a production endpoint. If no approved
connection is available, continue through the official product dashboard.

## Reach the first publication

1. Identify the site and intended environment; reuse the project, connections and
   valid installation already present. Ask only for what the next action needs.
2. Resolve the account, domain, applicable license and exact project snippet.
   Prepare the initial banner, privacy link and preferences without a design detour.
3. Inspect the installation path for conflicts and tracking that would invalidate
   the intended consent behavior. Handle relevant GTM settings when needed;
   adopting GTM, connecting Google and a full inventory are not universal gates.
4. Apply the approved setup and run the relevant choice and site-function checks.
   Use an existing valid scan; request a new one when evidence or the product
   requires it, not merely because a checklist includes scanning.
5. Review and authorize the required site, Consent Pro and optional GTM releases.
   Confirm the ordinary address outside Preview and report exactly what was tested.
6. Continue with the customer's chosen personalization and broader review.

The [journey](docs/00-the-journey.md) defines the first-activation boundary and
later work. A known consent failure or broken site function needs treatment;
an untested tracker remains unverified. Production can be the first chosen target
when its requirements and publication authority are satisfied. A test hostname
does not imply a free license, and publication does not prove payment.

For public HTML inspection, without credentials:

```bash
python3 scripts/inspect-site.py https://example.com
```

This reports declared runtime, required attributes, site ID, script order and image
tracker candidates. It cannot prove what ran in the browser. Finish with the
[behavior checks](docs/reference/verify-behaviour.md), including rejection,
acceptance as a positive control, partial choice, revocation and reload.

For local GTM automation, follow [Google Cloud setup](docs/01-google-cloud-setup.md),
[GTM account setup](docs/02-tag-manager-account.md), [authorization](docs/03-authorise.md)
and the [run guide](docs/04-run-it.md). This broader credential path is optional;
an MCP read-only restriction does not authorize switching to it.

The GTM [Community Template Gallery](https://tagmanager.google.com/gallery/#/owners/finsweet/templates/gtm-template-consent-pro)
provides the manual template installation. API imports pin the reviewed publisher
version and preserve recognized existing templates. Gallery availability does not
establish Google CMP certification.

## What is covered

- [Operations](docs/06-agent-readiness/operations.md): capability discovery,
  project targeting, installation, scan limits, previews, licenses, logs and recovery.
- [Guided onboarding](docs/reference/onboarding.md): progress checkpoints, manual handoffs,
  evidence-based fixes and resuming without repeating completed setup.
- [Beyond GTM](docs/05-what-gtm-does-not-cover.md): hardcoded scripts, image pixels,
  preferences and reconciliation with the scan.
- [GTM references](docs/reference/nine-steps.md): regions, categories, checks and troubleshooting.
- [Local script guide](docs/04-run-it.md): audits, simulation, approved writes and recovery.
- [Installation and recovery](docs/07-agent-installation/README.md): host-specific
  instructions, package verification, connection checks and updates.

Detection is not blocking. A successful scan, setup checkbox, preview or unchanged
cookie count does not establish that tags respected a visitor's choice. Report
only the trackers and actions actually tested, without compliance guarantees.

## Security, support and license

Read [SECURITY.md](SECURITY.md) before authorizing scripts. A Google write scope can
reach every container the account can access. The writer simulates by default,
ties application to an approved current-state plan, preserves business events and
regional tables, and keeps publication separate. Failures require inspection
before retrying; a partial application is not a finished version.

For access and product assistance, follow the
[support guide](docs/reference/troubleshooting.md#support-and-assisted-setup).
Keep credentials, signed links and customer records out of public issues. These
local scripts do not send telemetry.

This distribution uses the [MIT license](LICENSE). Product guidance cites the
official sources beside each procedure. The Finsweet GTM template is a separate
upstream component; its publisher, pinned version and license are linked in
[Security](SECURITY.md).
