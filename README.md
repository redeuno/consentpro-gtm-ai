# consentpro-gtm-ai

Wire Google Tag Manager to Consent Pro by handing the work to an AI agent.

Connecting the two is nine steps of clicking through menus. Almost all of it is an API call
underneath, so an agent can do it while you supply the handful of decisions only you can make.

---

## Where this fits, before anything else

Setting up Consent Pro is nine stages. **This repository automates one of them**, and it is
the one users report as the hardest.

| # | Stage | Agent? |
|---|---|---|
| 0 | Google Cloud and tag manager account | partly, once |
| 1 | Sign in, pick a workspace | no, the app |
| 2 | Connect Domain | no, the app |
| 3 | Configure Banner | no, the app |
| 4 | Install the core script | the site half, yes |
| 5 | Scan the site | no, the app |
| 6 | Categorise the trackers | no, and your judgement is required |
| 7 | **Wire Google Tag Manager** | ⭐ **yes, fully. This is what this repo does** |
| 8 | Publish | no, and production needs a paid plan |
| 9 | Image pixels and the `<noscript>` | yes, with your codebase |

**Stage 7 is automated because it is the only stage that happens in a system with a public
API.** The others happen inside the Consent Pro app, which today has no public API and no MCP
server. An agent cannot press a button on a screen it cannot reach.

⭐ It also happens to be the stage that hurts most: **63% of Consent Pro users use Google Tag
Manager, and it is reported as the most painful step**.

**[The full map, stage by stage, is in docs/00-the-journey.md](docs/00-the-journey.md)**, built
by walking the product end to end and capturing every screen in order. Read it before you
start, so nothing surprises you halfway through.

---

## Start here

| Step | Document | Time |
|---|---|---|
| 0 | [The whole journey](docs/00-the-journey.md) | 5 min, read first |
| 1 | [Google Cloud, once](docs/01-google-cloud-setup.md) | 15 min |
| 2 | [The tag manager account](docs/02-tag-manager-account.md) | 2 min |
| 3 | [Authorise once](docs/03-authorise.md) | 3 min |
| 4 | [Hand it to the agent](docs/04-run-it.md) | the agent's part |
| 5 | [What the tag manager does not cover](docs/05-what-gtm-does-not-cover.md) | 5 min, and it is the one people skip |

**New to the Google Cloud console?** Section 1.0 of the first document explains what it is,
what enabling an API means, and what this opens up beyond this one setup. It is worth the ten
minutes if the console is unfamiliar.

**Two things genuinely cannot be automated by anyone**, and they are both in stage 0. Creating
a tag manager account, because the interface demands a container name on the same screen and no
API path skips it. And approving a credential, because it ends at a Google consent screen a
person clicks.

---

## Before you start

- **Consent Pro installed and verified on the site.** The app's own `Verify installation` must
  pass. Wiring a container to a consent layer that is not there produces a trigger nothing
  fires. See the [installation docs](https://docs.consentpro.com/web-app/install).
- **A recent scan.** The agent maps each tracker's category, and categories come from the scan.
- **Python 3.** The scripts use only the standard library.
- **An agent that can run commands**, for the automated path. A web chat can still generate
  every exact value for you to type; section 06 of the guide covers that.

---

## What is in here

```
docs/
  01-google-cloud-setup.md    the console, in detail, with the decision that bites later
  02-tag-manager-account.md   the other thing that cannot be automated
  03-authorise.md             the single browser step
  04-run-it.md                the four values, the prompt, the sequence
  05-what-gtm-does-not-cover.md   image pixels, and the other two gaps
  reference/
    nine-steps.md             every step, and what differs between the two doc trails
    regions.md                region codes, and the case that breaks setups
    categories.md             category to consent check, and the essential question
    verify.md                 five checks, three of configuration and two of behaviour
    troubleshooting.md        six failure shapes, each with its symptom
skill/
  SKILL.md                    point an agent at this
scripts/
  authorise.py                one-time browser authorisation
  audit-container.py          reports which consent steps are in place. Read only
  wire-consent.py             does the configuration. Simulates by default
```

---

## The one idea worth reading even if you skip everything else

**Detection and blocking are different things, and the first works without the second.**

The Consent Pro scanner finds the cookies your tags set as soon as a tag fires on `All Pages`,
which is the default. So your trackers show up in the app, neatly categorised, and the setup
looks handled. **Blocking requires every step in this repository.** Without them the tags keep
firing whatever the visitor clicked.

The app says so on its own screen, in the Configure GTM panel: until the container is wired to
consent, the tags it fires ignore the visitor's choice. That sentence is a task, not a
disclaimer.

Run `scripts/audit-container.py` to find out which side of that line a container is on.

---

## Security

**[Read SECURITY.md](SECURITY.md) before running anything.** The short version:

A Tag Manager write scope reaches **every container that Google account can access**, including
other clients and production properties. There is no per-container scope. The scripts confirm
the account by its live name, simulate by default, require a second flag to publish, and refuse
to create a version from half-applied state. The audit script has no write path at all.

The scripts are short and dependency-free so that reading them is realistic. Do that once.

---

## Scope, and what this is not

This covers **Google Tag Manager**. Installing Consent Pro, configuring banners, the policy
generator and image trackers are separate topics with their own documentation.

It does not decide whether a tracker is essential, and it does not assert that a site is
compliant. It configures a container and proves what it configured. The conclusion is yours.

---

## Where this came from

The nine steps are the official Consent Pro documentation, both the Webflow trail and the web
app trail, read in September 2026. **The emphasis comes from carrying the setup out end to end
and measuring the result**, including getting the region wrong on the first attempt in exactly
the way `docs/reference/regions.md` warns about.

**Where this disagrees with the documentation, the documentation is right and this is out of
date.** Check [docs.consentpro.com](https://docs.consentpro.com) before relying on a detail.

This is an independent guide. It is not published by Finsweet and carries no warranty.
