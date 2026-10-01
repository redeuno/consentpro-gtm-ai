# The behaviour check

This procedure observes what named trackers do before a choice, after refusal and after
acceptance. Configuration checks alone cannot show whether the live page follows the
visitor's choice.

**Configuration correct does not mean behaviour correct.** A container can pass every
structural check and still fire trackers before consent, because structure is what you
declared and behaviour is what the browser did.

---

**Cookie counts are not a verdict.** Equal lists can mean that no relevant tracker was
triggered, that tracking uses requests without cookies, or that the browser blocked storage.
A new cookie on refusal may simply store the consent choice. More cookies after acceptance
do not prove that every tracker was blocked beforehand.

## Why this is a procedure and not a script

An agent with a browser tool runs this directly, and adapts to the banner in front of it.
Every banner has different button labels, different markup and different languages, so a
script with fixed selectors can miss the controls needed for the test. Report any browser
state you cannot inspect.

If you are driving it yourself, use the browser's developer tools to inspect network
requests, cookies and other relevant storage.

---

## The procedure

### Setup

Before loading the page:

- List the trackers being tested, their categories, expected cookie or storage names,
  request destinations, and the page or action that normally triggers each one.
- Record the banner type, region, consent mode and published container version. Expected
  behaviour must match this configuration. A setup deliberately using Advanced Consent Mode
  can send cookieless Google requests while storage consent is denied, as described in
  [Google's Consent Mode overview](https://developers.google.com/tag-platform/security/concepts/consent-mode#advanced_consent_mode).
- Open developer tools before navigation and keep the Network log across reloads. Record
  request destinations and purposes as well as cookies and relevant browser storage.
- Use a fresh browser session for each branch below, with no stored choice. Keep browser
  privacy settings, extensions, region, page actions and observation period consistent.
  Record any browser blocking that could hide a tracker's expected behaviour.

If no tracker is expected on the page, choose a page or action that exercises one. An empty
page cannot demonstrate that the consent setup blocks tracking elsewhere.

### Step 1. Before touching anything

Load the page without touching the banner. Perform any agreed page actions that do not
change consent. Record the consent state, named cookies and storage entries, and relevant
network requests.

Compare each observation with the expected behaviour for that tracker and consent mode.
An identified non-essential cookie created before a choice is evidence to investigate in an
opt-in setup. A request without a cookie still needs classification.

| What you see | What it means |
|---|---|
| No relevant request or storage entry appears | Absence observed for this action; acceptance must exercise the tracker before crediting consent blocking |
| An identified tracker acts against the configured rule | Preserve the request or storage evidence and trace its source |

⭐ **Record the exact names.** They are what makes the rest of this useful, and they are what a
developer needs to trace it back to a tag.

### Step 2. Refuse everything

In a fresh session, load the same page and use its reject path. Record the action and confirm
the resulting consent state.

Repeat the same page actions and observation period, then reload and check whether the
refusal is retained. Compare named trackers, not cookie totals.

| What you see | What it means |
|---|---|
| A cookie used by the CMP to remember refusal appears | Expected when that is how the product stores the choice; establish its purpose before calling it tracking |
| An identified tracker sends a request or writes storage that its denied category should prevent | Observed behaviour conflicts with the expected rule; trace the source |
| No expected tracker activity appears | Check the acceptance branch before concluding that consent caused the absence |

### Step 3. Accept everything

Start another fresh session and record the untouched state again. Accept, confirm the new
consent state, and repeat the same actions and observation period. Inspect the expected
tracker requests, cookies and storage.

| What you see | What it means |
|---|---|
| A known tracker absent before choice and after refusal appears after acceptance | Evidence of gating for that tracker and action, within the tested consent mode |
| More cookies appear | Identify them and compare their earlier states; the count alone proves nothing about other trackers |
| Lists stay equal or the expected tracker never appears | Inconclusive without more runtime evidence; investigate its trigger, browser blocking or another delivery problem |

Acceptance is the positive control: it shows whether the chosen action actually exercises
the tracker and whether your observation method can detect it. If that tracker never
appears, you cannot credit its earlier absence to consent blocking yet.

---

## Reading the result

Compare the evidence per tracker:

```
step 1 (untouched)   →  observed requests and storage before choosing
step 2 (refused)     →  observed requests and storage with the recorded refusal
step 3 (accepted)    →  positive control using the same expected tracker action
```

Limit the conclusion to the named trackers, pages, interactions, browser and region tested.
Requests that use no cookies and trackers triggered only by other actions remain outside a
cookie-only check. A cookie storing the consent choice is not itself evidence of tracking.
Equal lists or changes in their size establish neither success nor failure on their own.

---

## What to do with what you find

Use an unexpected request, cookie or storage entry to find its source. Possible paths:

1. **It is in the tag manager on a trigger that is not wired to consent.** Run
   `scripts/audit-container.py`, which names these.
2. **It is categorised `Essential` in the app**, so it fires by design. Check the category.
   See [categories.md](categories.md).
3. **It is an image pixel.** The script cannot block those on its own. See
   [../05-what-gtm-does-not-cover.md](../05-what-gtm-does-not-cover.md).
4. **It loads before the consent layer in the page source.** Run
   `scripts/inspect-site.py`, which reports load order.

Do not pick a cause from cookie totals. Preserve the observation and test the suspected path.

---

## The debugger does part of this for you

Consent Pro ships a debugger that reports runtime state, whether the banner is correct, and
what is blocked by category before and after the choice. It is reached with a URL parameter,
and the debugger documentation page has the exact form.

Compare the reported consent state with browser requests and storage, including the request
initiator when available. A state shown by the debugger is not proof that every tracker
obeyed it. A discrepancy needs investigation; report both observations and their sources.

---

## What to write down afterwards

Keep configuration and behaviour as separate claims. They are different, and merging them is
how an overstatement gets made:

> Configured: [published version, template identity, initialization trigger, regions and
> consent checks read from the container].
>
> Observed: [named tracker and action], [request destination and relevant storage],
> [before-choice result], [refusal result], [acceptance result], in [browser and region].
>
> Not verified: [other pages, interactions, regions or tracking sources not exercised].

Fill this structure only with observations you actually made. If the acceptance branch did
not exercise the expected tracker, mark that tracker inconclusive. Do not replace missing
runtime evidence with a configuration score or a count of cookies.

⛔ **Neither of those is "the site is compliant."** Compliance is a legal judgement about a
whole site, and these are two of its inputs. Report the inputs and let the person who owns the
risk draw the conclusion.
