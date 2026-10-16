# 5. What the tag manager does not cover

Container configuration covers one delivery path. Inspect the site's other sources and
finish with browser checks before reporting installation complete.

A site can receive trackers through several paths, and the container is only one of them.
The [operations guide](06-agent-readiness/operations.md) covers installation and diagnosis.

## A site without GTM

GTM is optional. If the customer has not chosen to adopt it, work with the site's
current integrations instead of introducing a container. Identify scripts inserted
by the site builder, plugins, shared code, embeds and image pixels. Read the exact
Consent Pro project snippet and inspect core order before changing any integration.

For each relevant source, record its purpose/category, how it loads, which business
action starts it and who can edit it. Guide the site owner through their actual
editor when the assistant has no code access. State the exact field or markup,
current and proposed value, deployment action and check needed to resume. The
customer does not need a terminal or an API connection for this guidance.

If another CMP is installed, use the
[transition procedure](06-agent-readiness/operations.md#existing-cmp-and-tracking-transition)
before adding or removing a runtime. Preserve working purchase, lead and form
integrations; moving a tag into GTM is a separate change, not a prerequisite for
consent. The [browser checks](reference/verify-behaviour.md) still apply without GTM.

| How it arrives | Covered by the wiring? | What handles it |
|---|---|---|
| A tag inside the container | **yes**, once wired | this repository |
| A script written straight into the page | separate runtime path | verify category, load order and observed blocking |
| **An image request** | **no** | a manual attribute change. Below |
| An embed or plugin integration | separate integration path | inspect its loading contract, purpose and actual requests before choosing a supported gate |

Do not generalize browser results to server-side events or integrations that were
not inspected. Record those dependencies and the responsible administrator.

---

## Image trackers, and why they are different

A tracking pixel is an `<img>` pointing at a third party. A browser fetches it as soon as it
parses the tag, and **there is no execution step to intercept**. A script can be held because
something has to run it. An image just loads.

So Consent Pro cannot block one on its own. **The source has to leave the HTML**, and the
product puts it back when the visitor accepts the matching category:

```html
<!-- Existing immediate request -->
<img src="https://example.com/pixel.gif?id=123" width="1" height="1" alt="">

<!-- Request held until the matching consent -->
<img fs-consent-src="https://example.com/pixel.gif?id=123"
     fs-consent-categories="marketing" width="1" height="1" alt="">
```

The exact attribute names and the available categories are in the official page:
[docs.consentpro.com/web-app/image-trackers](https://docs.consentpro.com/web-app/image-trackers).
In **Consent manager**, open a tracker with the **from Image** badge to find its attributed
URL and generated snippet. Multiple comma-separated categories require all listed choices.
Verify no live `src` before consent, release after acceptance, and removal after revocation.
Images setting only reviewed Essential cookies can keep `src`; still disclose them in the
manager. Source: [runtime image reference](https://docs.consentpro.com/runtime/image-trackers).

An image response can introduce more storage than its name suggests. Reconcile
observed requests and storage with the actual resource and saved tracker details;
do not infer its category from the provider name or a scan label alone.

---

## Two more edges worth knowing

**The `<noscript>` half of the container snippet.** It loads tags for visitors without
JavaScript, which means outside the consent layer entirely. Removing it is step one of the
wiring, and it is the step people skip because it looks like housekeeping.

**Tags the scanner cannot see.** The Consent Pro scanner reads cookies that appear on the page.
It does not open your container and read the tags inside, and the app says so in the Configure
GTM panel. A tag that sets nothing on a normal page load, or fires only after a click, will not
appear in a scan and therefore will not appear in your category map either. **Check the
container's own tag list against the map** rather than assuming the scan found everything.

---

## The honest summary to give someone

Keep a working [preferences control](https://docs.consentpro.com/web-app/preferences-link)
on every page, including when the floating control is hidden. Test partial consent,
revocation and reload as well as first-time acceptance and refusal.

After [testing browser behaviour](reference/verify-behaviour.md), report the scope observed:

> For [named trackers], we exercised [pages and actions] in [browser, region and consent
> mode]. We observed [requests and storage] before choice, after refusal and after acceptance.
> The observed result was [result for each tracker].

Do not turn that scoped observation into:

> Every tracker on the site is held.

Image pixels, the `<noscript>` block, trackers the scan missed and untested interactions can
all lie outside that observation. Record those limits. A cookie count cannot prove that
requests or other storage were blocked, and absence after acceptance makes the result
inconclusive when the expected tracker was never exercised.
