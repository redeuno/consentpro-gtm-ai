# Verifying the setup

The app's own checkbox records that someone said it was done. These are the checks that tell
you whether it is.

**The first three read configuration. The last two load the page.** A setup can pass all of
the first three and fail both of the last two, which is why the order ends where it does.

⭐ **6.4 and 6.5 have their own page now:
[verify-behaviour.md](verify-behaviour.md)**, with the full procedure for comparing named
trackers, requests and storage across consent choices. If you only do one
check on this page, do that one: it is the only one that watches what the browser actually
did.

---

## 6.1 The container is published

Not saved, published. Open the version history and confirm the live version is the one with
your changes, rather than a workspace nobody shipped.

**Why first:** if this fails, every other check is measuring the old container, and the results
mean nothing.

---

## 6.2 The initialization tag is on the right trigger

It must be **Consent Initialization - All Pages**, not **All Pages**.

Also check which template that tag uses. `audit-container.py` prints `TEMPLATE SOURCE` and
adds `template_identity` to its JSON report:

| Field | What it tells you |
|---|---|
| `status` | `missing`, `verified` or `blocked` according to the script's identity checks |
| `source` | `gallery` or `manual` when identified |
| `version` | the Gallery SHA, or `null` for a manual import |
| `templateId` | the template the tag should reference |
| `detail` | the evidence or reason that needs attention |

Here, `verified` describes the script's template identity checks, not live consent behaviour.
A recognised manual template has compatible content but no proven Gallery origin or version.
An unexpected Gallery identity/version or modified template blocks configuration. The
auditor must not confirm the initialization tag from its display name alone.

For this revision the accepted Gallery version is
`8a551897e5bfdecf03de59fa00058be442b7ac29`, from
[`finsweet/gtm-template-consent-pro`](https://github.com/finsweet/gtm-template-consent-pro).
Read the [existing-template and update rules](nine-steps.md#2-add-the-consent-pro-template-from-the-gallery)
before replacing or updating anything. Local tests of the importer do not prove that this
Gallery version has run in a live workspace or on a live site.

**What failure looks like:** intermittent. Sometimes tags are held, sometimes not, depending on
what loaded first. Intermittent consent behaviour almost always traces back to this.

---

## 6.3 The region row matches the banner

Open the tag, open the region table, compare against the banner's geotarget **code by code**.
See [`regions.md`](regions.md).

**What failure looks like:** nothing. It saves, it publishes, and the defaults never apply to
the visitors they were meant for.

---

## 6.4 Load the site and refuse everything

Start with a fresh session and developer tools open before loading. Record the untouched
state, decline in the banner, and exercise the expected trackers with the same page actions.
Inspect named cookies, relevant storage and network requests, then reload to check that the
refusal is retained. Record the browser, region and consent mode.

**What you are looking for:** a known tracker acting against the configured rule for its
denied category. A new cookie that remembers refusal is not itself evidence of tracking.
Identify names, destinations and purposes rather than comparing cookie totals.

**This is the first check that tests behaviour rather than configuration**, and it is the one
that cannot be skipped. Everything above reads settings.

---

## 6.5 Accept, and exercise the expected trackers

In another fresh session, accept and repeat the same page actions and observation period.
Check that the expected tracker actually runs and that you can observe its requests or
storage. This positive control makes the earlier absence interpretable.

Equal cookie lists are inconclusive: the tracker may use no cookies, lack a firing event or
be blocked by the browser. More cookies after acceptance also do not prove that every tracker
was blocked beforehand. Follow [the full procedure](verify-behaviour.md) and report results
per tracker, within the tested pages, actions and consent mode.

---

## The debugger does most of 6.4 and 6.5

It reports runtime state, whether the banner is correct, and what is blocked by category before
and after the choice. It is reached by adding a parameter to the site URL; the debugger
documentation page has the exact form.

Use it to compare the reported consent state with browser requests and storage. The debugger
does not replace observation of the named trackers.

---

## What to say when reporting the result

**Say what was configured and what was verified, separately.** They are different claims:

- "The container is published with the initialization tag on Consent Initialization, the region
  row matching the banner, and consent checks on the marketing and analytics tags." That is
  configuration, read from the container.
- "For the named trackers and actions tested, the expected requests and storage were absent
  after refusal and present after acceptance." Use this only when both branches were
  observed, and include browser, region, consent mode and any untested cases.

⛔ **Never merge the two into "the setup is compliant".** Compliance is a legal conclusion about
a specific site, and a correctly wired container is one input to it. Report the inputs.

⛔ **And never report a check you did not run.** In a web chat with no access to the container,
everything above is something the person did and told you about. Write it that way.
