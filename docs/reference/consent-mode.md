# Basic and Advanced Google Consent Mode

Choose the mode explicitly before configuring Google tags. Basic is the documented default;
Advanced sends cookieless Google requests when storage consent is denied and requires a
separate customer decision. It is not a fix to enable just because analytics traffic falls.
Source: [Consent Pro mode guide](https://docs.consentpro.com/web-app/google-consent-mode).

| Setting | Basic GA4 | Advanced GA4 |
|---|---|---|
| Base Google tag trigger | `Consent Updated` | `Consent Initialization - All Pages` |
| Built-in consent checks | Preserve | Preserve |
| Additional `analytics_storage` requirement | Required | Do not add |
| Before analytics acceptance in an opt-in region | No GA4 collection requests | Cookieless requests can occur; analytics storage remains denied |
| Init priority | Consent defaults must precede collection | Consent Pro Init `1`, Google tag `0`, per the product guide |

Both modes keep denied defaults for opt-in regions. Marketing/third-party tags still require
their category's consent. A purchase or form event must retain its business condition;
do not turn all conversion tags into page-load or consent-change tags.

The local writer supports Basic consent gating, not a full Advanced Google-tag migration.
Preserve an Advanced tag with an explicit `skip` map entry only after reviewing its existing
mode, trigger and built-in checks. Configure Advanced deliberately in the GTM interface until
a supported writer contract covers it. Do not label a skipped tag as verified.

For verification, record mode and region, inspect actual consent state plus requests and
storage, and exercise a positive control after acceptance. Do not use one request parameter
or total cookie count as the sole verdict. Follow [the browser procedure](verify-behaviour.md).
Use the [category mapping](categories.md) and [nine steps](nine-steps.md) for the other tags.
