# Basic and Advanced Google Consent Mode

Choose explicitly when configuring Google measurement. If no Google measurement is
being installed or changed, defer this choice until it affects the work.

## Explain the choice before asking

Lead with what visitors experience, not the technical mode names. Translate this
comparison into the customer's language before using the host's question tool:

| Choice | Before acceptance, or after rejection | After acceptance |
|---|---|---|
| Wait for acceptance (Basic) | The configured Google measurement tags send no measurement data until the relevant consent is granted. | Measurement can run for the categories the visitor accepted. |
| Send limited measurements (Advanced) | Supported Google tags can send limited information to Google without measurement cookies while consent is denied. | Measurement can use the cookies and data allowed by the accepted categories. |

Advanced still sends data to Google. Do not describe it as anonymous, zero data
or no tracking. These choices concern the configured Google measurement tags;
other scripts and pixels need their own consent rules.
Source: [Google's mode comparison](https://developers.google.com/tag-platform/security/concepts/consent-mode#basic_versus_advanced_consent_mode).

Ask one question: "When should Google measurement start on this site?"
Use the two short choice labels above, with their consequences as descriptions.
The terms Basic and Advanced identify behavior, not the customer's experience
level or their Consent Pro subscription.

Recommend waiting for acceptance when the stated goal is no Google measurement
before consent, including a first test with that goal. Explain that it leaves
non-consenting visits out of those tags' measurement. Present Advanced when the
customer wants to consider limited measurements before acceptance; do not imply
that it guarantees better reports or is required to install the banner.

If the customer asks for an explanation, explain and keep the decision pending.
Reuse an explicit choice already given. A recommendation, preselected option or
silence does not select a mode or authorize publication.

## Configure the selected behavior

Basic is the product's documented default, not permission to choose for the customer.
Advanced requires a separate decision; do not enable it merely because analytics
traffic falls. Source: [Consent Pro mode guide](https://docs.consentpro.com/web-app/google-consent-mode).

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
