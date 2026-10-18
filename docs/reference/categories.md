# Mapping a category onto a consent check

Step seven asks which consents a tag requires. Map the reviewed category for this site's
actual use, not an unconfirmed automatic suggestion.

| Category in the app | Consent checks to require | What it means on the page |
|---|---|---|
| **Marketing** | `ad_storage`, `ad_user_data`, `ad_personalization` | held until the visitor accepts marketing, or accepts everything |
| **Analytics** | `analytics_storage` | held until the visitor accepts analytics |
| **Personalization** | `personalization_storage` | held until the visitor accepts personalization |
| **Essential** | none | does not wait for optional consent; the original business trigger still applies |

## Essential is the one that deserves a second look

An Essential classification permits the source to run without optional consent; it does
not replace its business trigger or prove that it actually ran. A mistaken classification
can allow non-essential tracking before a choice even when the saved consent checks match
that category.

Identify the function served and why that specific use is necessary for the service the
visitor requests. Session handling or security may be relevant, but a vendor name or a
broken widget is not enough to classify every associated tracker as Essential. Separate
the component's required function from its measurement or advertising behavior and have
the responsible owner resolve uncertain purposes.

Automatic suggestions are review inputs. Do not assume a suggestion was verified against
this site's actual use, or assign Essential just to unblock a page.

## Unknown or inconsistent classification

Use this procedure for the sources relevant to the current installation or observed fault.
Do not require a complete historical inventory before checking the first banner.

1. Match the saved item to its script, resource and page action. Similar names can have
   different purposes; a shared provider does not establish identical use.
2. Separate observed or documented facts from suggestions: purpose, provider, category and
   retention. A code-defined lifetime, observed expiry and saved description may differ.
3. Show the specific conflict to the appropriate site or policy owner. Propose only values
   supported by evidence; leave unknown fields explicitly unresolved.
4. Record the agreed treatment and who resolves what remains. An unknown active source is
   not cleared by calling it Essential. A known leak must be corrected, held out of the
   agreed release with authorization, or reported as an unresolved blocker.
5. Read back the authorized change and repeat the relevant
   [behavior and site-function checks](verify-behaviour.md). Group related items for review
   when useful, but verify each affected source before applying a shared classification.

Unrelated historical cleanup can follow activation. Missing evidence about an active
integration stays visible in the handoff and cannot become a claim that blocking was tested.

## One tracker can need two checks

A source that combines reviewed analytics and advertising purposes can need both checks,
not the category that fits best. Compare the saved tracker list with the source's actual
use and browser observations rather than guessing from the vendor's name. A saved entry
alone does not establish what the current browser session wrote.

## Third-party widgets are rarely one tracker

A scheduler, a chat widget or a form embed usually loads several trackers, and marking the main
script does not release the rest. Find every tracker whose resource points at that vendor's
domains and handle them as a group.

⚠️ **And be careful with the reflex to mark a whole widget essential so it always shows.**
Rendering a component and tracking who used it are separate things, and the category field
treats them as one. If a widget must be visible before consent, that is worth a conversation
with whoever owns the legal position, not a checkbox.

## Google tags and built-in checks

Google's own tags carry built-in consent checks. **Basic GA4** uses `Consent Updated` and
requires the additional `analytics_storage` consent. **Advanced GA4** uses Consent
Initialization and does not add that requirement, allowing cookieless requests while storage
is denied. Preserve built-in checks in both cases. Agree the mode before editing. See
[the mode contract](consent-mode.md) and the
[official guide](https://docs.consentpro.com/web-app/google-consent-mode).
