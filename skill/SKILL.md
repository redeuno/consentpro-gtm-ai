---
name: consent-pro-gtm
description: Wire Google Tag Manager to Consent Pro so tags respect the visitor's choice. Use for GTM consent setup, consent mode, regional defaults, or when tags fire before consent.
---

# Wiring Google Tag Manager to Consent Pro

Installing Consent Pro puts a consent layer on a site. It does not, on its own, control what
Google Tag Manager fires. This skill covers the nine steps that connect the two, in order,
with the parts that are easy to get wrong called out.

## Before anything else, establish two things

**1. Which environment are you in?** It changes what you can do, not what is correct.

| Environment | What you can do |
|---|---|
| **Terminal** with the person's Google credentials | Read the container over the API and report exactly what is set. Guide the changes; see the write policy below |
| **Web chat** (no credentials) | Generate every exact value the person types, and check what they report back. You cannot read their container, so never claim you verified it |

**2. Which documentation trail applies?** Inspect the installed script with
`scripts/inspect-site.py` rather than deciding from the site's hosting platform alone.

- The **Webflow engine**: `https://docs.consentpro.com/webflow/google-tag-manager`
- The **web app engine**, including Webflow sites managed there:
  `https://docs.consentpro.com/web-app/google-tag-manager`

For a manual setup, use **Templates > Search Gallery > Consent Pro by Finsweet > Add to
workspace**, review permissions, then confirm **Add**. This path needs no custom OAuth client
or template download. API automation still needs the OAuth client JSON and `authorise.py`.
The [Gallery listing](https://tagmanager.google.com/gallery/#/owners/finsweet/templates/gtm-template-consent-pro)
and [publisher repository](https://github.com/finsweet/gtm-template-consent-pro) govern step 2.
The product guides still showed the download flow when checked on 2026-10-01.

⛔ **Read the region section of BOTH.** Only the web app trail explains how to write region
codes, and that is where most setups fail. This is not redundancy, it is the single most
common cause of a setup that publishes cleanly and does nothing.

## The one idea that decides whether the setup works

**Detection and blocking are different things, and the first one works without the second.**

The scanner finds the cookies your tags set as soon as a tag fires on `All Pages`, which is
the default. So trackers show up in the app, neatly categorised, and everything looks handled.
**Blocking requires every step in this skill.** Without them the tags keep firing whatever the
visitor clicked.

⭐ **The app says this on its own screen**, in the Configure GTM panel: the scanner cannot see
tags inside the container, and until the container is wired to consent, the tags it fires
ignore the visitor's choice. Treat that second sentence as a task, not a disclaimer.

**Practical consequence for you:** if the person says "my trackers are all showing up
correctly", that tells you detection works and tells you nothing about blocking. Do not accept
it as evidence the setup is done.

## The write policy, and it is not negotiable

⛔ **Never write to a container you have not been explicitly pointed at, by account ID.**
A Google credential typically reaches every container that person can access, including
production for other properties and other clients. A wrong target here does not create clutter
in a sandbox, it publishes to a live site.

**Before any write:**

1. Ask for the account ID and container ID, and read back the container's name for them to
   confirm. Name confirmation catches the wrong-target case that an ID alone does not.
2. Show what you are about to change, item by item, and get an explicit yes.
3. Prefer having the person click through the interface for the first setup. It is slower and
   it leaves them able to repeat it.
4. Publishing is a separate confirmation from saving. Never bundle the two.

**Reading is different and needs no ceremony.** Use `scripts/audit-container.py` to report
what is currently set, and read it back after changes to confirm.

## The scripts, and the order they go in

| Script | When | What it does |
|---|---|---|
| `scripts/inspect-site.py` | **first, always** | reads the public page: which engine is installed, which documentation trail applies, the container, and what loads before the consent layer. **No credential needed**, so there is no reason to skip it |
| `scripts/authorise.py` | for API automation | opens the Google consent screen and stores a refresh token; skip for manual GTM setup |
| `scripts/audit-container.py` | first, and again last | reports which consent steps are in place. Read only |
| `scripts/wire-consent.py --scaffold` | before configuring | prints a category map from the container's tags, every line defaulting to the strictest category |
| `scripts/wire-consent.py` | to configure | simulates by default. `--apply` writes, `--publish` ships, and they are separate on purpose |
| `scripts/consent-template.py` | shared helper | checks template identity and the pinned Gallery version; called by the audit and configuration scripts |

**The sequence that works:** authorise once, audit to see the current state, scaffold the map,
**go through the map with the person line by line**, simulate, show the simulation, apply on
their yes, publish on a second yes, then audit again and compare. Finish with browser checks.

**Template identity:** new imports use the Gallery API and pin
`finsweet/gtm-template-consent-pro` to SHA `8a551897e5bfdecf03de59fa00058be442b7ac29`.
Preserve recognised existing templates; a compatible manual import stays manual. Do not
migrate or update it automatically. Unexpected Gallery identity/version, modified templates
or unrecognised content must stop configuration before writes. Review the reason with the
person. `--apply` includes acknowledgement of a new template's permissions.

The audit's `template_identity` reports source/version evidence and configuration signals.
Its `verified` status does not prove runtime behaviour. The Gallery path in this revision
has not been exercised in a live workspace. Do not describe local tests as a live setup test.
For future publisher updates, follow the review, accept, test and publish sequence in
[`nine-steps.md`](../docs/reference/nine-steps.md#2-add-the-consent-pro-template-from-the-gallery).

⛔ **The map is where the person's judgement is required, not yours.** Essential is the only
category that fires without asking, so read those lines aloud with them. The scaffold defaults
everything to the strictest category precisely so that an unread file over-blocks instead of
letting everything through.

## The nine steps

Full detail in [`reference/nine-steps.md`](../docs/reference/nine-steps.md). The order matters: steps
three and five create the pieces everything else depends on.

1. Remove the tag manager `<noscript>`
2. Add Consent Pro by Finsweet from the Gallery; preserve recognised existing templates
3. Create the initialization tag, on **Consent Initialization, All Pages**
4. Set the regional defaults
5. Create the `Consent Updated` trigger for the event `consent-updated`
6. Move marketing and non-Google tags onto it
7. Add the per-tag consent checks
8. Submit and publish
9. Mark it done in the app

## The three places setups break

**Regions.** See [`reference/regions.md`](../docs/reference/regions.md). The default banner is written
as exactly `Global`, never the screen label `Global (default)`. The app's `EU` option is an
interface shortcut that must be expanded country by country. A wrong region saves and publishes
with no error, and the defaults silently never apply.

**Categories.** See [`reference/categories.md`](../docs/reference/categories.md). `Essential` is the
only category that skips consent entirely, so a tracker marked essential by mistake fires on
refusal while looking correctly configured. Automatic suggestions are a fine starting point and
a poor final answer for this one field.

**Verification.** See [`reference/verify.md`](../docs/reference/verify.md). The app's own checkbox
records that someone said it was done; it tests nothing. Test behaviour by exercising named
trackers and comparing their requests, relevant storage and consent state across choices.

## How to run this with someone

**Establish the state first.** Do not start at step one. Read the container, or ask them what
exists, and find out which of the nine are already done. Setups are usually partial, and the
common shape is tags detected but nothing wired.

**Work in the order above, one step at a time.** Confirm each one before moving on. A step
skipped early makes every later step look broken.

**Finish by testing behaviour, not configuration.**
[`reference/verify-behaviour.md`](../docs/reference/verify-behaviour.md) is the only check that
watches what the browser actually did, and **if you have a browser tool, you can run it
yourself**. Identify the expected trackers and actions first. Observe their requests and
storage before choosing, after refusal and after acceptance in fresh, comparable sessions.
Record browser, region and consent mode, and use acceptance to confirm that the test can
exercise and detect each tracker. Configuration checks alone are insufficient.

**Equal cookie lists are inconclusive without runtime evidence.** A cookie added on refusal
may store the CMP choice, and an increase after acceptance does not prove that all trackers
were blocked beforehand. Identify each cookie or request by source and purpose. Report only
the trackers and actions tested; do not infer a working or broken consent layer from counts.

**When something does not match, go to
[`reference/troubleshooting.md`](../docs/reference/troubleshooting.md)** before theorising. Six known
shapes cover most of it, and each one has a distinct symptom.

## What this skill will not do

- **Decide whether a tracker is essential.** That is a legal and product judgement about the
  specific site. Lay out what the tracker does and let the person decide.
- **Promise compliance.** A correctly wired container is one part of it. Say what was
  configured and what was verified, and let the person draw the conclusion.
- **Infer Google CMP certification from Gallery approval.** Report only the approval or
  certification supported by its own source.
- **Claim to have verified anything you did not read yourself.** In web chat you cannot see
  their container. Report what they told you as what they told you.
