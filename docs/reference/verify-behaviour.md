# The behaviour check

Everything else in this repository reads configuration. **This is the only check that watches
what actually happens**, and it is the one that answers the question a client asks.

**Configuration correct does not mean behaviour correct.** A container can pass every
structural check and still fire trackers before consent, because structure is what you
declared and behaviour is what the browser did.

---

## Why this is a procedure and not a script

An agent with a browser tool runs this directly, and adapts to the banner in front of it.
Every banner has different button labels, different markup and different languages, so a
script with fixed selectors breaks on the second site it meets. **A procedure does not.**

If you are driving it yourself, the same steps work by hand in about three minutes. The
browser's own developer tools show you the cookies.

---

## The procedure

### Setup

Open the site in a **fresh private window**. Private matters: a previous visit leaves a stored
choice, and the banner will not appear at all. If you see no banner, that is the first thing
to check, not a finding.

### Step 1. Before touching anything

**Do not click the banner.** List the cookies for the domain.

**What you are looking at:** every cookie present at this moment was set **without consent**.

| What you see | What it means |
|---|---|
| Nothing, or only the consent tool's own cookie | the consent layer is holding trackers. Correct |
| An analytics or advertising cookie | **it fired before the visitor chose.** This is the finding |

⭐ **Record the exact names.** They are what makes the rest of this useful, and they are what a
developer needs to trace it back to a tag.

### Step 2. Refuse everything

Find the reject path. It may be a `Reject all` button, or it may be behind `Preferences` with
every toggle left off, which is itself worth noting: **a refuse path that takes three clicks
while accept takes one is a finding of its own.**

Refuse, then reload the page, then list the cookies again.

| What you see | What it means |
|---|---|
| Same as step 1, or fewer | consistent |
| **More than step 1** | **something fires on refusal.** The worst outcome, and the one that produces complaints |

### Step 3. Accept everything

Clear the site data, reload, and this time accept. List the cookies again.

| What you see | What it means |
|---|---|
| More than in step 2 | **the gate works.** Trackers were held and released on consent |
| The same as step 2 | **the gate is not connected.** Either nothing was ever held, or the tags are not wired to the consent event |

⛔ **If steps 1, 2 and 3 give the same list, the consent layer is decorative on this site.**
It shows a banner and changes nothing. That is the single most important thing this check can
tell you, and no amount of configuration review would have found it.

---

## Reading the result

Three lists, and the relationship between them is the answer:

```
step 1 (untouched)   →  what fires with no choice made
step 2 (refused)     →  what fires against the visitor's wishes
step 3 (accepted)    →  what the site actually loads
```

**Healthy looks like:** step 1 small or empty, step 2 equal to step 1, step 3 noticeably
larger.

**Broken looks like:** all three roughly equal.

**Alarming looks like:** step 2 larger than step 1.

---

## What to do with what you find

**A tracker present in step 1 or 2** needs tracing. In order of likelihood:

1. **It is in the tag manager on a trigger that is not wired to consent.** Run
   `scripts/audit-container.py`, which names these.
2. **It is categorised `Essential` in the app**, so it fires by design. Check the category.
   See [categories.md](categories.md).
3. **It is an image pixel.** The script cannot block those on its own. See
   [../05-what-gtm-does-not-cover.md](../05-what-gtm-does-not-cover.md).
4. **It loads before the consent layer in the page source.** Run
   `scripts/inspect-site.py`, which reports load order.

Those four cover nearly everything, and each has a different fix.

---

## The debugger does part of this for you

Consent Pro ships a debugger that reports runtime state, whether the banner is correct, and
what is blocked by category before and after the choice. It is reached with a URL parameter,
and the debugger documentation page has the exact form.

**It is faster than reading cookie lists and it is not a replacement.** The debugger reports
what the product believes it is doing. The cookie list reports what the browser did. When they
disagree, the browser is right, and the disagreement is the finding.

---

## What to write down afterwards

Keep configuration and behaviour as separate claims. They are different, and merging them is
how an overstatement gets made:

> **Configured:** the container is published, the init tag is on Consent Initialization, the
> region row matches the banner, and consent checks are applied to the marketing and analytics
> tags.
>
> **Verified:** loading the site in a private window and refusing leaves no non-essential
> cookies. Accepting loads them.

⛔ **Neither of those is "the site is compliant."** Compliance is a legal judgement about a
whole site, and these are two of its inputs. Report the inputs and let the person who owns the
risk draw the conclusion.
