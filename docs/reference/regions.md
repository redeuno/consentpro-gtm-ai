# Regions: where most setups quietly go wrong

The region field decides who the defaults apply to. **Get it wrong and the tag still saves, the
container still publishes, and nothing warns you.** The defaults simply never reach most
visitors.

This page exists because the instruction that prevents the error lives in only one of the two
documentation trails. A setup built from the Webflow page alone can miss it entirely.

## How to write each case

| Banner | Type exactly | Not this |
|---|---|---|
| The default banner | `Global` | `Global (default)`, which is the label the app shows |
| A country | `GB`, `FR`, `BR` (two letters, ISO 3166-1) | the country name |
| A US state or other subdivision | `US-CA` (ISO 3166-2) | `California`, or `CA` alone |
| The app's **EU** option | every member country, plus `GB`, comma separated | `EU`. It is a grouping shortcut in the app interface, and the tag manager does not know it |
| Several regions, one banner | `US-CA,GB,FR` (comma separated, no spaces) | one row per region, unless they are genuinely separate banners |

## Where to find the right value

**Web app:** Consent banner, then Banners, then open the banner's **Geotarget** control.

**Webflow:** the **Banners** screen has a copy button on the **Regions** column.

Then translate what you see into codes using the table above. **The app's display value and the
tag manager's expected value are not always the same string**, and that gap is the failure.

## The check that catches it

First check the plan and published banner configuration. Basic supports Global instances;
Premium supports region-specific instances. A draft preview can show regional banners even
when the production plan does not run them, so preview is not proof of live eligibility.
Source: [Licenses](https://docs.consentpro.com/web-app/licenses).

Open the initialization tag, open the region table, and compare it against the banner's
geotarget **code by code**. Not "looks right", code by code.

If the banner is the default one and the region row says a country, the compliance posture has
been narrowed to that country. Visitors from everywhere else fall through to whatever the
template does with no matching region.

## Multiple banners

Preserve existing rows and unrelated initialization parameters. Do not replace the whole
table to change one region. Review the complete existing table, apply only the
agreed rows through a supported MCP operation or the GTM interface, then read it back.

Use one region row per banner, with its own codes and pattern. This example has
opt-in for the EU countries plus the UK and opt-out for California.
Both regional rows belong to one initialization tag:

| Row | Regions | Fields |
|---|---|---|
| 1 | the EU countries plus `GB` | all Denied |
| 2 | `US-CA` | all Granted |

These example rows preserve the existing `Global` fallback and any other agreed regions.
`US-CA` covers California only, not the whole United States.

## A note on what this controls

These defaults are the state **before** the visitor chooses, per region. They are not the
banner's behaviour and they do not replace it. If the defaults say granted and the banner is
opt-in, the two disagree and the defaults win until the visitor acts, which is the shape of a
tracker firing before consent on a site that looks correctly configured.
