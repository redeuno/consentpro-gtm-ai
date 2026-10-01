# When it does not behave

Six known shapes. Each has a distinct symptom, so start from what the person is seeing rather
than from a theory.

---

## The scan finds fewer trackers than the site actually loads

**The most reported one, and it is documented behaviour rather than a bug.**

**Cause:** the tag is on a trigger the scanner does not read. The documentation is explicit
that it only detects tags firing on `All Pages` or on a Consent Pro event such as
`consent-updated`. A tag on a click, a timer, a scroll, one specific page or your own custom
event is invisible to it.

**What that produces:** the tracker never appears in the app, never gets a category, and
therefore never gets a consent check. It fires, and nothing in the product says it exists.

**How to confirm it in seconds:**

```bash
python scripts/audit-container.py --account ID --container GTM-XXX --confirm-name "Name"
```

It lists every tag with its trigger and prints an explicit block naming the ones the scanner
cannot see.

**Fix:** move them to `Consent Updated`, which both detects and gates them. Or to `All Pages`
if you only need them detected and they are handled some other way.

⚠️ **Check this before reporting a scanning bug.** A tracker on an unusual trigger looks
exactly like a broken scan from the outside, and the two need completely different responses.

## Trackers appear in the app, and fire regardless of the choice

**The most common one by far.** Detection is working and blocking was never set up.

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

**Cause:** the container was configured but never published.

**Fix:** step eight. Then re-check, because the earlier checks were reading a container that
was not live.

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

## Two more that are not in the six

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
