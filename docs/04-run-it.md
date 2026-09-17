# 4. Hand it to the agent

Everything from here is API calls, so this is the part the agent does. Your job is to supply
four values and to read one file carefully.

## The four values the agent cannot work out

| Value | Where you find it | Why it has to come from you |
|---|---|---|
| **Account ID and container ID** | step 2 | the credential reaches many containers, and choosing one for you is exactly the mistake that publishes to the wrong site |
| **Banner type**<br>opt-in, opt-out, do-not-sell or informational | Consent banner, in the Consent Pro app | it decides whether every regional default is denied or granted, which is the difference between blocking and not blocking |
| **Regions** | Consent banner, Banners, the Geotarget control | the app's display value and the tag manager's expected code are different strings. [reference/regions.md](reference/regions.md) |
| **Which trackers are genuinely essential** | your judgement about your site | it is a legal and product decision, and the one field where a wrong automatic answer causes harm no check catches |

## A prompt that works

```
Wire my Google Tag Manager container to Consent Pro, following the official
documentation. Read skill/SKILL.md in this repository first.

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

# 7. prove it
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

Steps two through eight of the official guide, detailed in
[reference/nine-steps.md](reference/nine-steps.md): imports the template, creates the
initialization tag with your regional defaults, creates the `consent-updated` trigger, moves
each tag onto it, applies the consent checks from your map, creates a version and publishes.

The write calls themselves take a few seconds. Most of the elapsed time is you reading the map.

## Then verify, and two of the checks are yours

[reference/verify.md](reference/verify.md) has five. The agent can do three, because they read
configuration. **Only you can do the last two**, because they mean loading the site in a private
window, refusing, and looking at what cookies are there.

⛔ **Do not accept "the setup is compliant" from an agent.** It configured a container and it
can prove what it configured. Compliance is a judgement about a whole site. Ask for two separate
lists, what was configured and what was verified, and draw the conclusion yourself.

## Step nine is on screen

Ticking the tag manager confirmation inside the Consent Pro app. On Webflow it is the
**Actions** tab; on the web app it is **Overview**, **Data Privacy Check**, the **Configure
GTM** row. Do it after the container is published, and know that it records that somebody said
so rather than testing anything.
