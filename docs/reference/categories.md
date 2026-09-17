# Mapping a category onto a consent check

Step seven asks which consents a tag requires. The category the app gave that tracker decides
it.

| Category in the app | Consent checks to require | What it means on the page |
|---|---|---|
| **Marketing** | `ad_storage`, `ad_user_data`, `ad_personalization` | held until the visitor accepts marketing, or accepts everything |
| **Analytics** | `analytics_storage` | held until the visitor accepts analytics |
| **Personalization** | `personalization_storage` | held until the visitor accepts personalization |
| **Essential** | none | **fires without asking** |

## Essential is the one that deserves a second look

It is the only category that means "runs whatever the visitor chose". A tracker marked
essential by mistake becomes a tracker firing without consent, **correctly configured**, which
is the hardest kind of error to notice: nothing is broken, the setting simply says the wrong
thing.

**Before accepting essential on any tracker, ask one question:** does the site stop working
without it? Session handling, security, load balancing and fraud prevention usually qualify.
Anything that measures, attributes or personalises does not, however convenient it would be.

⛔ **Automatic suggestions are a good starting point and a poor final answer here.** Suggestion
engines classify from the origin of a tracker when they do not recognise the cookie itself, and
they are most confident exactly where they have least evidence. Read the essential list by
hand. It is usually short.

## One tracker can need two checks

A script that drops both an analytics cookie and an advertising cookie needs both, not the one
that fits best. The tracker list in the app shows what each one actually set, which is the
place to look rather than guessing from the vendor's name.

## Third-party widgets are rarely one tracker

A scheduler, a chat widget or a form embed usually loads several trackers, and marking the main
script does not release the rest. Find every tracker whose resource points at that vendor's
domains and handle them as a group.

⚠️ **And be careful with the reflex to mark a whole widget essential so it always shows.**
Rendering a component and tracking who used it are separate things, and the category field
treats them as one. If a widget must be visible before consent, that is worth a conversation
with whoever owns the legal position, not a checkbox.

## Google tags and built-in checks

Google's own tags carry built-in consent checks. For GA4 with Basic Consent Mode, leave the
built-in checks alone and do not add `analytics_storage` to the additional checks, because that
blocks the tag entirely instead of adjusting how it sends. With Advanced Consent Mode the
configuration differs, and the Basic versus Advanced page covers it.
