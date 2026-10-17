# Set up Consent Pro with your AI

Send this repository link to your assistant and say: "I want to install Consent
Pro on my website." The assistant should start helping in that conversation.
You do not need a perfect prompt, an installed skill, a connector or a terminal
before you can begin.

If the assistant cannot retrieve this GitHub page, share the
[plain-text entry](https://raw.githubusercontent.com/redeuno/consentpro-gtm-ai/main/README.md)
in the same conversation. This is another reading route, not a different setup.

## For the assistant: begin the requested setup

Read the [Consent Pro instructions](skills/consent-pro/SKILL.md) and the
[first-reply procedure](docs/07-agent-installation/README.md#start-in-your-current-chat),
then act on the customer's request. Reading these files provides guidance for this
conversation; it does not install a persistent skill or connect an account.

- Use the customer's language and the facts already given. Do not summarize this
  repository, send another starter prompt, or ask the customer to restart before helping.
- Check the tools actually available. Use connected project reads to resolve the
  target when possible. Otherwise, if the site is unknown, ask for its URL as the
  next step. If it is known, inspect available evidence before asking for the
  platform, account or GTM details that evidence can establish.
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

The [ready preview packages](https://github.com/redeuno/consentpro-gtm-ai/releases/tag/v0.2.1)
contain the instructions and references for optional persistent installation.
If the repository is private, downloads need access; a maintainer can supply the
same reviewed ZIP directly. The [installation guide](docs/07-agent-installation/README.md)
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

The [environment guide](docs/07-agent-installation/README.md#choose-the-environment)
separates customer service, product development staging and a customer's test site.
This preview does not establish a production MCP endpoint. Invited testers can use
the explicitly labeled staging instructions; other customers can begin manually.

## Start safely

1. Resolve the [account and instructions](docs/07-agent-installation/README.md), or open
   the [manual GTM procedure](docs/reference/nine-steps.md).
2. Identify the workspace, project, public hostname, installed engine and goal.
3. Read the current state. Decide whether GTM is needed; choose Basic or Advanced
   Google Consent Mode explicitly when applicable.
4. Review exact changes, including tag business events and every regional default.
5. Apply authorized changes, read them back and test behavior.
6. Report saved drafts, GTM versions, publications and site deployment separately.

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
- [Script catalogue](scripts/README.md): reads, writes, apply flags and recovery.
- [Tests](tests/README.md): offline checks, mutation controls and verification limits.
- [Evidence and implementation status](docs/06-agent-readiness/README.md): the complete
  delivery record, public-source references and remaining acceptance gates.
- [Next delivery plan](docs/06-agent-readiness/README.md#5-delivery-phases-and-remaining-gates):
  customer entry, complete manual GTM setup, support handoffs, versioned packages and
  per-client acceptance. Implemented guides and verified client behavior are separate.

Detection is not blocking. A successful scan, setup checkbox, preview or unchanged
cookie count does not establish that tags respected a visitor's choice. Report
only the trackers and actions actually tested, without compliance guarantees.

## Security and contribution

Read [SECURITY.md](SECURITY.md) before authorizing scripts. A Google write scope can
reach every container the account can access. The writer simulates by default,
ties application to an approved current-state plan, preserves business events and
regional tables, and keeps publication separate. Failures require inspection
before retrying; a partial application is not a finished version.

Repository documentation, skill instructions, scripts and tests are authored in
English. Raw source evidence is kept outside this repository. Update canonical
files and regenerate installed packages, rather than editing generated copies.
Run the documented checks before a pull request. Keep credentials and customer
records out of commits. This repository does not send telemetry.
