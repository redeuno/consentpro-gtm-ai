# 2. Select or create the tag manager account

Use this guide when the customer chooses GTM or needs to identify an existing
container. Consent Pro does not make GTM mandatory. A site without GTM can follow
the [direct script and pixel path](05-what-gtm-does-not-cover.md).

The manual path needs a Google login with the required container access and a
person who can edit the site. It does not require connecting Google to the agent,
Google Cloud setup, an OAuth client, an API key or a terminal. The customer may
operate both Consent Pro and GTM through their dashboards.

## Identify what already exists

Use the requested site, available site evidence and the selected GTM dashboard to
confirm the Google account, GTM account, container and workspace. The public
`GTM-XXXXXXX` ID identifies a container, not its owner or who may edit it. A
Consent Pro workspace is separate from a GTM workspace.

- Existing account and correct container: reuse them; inspect the live version,
  pending workspace changes and whether the snippet is actually on the site.
- Existing account but no container for this site: confirm that absence and the
  owner's intent before creating a web container in that account.
- Expected account/container missing: check the signed-in Google identity and
  permissions with its administrator. Do not create a replacement to bypass access.
- Read access only: the customer can inspect and help plan, but an editor must
  perform changes. Publication may belong to a different person.
- Neither party has access: prepare the exact administrator request and continue
  independent Consent Pro/site work. A blocker is not a finished setup.

For an agency, select one client's target and authority before every switch. Do
not use the first accessible container or carry another client's approval forward.

## Creating an account or container

The customer completes account creation in the GTM interface. The local scripts
configure containers; they do not create GTM accounts. For a new account:

1. Open [Google Tag Manager](https://tagmanager.google.com) with the Google account
   intended to manage this site. Confirm the account before creating anything.
2. Choose **Create Account**. Set the account name to the company or client's
   company and select its country. Country here does not select consent behavior.
3. Set the container name to an identifiable site name, such as `example.com`,
   and choose **Web** as the target platform.
4. Review the terms and create the account/container. Account creation and its
   first container are part of the same form. Confirm the resulting names and
   `GTM-` ID before continuing.

For an existing account, use its container creation control instead. If a screen
or control differs, inspect the account, permissions, language and current UI;
do not ask the customer to repeat a missing click. A supported API route is an
optional alternative, not a requirement for this procedure.

Source: [Google's account and container setup](https://support.google.com/tagmanager/answer/6103696).

## Identify the target for the selected path

| Path | Useful target evidence |
|---|---|
| Customer operates the interface | Account and container names, public `GTM-` ID and selected workspace; ask for a relevant screen only if needed |
| Connected MCP | Current Google status and fully paginated containers, then explicit target selection; inspect what published/workspace evidence the tool actually returns |
| Optional local API scripts | Numeric Account ID from Admin, Account Settings or the `/accounts/` URL, plus the public `GTM-` ID and selected workspace expected by the script |

Do not require numeric IDs merely to guide a customer through the interface. The
numeric Account ID, container's internal numeric ID and public `GTM-` ID are
different values. Never ask the customer to paste a token or OAuth callback URL.

## Connect the container to the site

The installation prompt shown after creation is not evidence that the site has
the snippet. Inspect the served site and the site's shared integration settings
before adding it. A CMS integration, shared layout or another administrator may
already install the same container.

Choose the order from the existing state:

| State | Safe next action |
|---|---|
| Correct snippet already installed | Keep it, inspect the live version and continue with the missing consent setup |
| New container with no published tracking | Prepare the exact GTM snippet and Consent Pro core on the authorized test site, then configure and preview the container before exposing visitors to tracking |
| Container already has published tags, snippet absent from this site | Inspect those live tags before deployment. Coordinate the consent configuration, GTM release and site release on the test target; installing the snippet can immediately activate the published tags |
| Another container or CMP already controls the site | Use the [transition procedure](06-agent-readiness/operations.md#existing-cmp-and-tracking-transition); do not add a second installation as a shortcut |

In the GTM interface, open the selected container's installation instructions and
use its exact web snippet. Place the executable script in the shared site head,
after the exact Consent Pro core as described in
[core installation](06-agent-readiness/operations.md#core-installation-and-licence).
Use the platform's authorized site settings or shared layout, not a page-specific
copy. Preserve existing CSP and other integrations. This consent setup omits the
GTM `noscript` iframe, whose separate loading path is explained in
[step 1](reference/nine-steps.md#1-remove-the-tag-manager-noscript).

Have the site owner preview or deploy the agreed change. Inspect the served page
for the intended container ID, one intended installation and core order. Then
use GTM Preview/Tag Assistant and the [browser checks](reference/verify-behaviour.md).
HTML presence does not establish that consent works. Record site deployment,
GTM workspace configuration and GTM publication separately.

For every customer-only action, provide its destination, exact object and intended
value, expected result and evidence needed to resume. Treat "done" as reported
until a relevant read or view confirms it. If no one can edit the site, hand the
snippet and approved placement to the site administrator and keep deployment open.

## Continue through the available route

- Manual setup, including declined Google connection: follow the
  [nine steps](reference/nine-steps.md). The template, tags, preview and publication
  remain possible through the interface without a connection to the assistant.
- Connected diagnosis: use the [Google connection flow](06-agent-readiness/operations.md#connect-google-tag-manager)
  only if the customer chooses it, then confirm the intended target and grants.
- Explicitly selected local automation: follow [Google Cloud setup](01-google-cloud-setup.md),
  [authorization](03-authorise.md) and the [run guide](04-run-it.md).

If interrupted, carry the [resume card](reference/onboarding.md#start-and-resume)
forward and re-read affected state when the customer returns. Do not repeat account
creation, install a second snippet or reconnect a working account just to restart.
