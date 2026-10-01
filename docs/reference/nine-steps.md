# The nine steps, in order

Both documentation trails carry the same nine. Step 2 now uses the Gallery; the remaining
configuration and browser checks still apply to both trails.

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
Simulation shows the planned import; `--apply` acknowledges its permissions and performs it.
Publishing remains separate.

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

---

## 5. Create the Consent Updated trigger

**Triggers**, **New**, **Trigger Configuration**, **Custom Event**.

- **Event name:** `consent-updated`
- Select **All Custom Events**
- Name it `Consent Updated` and save

**What fires this event:** the Consent Pro runtime on the site, when a visitor makes a choice.
Measured in a served runtime in September 2026: it pushes `consent-updated`, and also the
version one events `essential-activated`, `marketing-activated`, `analytics-activated` and
`personalization-activated`.

---

## 6. Move the tags onto it

**Apply to marketing and non-Google tags.** For each: open it, remove the current trigger, add
**Consent Updated**.

**If you use Advanced Consent Mode**, configure GA4 on Consent Initialization instead, and see
the Basic versus Advanced page. Advanced mode lets GA4 send cookieless pings when analytics
storage is denied, which is a deliberate choice rather than a default.

⚠️ **An ambiguity in the guide, worth naming so nobody is surprised.** The instruction says
"marketing and non-Google tags". A custom HTML tag that sets an essential cookie is non-Google
and also essential, so it matches both the rule and the exception, and the guide does not say
which wins. **Decide it with the person and record which way you went.** Moving an essential
tag onto the consent event means it stops firing on page load and starts depending on a visitor
choice, which may be exactly wrong for a tracker the site needs to function.

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

Nothing in steps one through seven reaches the site until this happens. A container with every
setting correct in an unpublished workspace behaves exactly like a container with none of them,
and the interface gives no hint of the difference.

---

## 9. Mark it done in the app

- **Webflow:** the **Actions** tab, check the Google Tag Manager message.
- **Web app:** **Overview**, **Data Privacy Check**, the **Configure GTM** row, **Mark as
  done**.

⛔ **This records that someone said it was done. It verifies nothing.** Do it after the
container is published, and do the real checks in [`verify.md`](verify.md).
