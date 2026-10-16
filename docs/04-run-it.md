# 4. Hand it to the agent

This is the **local GTM script path**, selected explicitly when the customer wants local API
automation. For connected MCP diagnosis and supported CP changes, start with the
[journey](00-the-journey.md) and [operations guide](06-agent-readiness/operations.md).
The captured MCP cannot write GTM; do not silently switch to local Google credentials.
For this script path, complete the
[OAuth setup](01-google-cloud-setup.md) and [authorisation](03-authorise.md), then establish
the target, mode and settings and review the category map. For GTM interface setup, use the
[nine steps](reference/nine-steps.md); that path needs no custom OAuth client.

The writer supports web containers only. It requires explicit container capability
metadata before writing and reads every supported collection carried by a version,
including variables and built-in variables. Missing capability metadata requires
inspection in GTM; it is not treated as an empty collection. The final version and
container settings must match the approved state before publication.

Creating a version removes the source workspace according to the Google API
contract and may return `newWorkspacePath`. Before a later run, list workspaces
again and confirm the current target; do not reuse an old workspace ID blindly.
Source: [create version](https://developers.google.com/tag-platform/tag-manager/api/reference/rest/v2/accounts.containers.workspaces/create_version).

Only the built-in All Pages trigger can be replaced automatically with the consent
event. A custom pageview, DOM-ready or window-loaded trigger can carry conditions
that must remain true after consent. The writer refuses these and unsupported trigger
types before writing. Review their conditional consent design manually, or use
`skip` only after reviewing the existing setup. Purchase, click and supported business
events retain their original conditions and receive the mapped consent checks.

> **Which documentation trail applies to you.** The nine steps are identical either way; the
> details differ, and the region section differs the most.
>
> | Your site | Trail |
> |---|---|
> | Installed Webflow engine | [the Webflow guide](https://docs.consentpro.com/webflow/google-tag-manager) |
> | Installed custom-site core | [the web app guide](https://docs.consentpro.com/web-app/google-tag-manager) |
>
> ⚠️ **A Webflow project managed from the web app follows the web app trail**, and that case is
> real rather than hypothetical. **The script address tells you which**, with no guessing:
> `/v2/cdn/runtime.js` is the Webflow engine, `/cdn/core/` is the web app. Look at your own
> page source, or ask the agent to.

## Decisions and target to establish

| Value | Where you find it | Why it has to come from you |
|---|---|---|
| **Account ID and container ID** | step 2 | the credential reaches many containers, and choosing one for you is exactly the mistake that publishes to the wrong site |
| **Banner type**<br>opt-in, opt-out, do-not-sell or informational | Consent banner, in the Consent Pro app | it decides whether every regional default is denied or granted, which is the difference between blocking and not blocking |
| **Regions** | Consent banner, Banners, the Geotarget control | the app's display value and the tag manager's expected code are different strings. [reference/regions.md](reference/regions.md) |
| **Which trackers are genuinely essential** | your judgement about your site | it is a legal and product decision, and the one field where a wrong automatic answer causes harm no check catches |
| **Consent mode** | agreed analytics policy | Basic blocks GA4 collection until consent; Advanced permits cookieless requests before consent and is not configured automatically by this writer |

Read banner and region values from the connected project when possible, then confirm the
intended target and change. Local scripts support Basic gating. See
[Basic and Advanced](reference/consent-mode.md) before mapping Google tags.

## A prompt that works

```
Wire my Google Tag Manager container to Consent Pro. Read skill/SKILL.md in this
repository first, including the Gallery installation and existing-template rules.

  account:    1234567890
  container:  GTM-XXXXXXX
  banner:     opt-in
  regions:    Global
  mode:       Basic

Audit the container first and show me what is already set. Then scaffold the
category map and go through it with me line by line before applying anything.
Preserve purchase/form events, existing region rows and unrelated settings.
Publish only when I say so.
```

**Why each line is there:**

- **Naming the target** stops the agent choosing a container, which is the failure that reaches
  a live site.
- **Audit first** means you find out the setup is already half done before something overwrites
  it.
- **The map line by line** is the one place your judgement is required, and an agent left alone
  will fill it plausibly and wrongly.
- **Publish only when I say so** separates configuring from shipping. A reviewed plan hash
  is required to write, and publication must be included in that plan.

## The sequence, if you are driving it yourself

```bash
# 1. what is there now
python scripts/audit-container.py --account 123 --container GTM-XXX
#    it prints the account name and tells you what to pass back
python scripts/audit-container.py --account 123 --container GTM-XXX \
    --confirm-name "Your Account Name"

# 2. build the category map
python scripts/wire-consent.py --account 123 --container GTM-XXX \
    --confirm-name "Your Account Name" --scaffold > map.json

# 3. READ map.json AND FIX IT. see below.

# 4. simulate. nothing is written
python scripts/wire-consent.py --account 123 --container GTM-XXX \
    --confirm-name "Your Account Name" \
    --banner opt-in --regions Global --map map.json

# 5. apply the reviewed PLAN_SHA256, still unpublished
python scripts/wire-consent.py --account 123 --container GTM-XXX \
    --confirm-name "Your Account Name" \
    --banner opt-in --regions Global --map map.json \
    --apply --approve-plan REVIEWED_HASH

# 6. simulate a new plan that includes publication
python scripts/wire-consent.py --account 123 --container GTM-XXX \
    --confirm-name "Your Account Name" \
    --banner opt-in --regions Global --map map.json --publish

# 7. after publication approval, apply that new plan
python scripts/wire-consent.py --account 123 --container GTM-XXX \
    --confirm-name "Your Account Name" \
    --banner opt-in --regions Global --map map.json \
    --publish --apply --approve-plan REVIEWED_PUBLICATION_HASH

# 8. read back configuration; browser verification follows separately
python scripts/audit-container.py --account 123 --container GTM-XXX \
    --confirm-name "Your Account Name"
```

Replace each hash placeholder with the `PLAN_SHA256` from the reviewed simulation. The hash
includes target, options, current state, existing workspace changes and publication intent.
A changed state invalidates it; simulate again and review the new plan rather than bypassing
the check. A first application changes state, so its old hash cannot approve later publication.
`--publish` without `--apply` only simulates a publication plan.

If more than one workspace exists, select the intended ID with `--workspace ID` and keep it
in every simulation/application command. The script refuses to choose one for you. The
banner CLI accepts `opt-in` or `opt-out`; other product banner types still need their actual
defaults reviewed, and a multi-banner change belongs in a separate plan.

## Step 3 is the one that matters

`--scaffold` prints a category-map entry per tag, initially `marketing`. This is a review
placeholder, not a classification. Review every entry before applying. The map must cover
every relevant current tag, with `skip` explicit for anything intentionally untouched;
duplicate or stale tag names must be resolved rather than guessed.

```json
{
  "GA4 Configuration": "analytics",
  "Meta Pixel": "marketing",
  "Session cookie helper": "essential",
  "Old test tag": "skip"
}
```

| Value | Effect |
|---|---|
| `marketing` | requires the three advertising consents |
| `analytics` | requires analytics consent |
| `personalization` | requires personalization consent |
| `essential` | no additional consent check; retain the original firing trigger |
| `skip` | the script leaves that tag completely alone |

**Read every `essential` line out loud.** Ask one question of each: does the site stop working
without this tracker? Session handling, security and fraud prevention usually qualify. Anything
that measures, attributes or personalises does not, however convenient it would be.

## What the agent does with all that

The container operations are detailed in [reference/nine-steps.md](reference/nine-steps.md).
For a new template, the script imports from the Gallery with owner `finsweet`, repository
`gtm-template-consent-pro` and pinned SHA `8a551897e5bfdecf03de59fa00058be442b7ac29`.
It preserves recognised existing templates, including compatible manual imports, with no
automatic migration. A modified or unrecognised template stops the run before configuration
writes. Review the audit's source and version before approving changes.

With `--apply --approve-plan HASH`, it configures the initialization tag and regional defaults, creates the
`consent-updated` trigger, applies the category map and creates an unpublished version.
Publication additionally requires `--publish` and a matching plan that includes publication.
Review new Gallery template permissions and all existing workspace changes before approving
that plan, since a container version includes the workspace state.

The writer validates that an existing consent trigger has the correct event, preserves
business-event firing conditions and adds category checks. Only page-load/consent-update
tracking uses the consent-updated replacement pattern. Existing regional tables and other
initialization parameters are preserved when `--regions` and `--banner` are omitted.
An explicit change to an existing multi-row region table is refused; plan that separately.
For a new initialization tag, provide the intended banner and regions as in the example.

An Advanced Google tag needs a separate reviewed configuration. Use `skip` only to preserve
an intentionally reviewed tag, never to make an unsupported case look verified.

Updates use fingerprints and readback before version creation/publication, but the API is
not a transaction and there is no automatic rollback. After partial failure, inspect the
workspace and review a new simulation. Do not repeat with an old hash. Existing entities are
reused, but a completed application creates another version. Recovery may require restoring
an earlier GTM version manually; publishing that recovery is another explicit action.

A live import on 2026-10-01 exposed a rewritten INFO brand in Google's response. The template
was imported, then the older identity check stopped before tag configuration or version
creation. The validator now checks the captured Gallery shape with the pinned origin and
content. A second attempt revealed that Gallery tags use a public template type; the writer
and auditor now share that checked type instead of the manual-import formula.
[The regression fixture](../tests/README.md) records both differences. Completed live
configuration and browser behaviour still require readback and checks on the target site.

## Live check on 2026-10-01

An isolated QA container received the pinned Gallery template through the real API. The two
compatibility failures above interrupted setup before an initialization tag or a new version
was created. After the fixes, the same imported template was reused. The first completed
application created version 2 while version 1 remained live. Repeating with the then-current
`--apply --publish` command
published version 3 without duplicating the template, initialization tag or consent trigger.
The existing lab container was read before and after, and its canonical state and live version
were unchanged. This was an audited recovery, not a single uninterrupted installation.

Chrome 154 on Windows tested the QA container with two local markers, one Analytics and one
Marketing, on a Web App test runtime version 2.4.2 using global opt-in defaults. The container
ID was substituted only in the browser's received HTML; the public lab installation was not
changed. Both markers stayed blocked before a choice and after refusal. Acceptance enabled
both, Analytics-only enabled only Analytics, and revocation caused no new marker execution.
Reloads preserved each choice and blocked both markers after revocation.

The synthetic marker cookies were not registered with the CMP and remained after revocation;
their presence does not mean a tag fired again. The check observed new executions and Google
consent state, with five seconds per stage. It does not cover every tracker, other regions or
consent modes, the Webflow runtime, Mac/Safari, a physical mobile device, or importing through
the signed-in GTM interface. Test the actual target site before making a broader claim.

That historical run predates the required plan-hash approval. The current writer's local
tests do not substitute for a new live API or customer-site validation.

## Then verify, and two of the checks are yours

[reference/verify.md](reference/verify.md) separates configuration from browser behaviour.
The audit reports template identity and configuration signals; it cannot prove that a page
respects consent. A person or an agent with browser access must load the site, refuse and
accept, and inspect the resulting behaviour.

⛔ **Do not accept "the setup is compliant" from an agent.** It configured a container and it
can prove what it configured. Compliance is a judgement about a whole site. Ask for two separate
lists, what was configured and what was verified, and draw the conclusion yourself.

## Step nine is on screen

Ticking the tag manager confirmation inside the Consent Pro app. On Webflow it is the
**Actions** tab; on the web app it is **Overview**, **Data Privacy Check**, the **Configure
GTM** row. Do it after the container is published, and know that it records that somebody said
so rather than testing anything.
