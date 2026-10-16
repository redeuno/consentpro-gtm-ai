# When it does not behave

Start from the observed symptom. Check both product and container state; the
[operations guide](../06-agent-readiness/operations.md#runtime-diagnosis) covers core,
licence, publication, CSP and scanner access alongside GTM configuration.

## Account access and project selection

Start from the layer that failed. Use the official
[Finsweet Account entry](https://finsweet.com/products/account) for **Log in** or
**Create Account**. The account page describes password, Google and passwordless
entry. The customer completes authentication and any recovery offered by the
current sign-in interface. Do not construct a reset URL or ask for a password,
one-time code, callback link or token. A failed automated fetch of the login page
does not prove the customer cannot open it in their browser.

| Symptom | Check and next step |
|---|---|
| Sign-in loops or no session appears | Confirm the official destination and intended login method; inspect the displayed error and retry only the failed session step. Use official recovery or support if it persists |
| Dashboard works, assistant tools do not | Keep the working dashboard session; inspect the host connector and its grants or continue entirely manually. Do not recreate the account |
| Expected workspace/project is absent | Confirm account, selected workspace, membership, filters and complete pagination. Have its administrator resolve access before creating a replacement |
| Paid plan or license is absent | Use [entitlement diagnosis](../06-agent-readiness/operations.md#a-purchased-plan-or-domain-licence-is-missing); compare purchase owner and domain assignment before discussing another purchase |
| The first project does not exist | Confirm domain, platform and authorization, then use [first-project setup](../06-agent-readiness/operations.md#account-workspace-and-first-project) |
| Google authorization is declined | Continue with [manual GTM setup](nine-steps.md); do not require a different OAuth flow or terminal |
| Google connected, container still missing | Check the selected Google account, complete inventory and container role. Access is personal; the customer's CP workspace does not automatically grant Google access |
| The instructed control is not on the screen | Inspect the current platform, language, selected object and role. Use the actual supported control; do not repeat an unavailable click |

When the customer returns after a failed step, use the
[resume card](onboarding.md#start-and-resume). Refresh affected state rather than
starting another scan, reconnecting everything or recreating the project.

## Support and assisted setup

Offer the option appropriate to the customer's need without requiring them to
exhaust a long manual procedure first. The public destinations below were checked
on 2026-10-16; confirm their current scope and any eligibility before promising help:

| Need | Official route | Boundary |
|---|---|---|
| Product question or troubleshooting | [Finsweet Forum](https://forum.finsweet.com/), linked from [Consent Pro troubleshooting](https://docs.consentpro.com/web-app/troubleshooting) | Check current access/posting controls; never post account or visitor records publicly |
| Human guidance while exploring or setting up | [Talk to an expert](https://consentpro.com/talk-to-expert) | Use its current contact flow; verify the service offered instead of promising a response time or a completed implementation |
| Customer wants someone to implement | [Implement for us](https://consentpro.com/implement-for-us) | A separate assistance option; confirm scope, terms and eligibility. A product purchase alone is not proof that implementation is included |

Escalate a persistent account/license discrepancy, permissions only an owner can
grant, an unsupported operation, an unreconciled write outcome, or a reproducible
runtime problem outside available access. Name the unresolved dependency and keep
independent work moving. Repeated clicks, scans or reconnections are not a remedy
without new evidence. Do not promise a refund, free work, legal advice or a deadline.

Prepare this short handoff for the customer to review:

```text
Help requested: [question, account correction, access or implementation]
Site and environment: [only what the recipient needs]
Current state: [reported/inspected/tested; saved and published separately]
Problem: [expected result, observed result, relevant error without secrets]
Already tried: [steps, result, date]
Needed next: [specific action and appropriate owner]
```

Exclude passwords, tokens, signed previews, callback URLs, consent identifiers,
individual visitor records, complete payment details and unrelated client data.
Use a private official channel for account-specific evidence requested by support;
do not attach it to a public forum post. The customer decides what to share.

Preparing this handoff does not open a ticket. Send, submit or book only when the
customer explicitly instructs that action and the destination/content are clear.
Report separately: prepared, submitted with acknowledgement, and response received.
After support or an administrator acts, re-read the affected state and resume the
next authorized step. Their message alone is not proof of the resulting setup.

---

## The scan finds fewer trackers than the site actually loads

Several documented coverage limits can produce this symptom.

**Possible causes:** the scan did not exercise a tag's event, did not reach its page, or was
blocked by authentication, `robots.txt` or bot protection. Check scan status and coverage
before assuming a trigger problem. The GTM guide describes detection on `All Pages` and
Consent Pro events; other interactions may not be exercised.

**What that can produce:** a tracker absent from the scan and an incomplete category map.
Absence from the scan is not evidence that the tracker cannot fire.

**How to check:** inspect the relevant tags and triggers in the selected GTM
workspace, use available MCP reads within their published/workspace scope, or
use this command only when the customer already chose local automation:

```bash
python scripts/audit-container.py --account ID --container GTM-XXX --confirm-name "Name"
```

Compare the container inventory and triggers against scan results and expected page actions.

**Fix:** preserve business triggers such as purchase or form submission and add the correct
consent checks. Exercise the original event in a browser. Only page-load tracking uses the
replacement pattern in [step 6](nine-steps.md#6-preserve-business-events-and-gate-the-tags).
Do not move a conversion onto All Pages or consent-updated just to make a scan see it.

**Check this before reporting a scanning bug.** A tracker on an unusual trigger looks
exactly like a broken scan from the outside, and the two need completely different responses.

## Trackers appear in the app, and fire regardless of the choice

Detection can work while consent gating is missing.

**Cause:** tags left on `All Pages`, with no consent check. The scanner detects tags on All
Pages by design, so everything looks handled.

**Fix:** steps five, six and seven.

---

## Everything saves and publishes, and the defaults never apply

**Cause:** the region is written as a label, a country name, or `EU`.

**Fix:** [`regions.md`](regions.md). Compare the tag's region row against the banner's
geotarget code by code.

**Why it is hard to spot:** there is no error. The tag accepts the value, the container
compiles, and the region simply never matches a visitor.

---

## Sometimes held, sometimes not

**Cause:** the initialization tag is on `All Pages` instead of `Consent Initialization - All
Pages`. Load order decides the outcome, so the behaviour changes between page loads.

**Fix:** change the trigger on that one tag.

---

## Everything looks right in the interface, the live site is unchanged

**Possible causes:** the GTM workspace is unpublished, Consent Pro has saved changes that
were not published, site code was not deployed, or published configuration remains cached.
An unlicensed domain or saved visitor choice can also hide the banner.

**Check:** identify the intended site deployment, CP publication and GTM live version, then
compare the ordinary domain in a fresh session. Do not publish without the corresponding
authority. See [release checks](../06-agent-readiness/operations.md#draft-preview-and-release).

---

## A tracker fires on refusal, and the configuration looks correct

**Cause:** it is categorised as essential, and essential skips consent. The configuration is
correct **for an essential tracker**; the categorisation is what is wrong.

**Fix:** re-read the essential list, recategorise in the app, and update that tag's consent
checks. See [`categories.md`](categories.md).

---

## Tags fire for some visitors with no banner interaction at all

**Cause:** the `<noscript>` was left in place, so tags load without JavaScript and outside the
consent layer.

**Fix:** step one.

---

## Local Gallery compatibility cases

### Gallery import stops with "Consent Pro INFO identity does not match"

The live Gallery response captured on 2026-10-01 changed `INFO.brand.id` from the public
file's `finsweet_consent_pro` to `github.com_finsweet`. The earlier validator stopped after
importing the template and before configuring tags. The corrected helper accepts the Gallery
shape only with its verified host, owner, repository, pinned version and content hash.

Use the corrected package, audit the workspace and review the simulation before resuming.
A recognised imported template is reused. Do not delete it or bypass identity checks to
retry. The same error can also identify an unexpected template; the
[captured-response tests](../../tests/README.md) define the case that was reproduced.

### Creating the initialization tag fails with "Unknown entity type"

The Gallery template uses the public type `cvt_WRGND`. Constructing it from the container ID
and the workspace template ID, as manual imports require, caused this API rejection in the
same live test. Use the corrected writer and auditor, which share the verified type by
template origin. Audit the existing workspace and review a new simulation before resuming.
The failed tag creation did not create an initialization tag or container version.

### Other causes

**Core/API blocked by CSP.** Inspect console and response headers. Both `script-src` and
`connect-src` may need the Consent Pro API origin. Merge into the existing policy and
respect nonces/hashes rather than replacing it.

**Scan blocked by a firewall.** Inspect the actual challenge and `robots.txt`. The scanner
identifies itself with the `ConsentProScanner` token, but header matches are not proof of
identity. Do not allow all shared Cloudflare IPs or disable protection automatically.
Sources: [Troubleshooting](https://docs.consentpro.com/web-app/troubleshooting),
[Scanner](https://docs.consentpro.com/scanner).

**Regional preview works but ordinary visits differ.** Compare plan eligibility and saved
versus published region mappings. Basic applies Global instances, while a preview can show
regional instances that production does not run. See [Licenses](https://docs.consentpro.com/web-app/licenses).

**GA4 waits for analytics consent.** Expected in Basic mode. Advanced intentionally behaves
differently; do not remove the additional consent check without a mode decision. See
[Basic and Advanced](consent-mode.md).

**The scan is old.** The categories mapped in step seven may describe trackers the
site no longer has, or miss ones it gained. Compare the current inventory, scan
time and coverage. Start an authorized relevant scan when needed; do not repeat
one merely to observe a draft setting or treat a scan as a substitute for event tests.

**The container reports no recent data.** This is ambiguous and worth not guessing about. It
can mean the consent layer is holding the tags, which is correct behaviour, or that the tags
are not firing for an unrelated reason. **Separating the two requires accepting the banner and
exercising a named tracker's expected action afterwards**, which is checks 6.4 and 6.5 in
[`verify.md`](verify.md). Observe its requests and storage, not just the cookie total. If the
tracker remains absent after acceptance, its earlier absence cannot yet be credited to
consent blocking.
An explanation that credits the result to the product working correctly is the one to be most
sceptical about, because it is the most comfortable and needs the same evidence as any other.
