# 4. Hand it to the agent

This is the API automation path. Complete the
[OAuth setup](01-google-cloud-setup.md) and [authorisation](03-authorise.md), then supply four
values and review the category map. For setup through the GTM interface, use the
[nine steps](reference/nine-steps.md); that path needs no custom OAuth client.

> **Which documentation trail applies to you.** The nine steps are identical either way; the
> details differ, and the region section differs the most.
>
> | Your site | Trail |
> |---|---|
> | Built and hosted in Webflow | [the Webflow guide](https://docs.consentpro.com/webflow/google-tag-manager) |
> | **Astro, Next, Nuxt, SvelteKit, Remix, plain HTML, anything you deploy yourself** | [the web app guide](https://docs.consentpro.com/web-app/google-tag-manager) |
>
> ⚠️ **A Webflow project managed from the web app follows the web app trail**, and that case is
> real rather than hypothetical. **The script address tells you which**, with no guessing:
> `/v2/cdn/runtime.js` is the Webflow engine, `/cdn/core/` is the web app. Look at your own
> page source, or ask the agent to.

## The four values the agent cannot work out

| Value | Where you find it | Why it has to come from you |
|---|---|---|
| **Account ID and container ID** | step 2 | the credential reaches many containers, and choosing one for you is exactly the mistake that publishes to the wrong site |
| **Banner type**<br>opt-in, opt-out, do-not-sell or informational | Consent banner, in the Consent Pro app | it decides whether every regional default is denied or granted, which is the difference between blocking and not blocking |
| **Regions** | Consent banner, Banners, the Geotarget control | the app's display value and the tag manager's expected code are different strings. [reference/regions.md](reference/regions.md) |
| **Which trackers are genuinely essential** | your judgement about your site | it is a legal and product decision, and the one field where a wrong automatic answer causes harm no check catches |

## A prompt that works

```
Wire my Google Tag Manager container to Consent Pro. Read skill/SKILL.md in this
repository first, including the Gallery installation and existing-template rules.

  account:    1234567890
  container:  GTM-XXXXXXX
  banner:     opt-in
  regions:    Global

Audit the container first and show me what is already set. Then scaffold the
category map and go through it with me line by line before applying anything.
Publish only when I say so.
```

**Why each line is there:**

- **Naming the target** stops the agent choosing a container, which is the failure that reaches
  a live site.
- **Audit first** means you find out the setup is already half done before something overwrites
  it.
- **The map line by line** is the one place your judgement is required, and an agent left alone
  will fill it plausibly and wrongly.
- **Publish only when I say so** separates configuring from shipping. The script enforces this
  too, with two separate flags, but say it anyway.

## The sequence, if you are driving it yourself

```bash
# 1. what is there now
python scripts/audit-container.py --account 123 --container GTM-XXX
#    it prints the account name and tells you what to pass back
python scripts/audit-container.py --account 123 --container GTM-XXX \
    --confirm-name "Your Account Name"

# 2. build the category map
python scripts/wire-consent.py --account 123 --container GTM-XXX \
    --confirm-name "Your Account Name" --scaffold > map.json

# 3. READ map.json AND FIX IT. see below.

# 4. simulate. nothing is written
python scripts/wire-consent.py --account 123 --container GTM-XXX \
    --confirm-name "Your Account Name" \
    --banner opt-in --regions Global --map map.json

# 5. apply, still not published
python scripts/wire-consent.py ... --map map.json --apply

# 6. publish
python scripts/wire-consent.py ... --map map.json --apply --publish

# 7. read back configuration; browser verification follows separately
python scripts/audit-container.py --account 123 --container GTM-XXX \
    --confirm-name "Your Account Name"
```

## Step 3 is the one that matters

`--scaffold` writes a line per tag, **every one defaulting to `marketing`**, which is the
strictest category. That default is not a guess at what your tags are. It is chosen so that a
file applied without reading **over-blocks**, which you notice in minutes, rather than letting
everything through, which nothing tells you about.

```json
{
  "GA4 Configuration": "analytics",
  "Meta Pixel": "marketing",
  "Session cookie helper": "essential",
  "Old test tag": "skip"
}
```

| Value | Effect |
|---|---|
| `marketing` | requires the three advertising consents |
| `analytics` | requires analytics consent |
| `personalization` | requires personalization consent |
| `essential` | **no check at all. Fires whatever the visitor chose** |
| `skip` | the script leaves that tag completely alone |

**Read every `essential` line out loud.** Ask one question of each: does the site stop working
without this tracker? Session handling, security and fraud prevention usually qualify. Anything
that measures, attributes or personalises does not, however convenient it would be.

## What the agent does with all that

The container operations are detailed in [reference/nine-steps.md](reference/nine-steps.md).
For a new template, the script imports from the Gallery with owner `finsweet`, repository
`gtm-template-consent-pro` and pinned SHA `8a551897e5bfdecf03de59fa00058be442b7ac29`.
It preserves recognised existing templates, including compatible manual imports, with no
automatic migration. A modified or unrecognised template stops the run before configuration
writes. Review the audit's source and version before approving changes.

With `--apply`, it configures the initialization tag and regional defaults, creates the
`consent-updated` trigger, applies the category map and creates an unpublished version.
Only `--apply --publish` also publishes that version. New Gallery imports acknowledge template permissions as part of
`--apply`; review them before approving the simulation.

The Gallery path in this revision has not been exercised in a live GTM workspace. Local tests
and official API documentation do not substitute for readback and browser checks on your
target site.

## Then verify, and two of the checks are yours

[reference/verify.md](reference/verify.md) separates configuration from browser behaviour.
The audit reports template identity and configuration signals; it cannot prove that a page
respects consent. A person or an agent with browser access must load the site, refuse and
accept, and inspect the resulting behaviour.

⛔ **Do not accept "the setup is compliant" from an agent.** It configured a container and it
can prove what it configured. Compliance is a judgement about a whole site. Ask for two separate
lists, what was configured and what was verified, and draw the conclusion yourself.

## Step nine is on screen

Ticking the tag manager confirmation inside the Consent Pro app. On Webflow it is the
**Actions** tab; on the web app it is **Overview**, **Data Privacy Check**, the **Configure
GTM** row. Do it after the container is published, and know that it records that somebody said
so rather than testing anything.
