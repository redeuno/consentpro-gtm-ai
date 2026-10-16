# When it does not behave

Start from the observed symptom. Check both product and container state; the
[operations guide](../06-agent-readiness/operations.md#runtime-diagnosis) covers core,
licence, publication, CSP and scanner access alongside GTM configuration.

---

## The scan finds fewer trackers than the site actually loads

Several documented coverage limits can produce this symptom.

**Possible causes:** the scan did not exercise a tag's event, did not reach its page, or was
blocked by authentication, `robots.txt` or bot protection. Check scan status and coverage
before assuming a trigger problem. The GTM guide describes detection on `All Pages` and
Consent Pro events; other interactions may not be exercised.

**What that can produce:** a tracker absent from the scan and an incomplete category map.
Absence from the scan is not evidence that the tracker cannot fire.

**How to confirm it in seconds:**

```bash
python scripts/audit-container.py --account ID --container GTM-XXX --confirm-name "Name"
```

Compare the container inventory and triggers against scan results and expected page actions.

**Fix:** preserve business triggers such as purchase or form submission and add the correct
consent checks. Exercise the original event in a browser. Only page-load tracking uses the
replacement pattern in [step 6](nine-steps.md#6-preserve-business-events-and-gate-the-tags).
Do not move a conversion onto All Pages or consent-updated just to make a scan see it.

⚠️ **Check this before reporting a scanning bug.** A tracker on an unusual trigger looks
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

**The scan is old.** The categories mapped in step seven describe trackers the site no longer
has, or miss ones it gained. Re-scan before mapping, and re-scan after adding anything to the
container.

**The container reports no recent data.** This is ambiguous and worth not guessing about. It
can mean the consent layer is holding the tags, which is correct behaviour, or that the tags
are not firing for an unrelated reason. **Separating the two requires accepting the banner and
exercising a named tracker's expected action afterwards**, which is checks 6.4 and 6.5 in
[`verify.md`](verify.md). Observe its requests and storage, not just the cookie total. If the
tracker remains absent after acceptance, its earlier absence cannot yet be credited to
consent blocking.
An explanation that credits the result to the product working correctly is the one to be most
sceptical about, because it is the most comfortable and needs the same evidence as any other.
