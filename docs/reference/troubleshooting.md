# When it does not behave

Six known shapes. Each has a distinct symptom, so start from what the person is seeing rather
than from a theory.

---

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

**The scan is old.** The categories mapped in step seven describe trackers the site no longer
has, or miss ones it gained. Re-scan before mapping, and re-scan after adding anything to the
container.

**The container reports no recent data.** This is ambiguous and worth not guessing about. It
can mean the consent layer is holding the tags, which is correct behaviour, or that the tags
are not firing for an unrelated reason. **Separating the two requires accepting the banner and
watching the container afterwards**, which is checks 6.4 and 6.5 in [`verify.md`](verify.md).
An explanation that credits the result to the product working correctly is the one to be most
sceptical about, because it is the most comfortable and needs the same evidence as any other.
