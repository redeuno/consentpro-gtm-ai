# 5. What the tag manager does not cover

Finishing the wiring feels like finishing the job. It is not, and the gap is easy to miss
because nothing on any screen mentions it.

**Everything in this repository is about trackers that arrive through Google Tag Manager.** A
site usually has three ways trackers get in, and the container is only one of them.

| How it arrives | Covered by the wiring? | What handles it |
|---|---|---|
| A tag inside the container | **yes**, once wired | this repository |
| A script written straight into the page | **yes**, the consent layer intercepts it | Consent Pro, automatically |
| **An image request** | **no** | a manual attribute change. Below |

---

## Image trackers, and why they are different

A tracking pixel is an `<img>` pointing at a third party. A browser fetches it as soon as it
parses the tag, and **there is no execution step to intercept**. A script can be held because
something has to run it. An image just loads.

So Consent Pro cannot block one on its own. **The source has to leave the HTML**, and the
product puts it back when the visitor accepts the matching category:

```html
<!-- before: fires immediately, whatever the visitor chose -->
<img src="https://example.com/pixel.gif?id=123" width="1" height="1" alt="">

<!-- after: held until consent, then restored -->
<img fs-consent-src="https://example.com/pixel.gif?id=123"
     fs-consent-category="marketing" width="1" height="1" alt="">
```

The exact attribute names and the available categories are in the official page:
[docs.consentpro.com/web-app/image-trackers](https://docs.consentpro.com/web-app/image-trackers).
The app's **Block tracking images** panel also lists the pixel URLs it found on your site,
which is the fastest way to know whether you have any.

> **A pixel carries more than the tracker you meant to add.** One measured case: a LinkedIn
> pixel planted for a test also set a Cloudflare bot management cookie, which then appeared in
> the scan as an essential tracker from an image source. The cookie nobody planted is the one
> that shows up in the audit.

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

After the wiring is done and verified, what you can say is:

> Trackers arriving through the tag manager are held until the visitor chooses, and that has
> been verified by loading the site and refusing.

What you cannot say without checking these three:

> Every tracker on the site is held.

The difference is image pixels, the `<noscript>` block, and anything the scan did not see.
Three checks, a few minutes, and the second sentence becomes true or you find out why it is
not.
