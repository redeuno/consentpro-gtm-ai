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

An agent with permitted browser access runs this procedure and adapts to the banner in front of it.
Every banner has different button labels, different markup and different languages, so a
script with fixed selectors can miss the controls needed for the test. Report any browser
state you cannot inspect.

If the customer is driving, offer the relevant short instruction below and check its
result before introducing another tool. A terminal, Google API access and a complete
container export are not prerequisites.

### MCP page audit and access limits

When the discovered `consentpro_site_audit` contract is available, follow the
[published-page audit](https://docs.consentpro.com/mcp/site-audit) procedure. Its
prepare phase reads expectations; the client's browser supplies observations.
It is not a remote browser test performed by MCP. Show the exact page and expected
behavior for confirmation before navigation, and retain that contract's approval
boundary even for a connected project. Default to the homepage; another exact
page requires the customer's request and confirmation. Do not crawl other pages.

An API/MCP-only restriction remains in effect. Complete allowed configuration
reads and report browser scenarios as unverified instead of opening a browser or
inventing observations for assessment. Audit results propose fixes; they do not
authorize edits, imports, checklist updates, publication or rollback. A single-page
audit does not change the hostname-wide installation requirement.

## First activation and further verification

Start with the selected site's initial page and main visitor action, the integrations
affected by this installation and any known failure. Confirm the banner, choices and
preferences control visibly work. Test the relevant named sources across the choice
states below and check the main site function separately. Do not expand this into an
audit of every page, browser, region and historical tracker before first publication.

Use a draft or isolated test target where available. After authorized publication, repeat
the relevant checks on the ordinary address outside preview.

For production release testing, use the tester's own site, workspace and container.
Connecting the production MCP does not approve site edits, tracker insertion or publication.
Record which product environment supplied the project snippet; a public test hostname
does not make a staging project a production project. A production preview is still a draft.

Keep these results separate:

| Result | Evidence needed |
|---|---|
| Banner publication observed | Intended banner and usable choice/preferences controls on the ordinary target, with its environment recorded |
| Named integrations verified | Requests/storage compared across the relevant consent states and expected actions |
| Main site function verified | The agreed visitor action reached its expected result under the tested choices |

Visual checks alone can establish the first result, not the other two. State which checks
remain unverified and who will finish them. Do not recommend publication with a known leak
or broken main function. Resolve the cause or agree a supported temporary change, then
retest; an unresolved blocker needs a handoff, not later personalization. Explain missing
verification before a publication decision without presenting unknown behavior as success.
Broader coverage and optional styling follow activation without erasing those limits.
Resume through [onboarding](onboarding.md).

## Guide a beginner through the browser

Use only the next relevant instruction, in the customer's language. Begin with the
visible checks: open the target, choose the appropriate reject/accept path, reopen
preferences, change the choice and reload. Ask what appeared and whether the controls
worked. A cropped screenshot can support that observation; it cannot prove tracking behavior.

### Prepare a fresh session

In Chrome, use the three-dot menu, **New Incognito window**, for a separate test session.
Another Incognito window shares that private session. For an independent branch, save any
private-window work before closing all Incognito windows and reopening one, or use a
separate test profile. Keep browser settings consistent. Incognito blocks third-party
cookies by default, so missing cookies may reflect the browser, not Consent Pro. Do not
disable privacy protections automatically. Source: [Chrome Incognito](https://support.google.com/chrome/answer/95464).

Use the equivalent supported route for the customer's browser. If controls differ, ask
which browser and screen are open rather than repeating unavailable instructions. A signed
debugger's **Reset Banner** can reset the test choice, but does not by itself establish
that all tracker storage was cleared.

### Observe one named request and storage item

The agent first supplies the actual destination or storage name and the safe page action
expected to trigger it, based on the selected integration. Do not ask the customer to
guess what every request means.

1. In Chrome, open **More tools > Developer tools**, or press `Ctrl+Shift+I` on Windows/Linux
   or `Command+Option+I` on Mac. Select **Network** before loading the test page.
2. Enable **Preserve log**, leave recording on and select **All** request types. Enter the
   named host or resource in **Filter**. Keep the same filter and action for comparison.
3. Load the page, perform the agreed action and note whether the request appeared before
   or after the choice. A blocked/failed row is not proof that the destination received it.
4. If the named item is a cookie, open **Application > Storage > Cookies**, select its
   origin and find its name. Note presence and relevant metadata, not its value. If the
   integration uses another storage type, guide that specific pane instead.
5. Repeat the same observation for refusal and acceptance. An absent result after both
   remains inconclusive; use the [acceptance control](#step-3-accept-everything).

Sources: [open Chrome DevTools](https://developer.chrome.com/docs/devtools/open),
[network inspection](https://developer.chrome.com/docs/devtools/network),
[preserve the network log](https://developer.chrome.com/docs/devtools/network/reference)
and [inspect cookies](https://developer.chrome.com/docs/devtools/application/cookies).
For Edge, start from its [DevTools entry](https://learn.microsoft.com/en-us/microsoft-edge/devtools/overview)
and confirm the available panels. These instructions do not require pasting code into a console.

Share only the named destination, action, consent state, presence/absence, relevant blocked
status and browser. Keep cookie values, request payloads, query identifiers, authorization
headers, signed preview URLs and unrelated tabs out of chat and screenshots. Do not request
a full HAR/network export by default. If deeper evidence is necessary, explain the exact
need and use an agreed private, minimized handoff. If the customer cannot obtain it, retain
the visible results and use [support](troubleshooting.md#support-and-assisted-setup), labeling
technical behavior unverified rather than repeating an unsuccessful DevTools sequence.

## Check the main site function separately

Choose the main action affected by this installation, not every feature on the site.
Agree a safe test and expected result before running it, then compare the relevant consent
states. Use a test account or sandbox where needed. Do not make a real payment, submit a
live lead, send email or reserve an appointment without explicit authorization for that
action. If the test stops before submission, record that completion was not tested.

| Function present on this site | Observe separately from tracking |
|---|---|
| Form or checkout | Fields, navigation and the agreed test confirmation work; record any step not submitted |
| Login | The authorized test account can complete the agreed flow and retain its session |
| Video, scheduler or embed | Held content explains how to continue, preferences remain reachable and the permitted function loads after the appropriate choice |
| Dynamic navigation | The main path and preferences remain usable after navigation; relevant events are not duplicated |

Keep "the visitor action worked" separate from "its conversion request respected the choice".
Preserve purchase, form and other business-event conditions. If a function breaks, attribute
the dependency before changing it; follow [classification review](categories.md), not a blanket
Essential classification. A successful functional test does not prove consent enforcement.

---

## The procedure

### Setup

Before loading the page:

- List the relevant named trackers being tested, their categories, expected cookie or
  storage names, request destinations, and the page or action that normally triggers each one.
- Record the banner type, region, consent mode and published container version. Expected
  behaviour must match this configuration. A setup deliberately using Advanced Consent Mode
  can send cookieless Google requests while storage consent is denied, as described in
  [Google's Consent Mode overview](https://developers.google.com/tag-platform/security/concepts/consent-mode#advanced_consent_mode).
- Record whether this tab uses a saved-draft preview or ordinary published configuration,
  plus the Consent Pro publication and site deployment being tested. A preview cannot prove
  the ordinary visitor path. See [release checks](../06-agent-readiness/operations.md#draft-preview-and-release).
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

**Record the exact names, not private values.** They make the observation useful and help
trace it back to a tag.

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

### Step 4. Partial consent, revocation and persistence

In another fresh session, accept only one optional category, such as Analytics. Exercise the
same named trackers and confirm that the chosen category runs while denied categories follow
their configured rules. Reload and repeat to check the stored choice.

Then reopen preferences through the site's visible control and revoke the optional category.
Confirm the displayed and runtime choices, exercise the same actions again and reload.
Distinguish existing storage from new requests or writes after revocation. An existing
cookie alone does not establish that a tracker ran again. For an attributed image pixel,
verify the `src` is removed after its category is revoked.

Test the preferences control on representative pages, including navigation after a choice.
If the floating button is hidden, a working replacement must exist wherever Consent Pro
runs. See [Preferences Link](https://docs.consentpro.com/web-app/preferences-link) and
[Image Trackers](https://docs.consentpro.com/web-app/image-trackers).

---

## Reading the result

Compare the evidence per tracker:

```
step 1 (untouched)   →  observed requests and storage before choosing
step 2 (refused)     →  observed requests and storage with the recorded refusal
step 3 (accepted)    →  positive control using the same expected tracker action
step 4 (changed)     →  partial choice, revocation and persistence after reload
```

Limit the conclusion to the named trackers, pages, interactions, browser and region tested.
Requests that use no cookies and trackers triggered only by other actions remain outside a
cookie-only check. A cookie storing the consent choice is not itself evidence of tracking.
Equal lists or changes in their size establish neither success nor failure on their own.

---

## What to do with what you find

Use an unexpected request, cookie or storage entry to find its source. These are hypotheses,
not conclusions from the symptom:

| Suspected path | Inspect with the available access | If confirmed |
|---|---|---|
| GTM source without the required consent condition | Read the named tag through supported MCP tools, guide its **Triggers** and **Consent Settings** in GTM, or use `scripts/audit-container.py` only on the customer's chosen local path | Apply the agreed check while preserving the business event, then repeat it after refusal and acceptance |
| Saved Essential category does not match the actual purpose | Match the resource and saved tracker in Consent Pro, through available reads or the selected dashboard | Follow [classification review](categories.md), read back the change and repeat the behavior test |
| Direct image pixel or embed | Inspect its source markup, initiator and actual requests; guide the relevant editor if code access is unavailable | Use the supported [non-GTM treatment](../05-what-gtm-does-not-cover.md) and check its function too |
| A tracker loads before the consent layer | Inspect original served HTML and runtime timing; `scripts/inspect-site.py` is optional when local inspection was chosen | Correct the attributed source/order and retest; a dynamically inserted GTM element alone does not prove duplicate installation |

Do not pick a cause from cookie totals or change consent mode to make a warning disappear.
Preserve the minimum relevant observation and test the suspected path. Use
[troubleshooting](troubleshooting.md) when several causes remain possible.

---

## The debugger does part of this for you

Open **Preview** or use the available MCP preview tool to obtain the signed debugger link.
Keep it private and respect its expiry; do not construct the URL yourself. Record runtime,
resolved region, banner and category state. **Reset Banner** clears stored consent in that
test browser. Source: [Debugger](https://docs.consentpro.com/web-app/debugger).

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
> Partial choice, revocation and reload: [observed outcomes or not tested].
>
> Main site function: [safe action, result, consent state and any step not submitted].
>
> Not verified: [other pages, interactions, regions or tracking sources not exercised].

Fill this structure only with observations you actually made. If the acceptance branch did
not exercise the expected tracker, mark that tracker inconclusive. Do not replace missing
runtime evidence with a configuration score or a count of cookies.

**None of those means "the site is compliant."** Compliance is a legal judgement about a
whole site, and these are only inputs. Report them and let the person who owns the
risk draw the conclusion.
