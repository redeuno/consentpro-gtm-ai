# Verifying the setup

The app's own checkbox records that someone said it was done. These are the checks that tell
you whether it is.

**The first three read configuration. The last two load the page.** A setup can pass all of
the first three and fail both of the last two, which is why the order ends where it does.

⭐ **6.4 and 6.5 have their own page now:
[verify-behaviour.md](verify-behaviour.md)**, with the full procedure, what each of the three
cookie lists means, and how to trace anything that should not be there. If you only do one
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

Private window, load the page, decline in the banner. Then open the browser's cookie list for
that domain.

**What you are looking for:** anything non-essential that is present has not been held.

**This is the first check that tests behaviour rather than configuration**, and it is the one
that cannot be skipped. Everything above reads settings.

---

## 6.5 Accept, and watch them arrive

Same window, accept. The cookies that were absent should appear.

**If nothing changes either way**, the trigger is not receiving the event and the container is
effectively inert. Check the event name in step five, and confirm the core script is actually
loading on the page.

---

## The debugger does most of 6.4 and 6.5

It reports runtime state, whether the banner is correct, and what is blocked by category before
and after the choice. It is reached by adding a parameter to the site URL; the debugger
documentation page has the exact form.

It is also the natural tool for an automated agent to check its own work, because it reports
state rather than requiring someone to read a cookie list.

---

## What to say when reporting the result

**Say what was configured and what was verified, separately.** They are different claims:

- "The container is published with the initialization tag on Consent Initialization, the region
  row matching the banner, and consent checks on the marketing and analytics tags." That is
  configuration, read from the container.
- "Loading the site and declining leaves no non-essential cookies." That is behaviour, observed
  on the page.

⛔ **Never merge the two into "the setup is compliant".** Compliance is a legal conclusion about
a specific site, and a correctly wired container is one input to it. Report the inputs.

⛔ **And never report a check you did not run.** In a web chat with no access to the container,
everything above is something the person did and told you about. Write it that way.
