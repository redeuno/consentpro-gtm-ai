# The nine steps, in order

Both documentation trails carry the same nine. Step 2 now uses the Gallery; the remaining
configuration and browser checks still apply to both trails.

Choose [Basic or Advanced Consent Mode](consent-mode.md) first. The local script is a Basic
configuration path; the current Consent Pro MCP reads GTM but does not write or publish it.
Account for the [three separate releases](../06-agent-readiness/operations.md#draft-preview-and-release).

---

## 1. Remove the tag manager `<noscript>`

**Why:** it loads tags without JavaScript, which means outside the consent layer entirely.

- **Webflow:** Site Settings, Custom Code, remove it from the Footer.
- **A framework project** (Astro, Next, Nuxt, SvelteKit, Remix): it is in the shared layout or
  root document that renders `<body>`, not in a page. In Astro that is usually
  `src/layouts/*.astro` or `src/pages/_document`-style wrappers; in Next, `app/layout.tsx` or
  `pages/_document`. **Search your repository for `googletagmanager.com/ns.html`**, which is the
  string only the `<noscript>` half contains, and you will land on it directly.
- **A plain site:** wherever your template or include puts it.

---

## 2. Add the Consent Pro template from the Gallery

Open your GTM workspace and follow **Templates > Search Gallery > Consent Pro by Finsweet >
Add to workspace**. Review the requested permissions, then choose **Add** if you approve.
Check the publisher and linked repository against the
[Consent Pro Gallery listing](https://tagmanager.google.com/gallery/#/owners/finsweet/templates/gtm-template-consent-pro)
and [Finsweet's repository](https://github.com/finsweet/gtm-template-consent-pro).

This manual path does not need a `.tpl` download, Google Cloud setup or a custom OAuth
client. It needs a Google login with access to the target container.
[Google documents the Gallery flow](https://support.google.com/tagmanager/answer/9454109?hl=en).

**What it gives you:** a tag type that the next step uses. Nothing fires yet.

**For API automation:** the script uses
[`templates.import_from_gallery`](https://developers.google.com/tag-platform/tag-manager/api/reference/rest/v2/accounts.containers.workspaces.templates/import_from_gallery)
for a new template, with owner `finsweet`, repository `gtm-template-consent-pro` and version
`8a551897e5bfdecf03de59fa00058be442b7ac29`. This path still needs the
[OAuth setup](../01-google-cloud-setup.md) and [authorisation](../03-authorise.md).
Simulation shows the import and its `PLAN_SHA256`. Review permissions and the full plan;
`--apply --approve-plan HASH` executes only a matching plan. Publication needs a separately
reviewed plan including `--publish`. See [execution commands](../04-run-it.md).

**Already installed:** audit first. The script preserves recognised existing templates and
their IDs. A compatible manual import stays manual; it does not gain Gallery provenance or
update notifications from being recognised. Unexpected Gallery owner, repository or version,
modified templates, and unrecognised content stop configuration before writes. Review the
reported reason instead of deleting a working template to force the script through.

**Future updates:** GTM can notify you of publisher updates to a Gallery template. Open the
notification, compare the changes, accept the update when appropriate, test the workspace and
publish it. Saving an update does not publish it. Editing the template can disconnect it from
publisher updates. See [Google's update instructions](https://support.google.com/tagmanager/answer/9454109?hl=en).
The scripts do not automatically update or migrate templates; a new Gallery version also
needs review against this repository's pinned version.

**Source status, 2026-10-01:** the official
[Webflow](https://docs.consentpro.com/webflow/google-tag-manager) and
[web app](https://docs.consentpro.com/web-app/google-tag-manager) pages still showed the older
download flow when checked. For installation in this step, use the Gallery and publisher
sources above. Gallery approval does not by itself establish Google CMP certification or
prove that a site's consent behaviour works.

---

## 3. Create the initialization tag

**Tags**, **New**, **Tag Configuration**, pick the Consent Pro template installed in step 2
from the Custom section. Then **Triggering**, and select **Consent Initialization - All Pages**.

⛔ **Not `All Pages`.** They are two different built-in triggers and the names are one word
apart. Consent Initialization runs before everything else in the container, which is the entire
reason this tag exists. On plain All Pages, other tags can beat it to the page and fire before
consent is known.

Name it something recognisable, such as `Consent Pro Init`, and save.

---

## 4. Set the regional defaults

Still inside that tag: **Region-Specific Consent Settings**, then **Add Region Setting**.

**The pattern depends on your banner type:**

| Banner type | Every field |
|---|---|
| Opt-in (GDPR style, explicit acceptance) | **Denied** |
| Opt-out, Do Not Sell, or Informational | **Granted** |

The reasoning: with opt-in, tracking must not happen before consent, so the defaults deny and
the visitor's acceptance grants. With opt-out, tracking is allowed until the visitor declines.

**The region codes are in [`regions.md`](regions.md), and that page matters more than it
looks.**

Three optional settings on the same tag:

| Setting | What it does | Reasonable value |
|---|---|---|
| Wait for consent update | how long tags are held while consent resolves | 500 to 2000 ms, default 1000 |
| URL passthrough | carries ad click identifiers through the URL while consent is pending | on, if the site runs paid ads |
| Ads data redaction | strips ad identifiers from requests when consent is denied | on, for stricter setups |

**More than one banner means more than one region row**, each with its own codes and its own
granted or denied pattern. Not more than one tag.

Read the existing rows before changing them. Preserve rows outside the requested change,
plan eligibility and unrelated options. The local writer preserves an existing table when
`--regions` and `--banner` are omitted; it refuses explicit changes to a multi-row table.

---

## 5. Create the Consent Updated trigger

**Triggers**, **New**, **Trigger Configuration**, **Custom Event**.

- **Event name:** `consent-updated`
- Select **All Custom Events**
- Name it `Consent Updated` and save

**What fires this event:** the runtime when consent is applied or changed, including a
rejection. The event itself grants no permission; the category checks still matter.
Source: [runtime events](https://docs.consentpro.com/runtime/events).

If a trigger already has this name, check its type and exact event rather than trusting the
label. A `Consent Updated` trigger pointing to `purchase` must not be reused as consent.

---

## 6. Preserve business events and gate the tags

For a Basic-mode page-load tracker, replace its page-load trigger with **Consent Updated**
and add the category checks in step 7. If the original trigger has page conditions,
preserve those conditions in the reviewed consent trigger; do not replace a filtered
pageview with an unrestricted event. The local writer automates only built-in All
Pages and refuses custom page lifecycle triggers for manual review.
For a purchase, form submission, click or other
business-event tag, preserve its original event and conditions, then add the appropriate
consent checks. A consent choice is not a purchase. Review tags with multiple firing or
blocking triggers separately before changing their semantics.

**Basic GA4** follows the consent-updated plus additional `analytics_storage` pattern.
**Advanced GA4** uses Consent Initialization, no additional `analytics_storage` requirement,
and Consent Pro Init before the Google tag. See [the mode contract](consent-mode.md).

For a reviewed Essential tag, retain its original trigger rather than making it depend on a
consent choice. The public guide's broad instruction to replace marketing/non-Google
triggers does not preserve conversion-event semantics. This repository deliberately narrows
that step to protect business conditions; test both consent and the original event.

---

## 7. Add the consent checks

Per tag: **Tag Configuration**, **Advanced Settings**, **Consent Settings**, select **Require
additional consent for tag to fire**, and pick the consents.

Which ones to pick is in [`categories.md`](categories.md).

⚠️ **Scan first.** The categories come from the scan, so mapping against an old scan describes
trackers the site no longer has, or misses ones it gained.

⚠️ **If a script uses `document.write`**, enable "Support document.write" in the tag settings,
or it may not execute and may not be detected.

---

## 8. Submit and publish

**Submit**, then **Publish**.

Container edits reach ordinary visitors only after the intended GTM version is published.
Until then, the previous live version remains in use. Changes to the site's markup have
their own deployment and must be tracked separately.

Saving, creating a version and publishing are distinct operations. Authorisation to configure
does not include publication. Consent Pro settings and site code require their own releases.

---

## 9. Mark it done in the app

- **Webflow:** the **Actions** tab, check the Google Tag Manager message.
- **Web app:** **Overview**, **Data Privacy Check**, the **Configure GTM** row, **Mark as
  done**.

⛔ **This records that someone said it was done. It verifies nothing.** Do it after the
container is published, and do the real checks in [`verify.md`](verify.md).
