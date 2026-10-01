# 0. The whole journey, and where an agent fits today

Read this first. It saves you discovering halfway through that the automated part is one
stage out of several.

**This map is not a guess.** It was built by walking the product end to end, from a site that
did not exist to a recorded consent, capturing every screen in order. The stage names below
are the product's own labels.

---

## The nine stages

| # | Stage | Where it happens | Can an agent do it today? |
|---|---|---|---|
| 0 | **Tag manager account; Google Cloud for automation only** | Google consoles | The GTM interface needs container access. Scripts also need an OAuth credential. [Docs 1](01-google-cloud-setup.md) and [2](02-tag-manager-account.md) |
| 1 | **Sign in, pick a workspace** | the app | no. SSO, in the browser |
| 2 | **Connect Domain** | the app, setup step 1 | no |
| 3 | **Configure Banner** | the app, setup step 2 | no |
| 4 | **Install** the core script | the app gives it, your site takes it | **the app half, no. Putting the snippet in your site, yes**, if the agent has your codebase |
| 5 | **Scan** the site | the app | no. One button, and it drives stages 6 and 8 |
| 6 | **Categorise the trackers** | the app, with `Fill with AI` | no |
| 7 | **Wire Google Tag Manager** | the GTM interface or API | yes, the container configuration; site checks remain separate |
| 8 | **Publish** | the app | no. **Publishing a production domain requires a paid plan** |
| 9 | **Image trackers and the `<noscript>`** | your site's code | **yes**, if the agent has your codebase. [Doc 5](05-what-gtm-does-not-cover.md) |

---

## Why stage 7 is the automated one, and the others are not

**Not because it is the most important.** Because it is the only stage that happens in a
system with a public API.

Stages 1 through 8 happen inside the Consent Pro app, which today has no public API and no
MCP server. An agent cannot press a button on a screen it cannot reach. Stage 7 happens in
Google Tag Manager, which has a full API, and that is the entire reason this repository
exists.

⭐ **It also happens to be the stage users find hardest.** Finsweet's own figure: 63% of
Consent Pro users use Google Tag Manager, and it is the most painful step of the setup.

---

## What each stage actually involves

### Stage 0. Google Cloud and the tag manager account

**Manual setup:** sign in to GTM and use an existing container or create one with
[doc 2](02-tag-manager-account.md). Add Consent Pro from the Gallery in
[step 2](reference/nine-steps.md#2-add-the-consent-pro-template-from-the-gallery).
This path needs no custom OAuth client and no template download.

**API automation:** also complete [Google Cloud setup](01-google-cloud-setup.md) and
[authorisation](03-authorise.md). The OAuth client JSON and refresh token let the scripts act
on your behalf; installing a Gallery template does not authorise those scripts.

**Two things here cannot be automated by anyone.** Creating a tag manager account, because
the interface demands a container name on the same screen and no API path skips it. And
approving a credential, because it ends at a Google consent screen a person clicks.

### Stages 1 to 3. Sign in, connect the domain, configure the banner

The setup wizard has three steps, in this order: **Connect Domain**, **Configure Banner**,
**Install**.

Connect Domain asks for the domain and a project name. Configure Banner covers the banner's
position, the preferences screen, and two colour palettes, with a live preview of both. The
defaults arrive light: white background, black text, blue links. The four categories appear
in the preferences screen, with `Essentials` fixed as always active.

**Decide your banner type here**, because it decides everything in stage 7: an opt-in banner
means every regional default is denied, and opt-out, do-not-sell or informational mean granted.

### Stage 4. Install

The app hands you a snippet with `Copy code` and `Verify installation`.

⛔ **`Finish setup` stays disabled until verification passes.** `Do it later` exists and opens
the project unverified.

**The snippet goes at the very top of `<head>`, before everything else.** An agent with access
to your codebase can do this part. In a framework project (Astro, Next, Nuxt, SvelteKit) it
belongs in the shared layout that renders `<head>`, not in a page.

### Stage 5. Scan

One button, and everything downstream depends on it. The scan reads your published site and
finds the cookies your trackers set.

⚠️ **Two things the scan does not see**, and both bite later: a tracker inside your tag
manager whose tag does not fire on `All Pages` or on `consent-updated`, and anything that only
appears after an interaction. [Doc 5](05-what-gtm-does-not-cover.md) covers this.

**Publish a `sitemap.xml` before scanning.** Without one the scan reads a single page. With
one, auto-detect finds it and reads the whole site.

### Stage 6. Categorise

Each tracker gets a category, and the category decides whether it runs before consent.
`Fill with AI` fills six fields at once, with a justification and a source link per field, and
an individual `Regenerate`.

⛔ **This is where your judgement is required and cannot be delegated.** `Essential` is the
only category that skips consent entirely. Read that list yourself.
[reference/categories.md](reference/categories.md) explains what to ask of each one.

### Stage 7. The tag manager

**This is what the rest of this repository is about.** Follow the
[nine steps](reference/nine-steps.md) in the GTM interface, or use
[scripts/wire-consent.py](../scripts/wire-consent.py) for the container configuration.
Removing the site's `<noscript>`, testing browser behaviour and marking the app's checklist
still need their own checks.

For [browser verification](reference/verify-behaviour.md), identify the trackers and actions
being exercised, then compare requests, storage and consent state across choices. Equal
cookie lists or a change in their count alone cannot establish whether consent gating works.

The Gallery changes how step 2 installs the template. It does not configure regional
defaults, move triggers, add consent checks or test the site for you. Existing manual
templates are not migrated automatically by this repository.

⚠️ **It depends on stage 6.** The consent check applied to each tag mirrors the category the
app gave that tracker, so a wrong category here becomes a firing rule there.

### Stage 8. Publish

⛔ **Publishing to a production domain requires a paid plan.** The button labelled
`Publish on production` opens a purchase screen rather than publishing, which is worth knowing
before you promise a client a timeline.

Staging is free. You can install, configure, scan, categorise and test the whole thing without
paying, and pay when you go live.

### Stage 9. What the tag manager does not cover

Image pixels and the `<noscript>` block. An agent with your codebase does both.
[Doc 5](05-what-gtm-does-not-cover.md).

---

## What changes when Consent Pro ships an MCP server or a CLI

Right now the product connects to one thing: Google Tag Manager, through Google's API. That
is the whole reason the automated part of this map is a single stage.

**When Consent Pro exposes its own MCP server or a CLI**, stages 2, 3, 5, 6 and 8 become
reachable, and this table changes from one automated stage to most of them. **The structure
here is built for that**: each stage already says where it happens and why it is or is not
automatable, so the change is a column, not a rewrite.

Until then, this map is the honest version, and the honest version is the one that does not
frustrate someone in the middle of a setup.
