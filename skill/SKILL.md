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

**2. Which documentation trail applies?** The nine steps are identical; the details differ.

- A **Webflow** site: `https://docs.consentpro.com/webflow/google-tag-manager`
- **Any other** site: `https://docs.consentpro.com/web-app/google-tag-manager`

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
| `scripts/authorise.py` | once per machine | opens the Google consent screen and stores a refresh token. The only step that needs a human at a browser |
| `scripts/audit-container.py` | first, and again last | reports which consent steps are in place. Read only |
| `scripts/wire-consent.py --scaffold` | before configuring | prints a category map from the container's tags, every line defaulting to the strictest category |
| `scripts/wire-consent.py` | to configure | simulates by default. `--apply` writes, `--publish` ships, and they are separate on purpose |

**The sequence that works:** authorise once, audit to see the current state, scaffold the map,
**go through the map with the person line by line**, simulate, show the simulation, apply on
their yes, publish on a second yes, then audit again and compare.

⛔ **The map is where the person's judgement is required, not yours.** Essential is the only
category that fires without asking, so read those lines aloud with them. The scaffold defaults
everything to the strictest category precisely so that an unread file over-blocks instead of
letting everything through.

## The nine steps

Full detail in [`reference/nine-steps.md`](../docs/reference/nine-steps.md). The order matters: steps
three and five create the pieces everything else depends on.

1. Remove the tag manager `<noscript>`
2. Import the Consent Pro template
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
records that someone said it was done; it tests nothing. Only loading the page, refusing, and
inspecting cookies tests behaviour.

## How to run this with someone

**Establish the state first.** Do not start at step one. Read the container, or ask them what
exists, and find out which of the nine are already done. Setups are usually partial, and the
common shape is tags detected but nothing wired.

**Work in the order above, one step at a time.** Confirm each one before moving on. A step
skipped early makes every later step look broken.

**Finish by testing behaviour, not configuration.**
[`reference/verify-behaviour.md`](../docs/reference/verify-behaviour.md) is the only check that
watches what the browser actually did, and **if you have a browser tool, you can run it
yourself**. Three cookie lists: before touching the banner, after refusing, after accepting.
Everything else in this skill reads settings, which is necessary and not sufficient.

⛔ **If all three lists are the same, the consent layer is decorative on that site.** It shows
a banner and changes nothing. No amount of configuration review finds that, and it is the most
important thing you can tell someone.

**When something does not match, go to
[`reference/troubleshooting.md`](../docs/reference/troubleshooting.md)** before theorising. Six known
shapes cover most of it, and each one has a distinct symptom.

## What this skill will not do

- **Decide whether a tracker is essential.** That is a legal and product judgement about the
  specific site. Lay out what the tracker does and let the person decide.
- **Promise compliance.** A correctly wired container is one part of it. Say what was
  configured and what was verified, and let the person draw the conclusion.
- **Claim to have verified anything you did not read yourself.** In web chat you cannot see
  their container. Report what they told you as what they told you.
