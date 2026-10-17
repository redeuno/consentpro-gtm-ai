# Client agent readiness

Updated: 2026-10-16. This page records the investigation and implementation scope.
The source baseline was commit
[`d33d2e0`](https://github.com/redeuno/consentpro-gtm-ai/tree/d33d2e06bfa07b5dd2fda4d8d9e3ad7962b8899b).
Current checks and remaining release gates are recorded below and in
[tests](../../tests/README.md). This document does not authorize customer changes.

## 1. Current state

The repository now provides a primary Consent Pro workflow and a specialized GTM
skill, shared operating references, local GTM tools and a self-contained package
builder for Codex and Claude Code. A connected web chat can use the supported MCP
operations without local Google credentials. Hosted plugin delivery is separate.

The [guided onboarding](../reference/onboarding.md) now provides one conversational
procedure for both skills: inspect what exists, explain the next action, complete
authorized work, verify and resume. It includes delivery roles for agencies,
freelancers and businesses, without making technical experience an intake gate.
The [GTM capability path](operations.md#future-gtm-writes) anticipates editing by
operation, with workspace evidence, scope checks, concurrency and recovery. It does
not enable a future tool or turn a release expectation into measured availability.

The maintained guides cite public product documentation. Raw collected documents,
screenshots and authenticated tool catalogues are now preserved outside this
repository with verified hashes. They are not package dependencies. Synthetic
archive fixtures exercise the verifier in CI. Historical Git objects still contain
earlier collections. The owner made the repository public for an entry-path test
on 2026-10-16; this does not clear those historical collections for redistribution.
The separate public-history review remains unresolved. No visibility or history
change is included in the first-conversation correction below.

Capability discovery and authenticated reads establish only the current connection's
available path. They do not establish effective write permissions, production
parity, complete browser behavior or support in a different AI client. Refresh
discovery when tools or grants change. Public MCP pages were unavailable during
source checks, so this release does not advertise a verified production endpoint.

| System | Advertised capability | Boundary |
| --- | --- | --- |
| Consent Pro reads | Projects, setup, diagnosis, trackers, scans, stats, preview and documentation | Follow pagination and detail pointers; missing is not zero |
| Consent Pro writes | Custom-site creation, domain change, scan start/settings, banner style, privacy link, export/proof requests | Some are drafts; others change assets, start work or queue email |
| GTM | Status, containers, audit and details | Published-container reads, not unpublished workspace writes |
| Consent Pro publication/categories | No matching tool in this snapshot | Use the dashboard; never claim completion through MCP |
| Additional MCP operations | Adopted separately when available | Require a discovered, reviewed and tested tool contract |

## 2. What was analyzed

The base repository was searched by topic before adding this documentation home.
It already covered GTM configuration and browser checks, but lacked an installation
package and the broader client workflow. Source-to-guide comparison identified:

- Reversed GA4 Basic/Advanced advice. Basic requires the documented consent gate;
  Advanced uses its own initialization sequence and must be chosen explicitly.
  [Google Consent Mode](https://docs.consentpro.com/web-app/google-consent-mode).
- A singular image category attribute instead of `fs-consent-categories`.
  [Image trackers](https://docs.consentpro.com/web-app/image-trackers).
- A false one-page-versus-whole-site scan guarantee. Sitemap and link discovery
  have coverage limits. [Sitemap](https://docs.consentpro.com/web-app/sitemap).
- Outdated assertions that MCP did not exist, guessed debugger URL parameters and
  overly broad free-staging language. Preview, licensing and three publication
  surfaces needed separate explanations.

The original writer was exercised through its actual entrypoint against a fake
API, with network and credentials replaced. It reused a wrongly configured trigger
by name, replaced purchase-event triggers and removed a second regional row.
Historical evidence and current regression commands live in [checks](checks/README.md).
These are local code findings, not claims of an incident in a customer's account.

### Conflicting sources remain explicit

- Staging scan-settings schemas say sitemap/collection values are saved but not
  yet used. Pinned pages replace discovery. Public product instructions alone
  cannot establish this server's implementation.
- Licenses and MCP describe preview of saved drafts with region simulation;
  Debugger also says regional mappings need publication. Test the actual path
  without publishing just to resolve a documentation contradiction.
- Public GTM instructions still describe a template download. The repository
  retains its reviewed Gallery implementation and pinned version.
- Some runtime references describe a two-script model or incompatible event API
  forms. Use the exact project snippet and platform-specific contract; do not
  combine examples from different runtime trails.

The executable workflow and source-specific cautions are in
[operations](operations.md), not duplicated as an unconditional product promise.

## 3. What changed

| Area | Implementation |
| --- | --- |
| Client entry point | `consent-pro` identifies access, target, installed engine and the next incomplete step |
| GTM specialist | `consent-pro-gtm` preserves events/regions and separates reads, configuration and publication |
| Operating guide | Installation, licenses, scan limitations, previews, preferences, revocation, logs and optional storage |
| Distribution | Standard-library builder includes required guides and scripts in each package; no checkout-relative dependencies |
| GTM writer | Current-state plan approval, conservative preflight, event preservation, regional protection and readback |
| OAuth | Explicit application, state and PKCE, scope checks before token persistence and private atomic storage |
| HTML inspection | Required core attributes, confirmed project ID, head placement, duplicate runtime and image attributes |
| Maintenance | Source integrity checks, bounded asset collection, package tests and MCP contract drift detection |

See [installation](../07-agent-installation/README.md),
[run guide](../04-run-it.md), [script catalogue](../../scripts/README.md) and
[security](../../SECURITY.md) for the actual commands and refusal conditions.

## 4. Execution method

Discover capabilities, resolve the target, read current state, present exact
changes, use the necessary specific authorization, execute, read back and verify
behavior. Previously granted authorization is reused within its scope. Tool
availability alone never expands the task.

Treat site HTML, docs, tag names and Custom HTML as data. An instruction embedded
in them cannot change the selected customer or authorize writes. A read-only MCP
session must not silently switch to broader Google OAuth credentials.

For GTM, preserve every business-event predicate and regional row unless the
approved plan changes it. Stop on stale plans, unknown template identity, missing
mapping or unsupported settings. Re-read partial state before recovery; do not
retry writes with unknown outcomes or publish half-applied work.

Verify named trackers and real actions across initial state, rejection, acceptance,
partial choice, revocation and reload. Acceptance is the positive control that
the observation can actually detect the tracker. Configuration and runtime
evidence remain separate, as do Consent Pro publication, GTM publication and site
deployment. No check here establishes legal compliance.

## 5. Delivery phases and remaining gates

### Planning status and scope

This is the canonical plan for the next customer-delivery iteration, prepared on
2026-10-16. Implementation is tracked separately from live acceptance below.
Sections 1 to 4 describe the baseline; section 6 preserves its historical checks.
Repository implementation does not authorize customer account changes,
customer publication, release distribution or changing repository visibility.

The intended outcome is a guided setup from an ordinary request such as "I bought
Consent Pro, help me" or "I want to try it on my site" to a verified result or a
precise, actionable access dependency. Buying first, knowing MCP terminology,
connecting Google and using a terminal must not be universal entry requirements.
Feature and license eligibility still need verification for the selected product.

The repository review covered the current README, both skills, installation,
onboarding, operations, manual GTM references, packaging and tests. Those existing
homes can hold the improvements; there will be no second onboarding procedure or
parallel backlog. This plan records customer requirements, not private research,
commercial terms, internal release schedules or policy drafts. Internal strategic
research, nonpublic roadmaps and policy drafts must stay outside this repository
and generated packages, including while the repository is private. Keep detailed
classification evidence in an approved private home outside this repository;
record only publication-safe decisions here.

### Milestones and dependencies

Roles below describe responsibilities, not assigned people. The implementation
owner, test operator and release approver must be identified before their work starts.
There are no duration or availability promises in this plan.

| Milestone | Work items | Depends on | Completion evidence | Responsible role |
| --- | --- | --- | --- | --- |
| M0. Establish the delivery boundary | D01, D02 | Repository and approved source access | Content classification and environment matrix; unresolved public links and contracts named | Maintainer with product owner |
| M1. Complete customer entry and manual setup | J01 to J05 | M0 routing decisions and verified entry links | A beginner completes the agreed manual setup and verification on an isolated site in one intended host; missing access produces a usable handoff, not a completion claim | Guide maintainer with test operator |
| M2. Complete support, resumption and ownership | J06, J07 | M1 progress record; verified support route for J06 only | A second session or responsible person resumes without repeating setup or inheriting credentials; support handoff follows the verified route | Guide maintainer with support owner |
| M3. Deliver reproducible client packages | D03, D04 | M0 content decisions; M1 and M2 instructions for final candidate | Versioned artifacts work outside the checkout and pass the intended client's real installation path | Package maintainer with client testers |
| M4. Validate and release the supported journey | V01, V02 | M1 to M3 and an authorized isolated test target | Recorded end-to-end results, declared limitations and explicit release approval | Test operator and release approver |
| M5. Adopt additional MCP operations | C01 | A deployed tool contract, effective grants and isolated test access | Each operation passes its own scope, conflict, recovery and readback checks | Integration maintainer with product owner |

M3 packaging work can run alongside M1 and M2 after M0. M5 is an independent
capability track, not a prerequisite for the manual journey or a promise tied to
a date. M4 can release a clearly scoped manual/read experience while unsupported
operations remain manual. An unresolved production endpoint blocks production
connector claims, not work on guides, packages or an explicitly labeled test path.

The first usable milestone is M1: a customer in chat, without a terminal or Google
connection, reaches the correct project, chooses whether GTM is needed and follows
the manual route through the agreed setup and verification, including resumption
after leaving. When access is missing, the route produces a concrete dependency
and continues independent work; it does not call that setup complete. The first
isolated demonstration does not establish support in every host or coverage of
every page and tracker on a customer's site.

### Customer journey work

| ID | Change and canonical home | Acceptance condition |
| --- | --- | --- |
| J01 | Add entry-state routing to [onboarding](../reference/onboarding.md); add verified sign-up, login and recovery paths to [installation](../07-agent-installation/README.md) | Plain-language requests work without a perfect prompt. The agent asks only for the next missing fact and never requests passwords, login codes or tokens in chat |
| J02 | Complete account, workspace, project and license diagnosis in [operations](operations.md) | An empty list is distinguished from missing access or the wrong workspace; an existing purchase is investigated before another purchase is suggested; project creation follows target confirmation and authorization |
| J03 | Add the GTM decision and manual entry to [GTM account setup](../02-tag-manager-account.md), with routing in onboarding and both skills | The customer can choose no GTM, adopt GTM, use existing GTM manually, or use available agent capabilities; Google Cloud and local OAuth are required only for the optional local API route |
| J04 | Complete the account-to-site handoff and guided interaction in [nine steps](../reference/nine-steps.md) and [beyond GTM](../05-what-gtm-does-not-cover.md) | Snippet installation, configuration, Preview and publication have an explicit sequence based on the container's current published state and the test environment; declining Google OAuth leaves a complete manual path |
| J05 | Add existing-installation routing to operations and onboarding | Existing CMPs, direct pixels, duplicate scripts and conversion events are inventoried before changes; the plan preserves business events and identifies any required migration or rollback |
| J06 | Add support escalation to [troubleshooting](../reference/troubleshooting.md) and the operations handoff | A verified support route and current eligibility determine the offered help; the agent prepares a minimal handoff and only sends it on explicit instruction |
| J07 | Extend onboarding's progress and completion records | A returning customer or new maintainer can distinguish reported, inspected and tested work; changed versions are reread, and each person uses their own authorized connection |

Entry routing should cover the following states behind the conversation. It must
not become a questionnaire shown in full to every customer.

| Customer state | Next action | Condition for moving on |
| --- | --- | --- |
| No account, or exploring before purchase | Explain the verified account entry and available trial/test path | Customer signs in, or chooses a manual preparation step; do not assume universal free access |
| Cannot sign in | Distinguish an expired session, login method, recovery and organization access | Customer completes recovery through the official interface; no secret enters chat |
| Paid plan or site license is missing | Check the account, workspace, purchase and domain/license assignment using available evidence | Correct entitlement is found or a support handoff identifies the discrepancy; no automatic second purchase |
| Account works, assistant connection is missing | Identify the host and offer its supported instructions/connector route or guided dashboard work | The connected route verifies instructions and authenticated workspace separately; the manual route confirms the target with available evidence and labels what the customer only reported |
| No projects appear | Check workspace, permissions and complete pagination before deciding the project is absent | Existing project is selected, access is requested, or creation is explicitly authorized |
| Site has no project | Confirm domain, platform and owner; use the supported create/connect path | Project identity and its exact install snippet are verified |
| Setup is partly complete | Inspect the current project and site | Continue at the first incomplete dependency without duplicating installation |
| Customer does not know whether GTM exists | Inspect available site evidence and explain its limits | Confirm the container using available account or dashboard evidence before edits; an observed public ID alone is not ownership |
| No GTM is installed | Ask whether the customer wants or needs to adopt it | Continue with direct integrations, or make GTM adoption an explicit setup decision |
| GTM is accessible only to the customer | Guide the dashboard path and inspect the evidence they choose to share | Continue without requiring an API connection |
| Neither customer nor agent can edit GTM | Prepare a precise administrator request | Record the access dependency and continue independent Consent Pro/site work |
| All required access is available | Diagnose, agree the applicable changes and use supported operations | Read back settings and run behavior checks before claiming completion |

Update both skill entrypoints to route into these shared references. Keep the
top-level README and [journey map](../00-the-journey.md) short: entry action, available
routes and next destination. Customer-facing instructions should adapt to the
conversation language; canonical repository content remains English. An absent or
declined connector blocks only connector-dependent actions, including when the
customer operates both Consent Pro and GTM entirely through their dashboards.

### Manual GTM experience

J03 and J04 must connect the whole route: account/container selection or creation,
site snippet installation, duplicate check, template installation, Consent
Initialization tag, explicit global/regional defaults, the applicable consent
events, tag consent settings, Preview/Tag Assistant, separately authorized
publication and post-publication behavior checks. Reuse the technical procedure
in nine steps rather than maintaining another copy.

The sequence depends on existing published configuration. Installing a previously
absent GTM snippet can activate the container's already-published tags. Inspect
that version first and coordinate site deployment, consent configuration and GTM
publication on the approved test target before exposing visitors to those tags.
Snippet installation must be verified, but must not always precede tag setup.

Every guided action must state its purpose, exact destination, controls and values,
expected result, verification method and recovery when the screen differs. Show
one useful action at a time. Inspect language, current screen, permissions and UI
version before repeating instructions that the customer says do not match.

Gather evidence progressively: confirm the container, inspect the relevant tag
list, open a specific tag's type/triggers/consent settings, then consider an export
only if needed. Explain what an export or screenshot shares and have the customer
remove secrets and unrelated information. Do not request a full container export
as the default first step or commit customer exports to this repository.

"Done" records a customer report until the result can be inspected. A screenshot
may verify a configuration, but not network/storage behavior. `consent-updated`
also follows rejection; creating it does not gate a tag by itself. Purchase,
form and lead predicates must survive consent changes. A consent event must not
create a purchase or replay one merely because preferences changed.

Handle an existing CMP as a migration decision: identify consent ownership,
defaults and integrations; propose the transition and recovery; obtain the
necessary approval before replacing it. Do not install a second CMP as an
unexamined fix. Test the agreed Basic or Advanced Consent Mode behavior; do not
use zero network requests as a universal pass criterion.

### Support, maintenance and continuity

J06 must offer guided setup, verified assisted implementation when eligible, or
human review when available. Do not require customers to exhaust a long manual
procedure before showing an applicable assistance option. Confirm current offer
terms and the official support route before promising inclusion, price or response
time. Keep commercial source material outside the distributed instructions.

J07 should extend the existing record with target/environment, current milestone,
settings saved, publications per system, named behavior checks, outstanding issues,
next action and responsible role. Keep customer-specific records in a private,
user-approved location or a copyable conversation summary, not in this repository.
The next session must reread affected state after expiry, manual edits or publication.

A support handoff includes only the relevant site, issue, current state, attempted
steps and access needed. Exclude tokens, signed preview links, consent identifiers,
individual visitor records and unrelated customer details. Preparing a handoff is
not opening a ticket. A successor verifies their own project, site and GTM access;
credential transfer and automatic revocation are not part of handing over the guide.

Maintenance instructions should identify who reviews the setup after a new pixel,
integration, site deployment or policy change. Scheduled scans are optional and
depend on current capability, plan and authorization, including any report-email
effect. A scan schedule is not continuous monitoring or automatic repair.

### Distribution and public-content work

| ID | Change and canonical home | Acceptance condition |
| --- | --- | --- |
| D01 | Classify the existing source archive, images, fixtures, research and links in this documentation home and [security](../../SECURITY.md) | Each item has a public, private or unresolved destination with provenance and permission evidence; authenticated retrieval is not treated as permission to redistribute |
| D02 | Separate environments in installation, operations, README and both skills | Customer service, product development staging and the customer's test site have distinct purposes, verified destinations, effective access and limits; no production endpoint is guessed |
| D03 | Version [package output](../../scripts/package-skills.py) and update its [tests](../../tests/test_skill_packages.py) and [script catalogue](../../scripts/README.md) | Artifacts identify release, source commit, channel and hashes; approved contents and required links work outside the checkout, without private sources or mutable `main` dependencies |
| D04 | Complete per-client install/update/remove instructions in installation | Each supported client has a ready artifact or verified installation route, an identifiable loaded revision and an update test; customers need not build a package to start |

D01 starts with the current tree and relevant history. Hash integrity alone does
not review screenshot content or establish redistribution rights. If evidence must
move out, preserve it in its approved private home before removing public copies.
Replace CI dependencies with approved or synthetic fixtures and retain failure
controls. Removing a file from the current tree does not remove its history.
History rewriting, a clean public export and visibility changes require a separate
decision after classification; no automatic deletion is part of this plan.

D02 must also distinguish a customer's test hostname from Consent Pro's internal
development service. A free preview entitlement, when verified, does not imply
access to internal staging. Publishing Consent Pro, publishing GTM and deploying
the site remain separate actions with separate authority and verification.

D03 must produce versioned archives and checksums from a pinned source, check the
ZIP root and required references, reject unapproved files and verify repeatable
content. Public-ready packages must not depend on GitHub authentication or internal
documents. Prefer bundled essential references; any required external reference
must resolve to approved content at a stable version. Updating source or a ZIP
does not update a hosted plugin or prove its OAuth connection survived an update.

### Acceptance and measurement

| ID | Work | Completion evidence |
| --- | --- | --- |
| V01 | Expand the [scenario suite](../../tests/README.md) with the cases below and deliberate failure controls | Expected outcomes, observed outcomes, evaluator method and negative controls recorded; simulations labeled as such |
| V02 | Run the full customer path in each intended client and on an isolated site/container | Versioned artifact, host/version, environment, permissions, steps, observed results and limits recorded; real behavior distinguished from configuration and conversation tests |
| C01 | Refresh tool discovery and adopt additional operations using the [capability path](operations.md#future-gtm-writes) | Review effective Consent Pro permission, any separate Google grant and container role, target/workspace, draft/live effect, concurrency, failure recovery and readback for each operation |

The scenario suite must include: no account; testing before purchase; login failure;
purchase not visible; wrong workspace or empty project list; no GTM by choice;
adopting GTM; an existing but uninstalled container; declined Google OAuth; GTM
read access without edit access; customer-only dashboard access; neither party
having access; direct pixels and an existing CMP; purchase/form tags; a mismatching
UI; "done"; returning after another person published; switching agency clients;
assisted setup eligibility; support handoff; successor access; and "is it ready?".

Failure controls must reject duplicate projects used to bypass access problems,
repurchase without checking an existing entitlement, terminal requirements in the
manual path, forced Google reconnection after refusal, inherited authority across
clients, lost business predicates, hidden publication and claims based only on a
customer's reported click. Unknown new tools must not inherit approval from a
similar tool name. New permissions and Google scopes are verified separately.

| Client | Real path to verify before claiming support |
| --- | --- |
| ChatGPT Chat/Work | The intended plugin/instructions delivery, new and existing conversation activation, authenticated target read, OAuth return and upgrade preserving the intended connection |
| Claude web/Desktop | The actual skill/import and connector path in each supported host, references accessible, conversation activation and manual-step resumption; local scripts only where execution is supported |
| Codex app/CLI | Installation, actual instruction loading, discovery, OAuth, target read, supported local entrypoints outside the checkout and update/recovery in each supported interface |
| Claude Code | Native installation, invocation, references, supported local entrypoints, MCP sign-in, target read and resumption |

Mark each tested combination `PASS`, `FAIL`, `NOT TESTED` or `UNAVAILABLE`, with
date and limits. A successful Codex test does not establish Claude support. A
simulated conversation does not establish live OAuth, edits or browser behavior.
For supported writes, test an authorized disposable target and interruptions or
conflicts before customer use; never discover write behavior on a customer asset.

Browser acceptance uses named trackers and network/storage observations for
initial state, rejection, acceptance as a positive control, partial choice,
withdrawal and reload. Exercise actual purchase/form actions where applicable;
record what did and did not fire. Interpret Google behavior using the chosen
Consent Mode. Separate draft preview from published behavior and list pages,
regions, devices and integrations not covered. No result is legal certification.

Also check regional fallback and conflicting assignments against the customer's
chosen policy, without treating broad country rules as legal advice. Distinguish
aggregate consent statistics from an individual consent record. When an authorized
report request is supported, an acknowledgement proves the request was accepted,
not that a report was delivered. Keep personal records out of test fixtures and
public evidence. New-tracker detection must lead to review, not automatic approval.

Beginner sessions should measure completion against the agreed task, active
customer time separately from waiting, abandonment versus an unresolved dependency,
manual/support interventions and defects remaining or reopened. Define the cohort,
start/end points, count and denominator before reporting a rate. Keep participant
records private, minimize collection and publish only approved summaries. Do not
claim a setup duration, completion rate or risk reduction before measuring it.

### Decisions needed and first execution slice

| Decision or evidence needed | Resolver | Blocks |
| --- | --- | --- |
| Approved sign-up, recovery, account/license and support destinations; current assistance eligibility | Product/support owner | The affected J01, J02 and J06 instructions |
| Verified production endpoint, dashboard, scopes and documentation | Product/integration owner | Production connector claims in D02 and V02, not the manual route |
| Classification of archived sources and research; handling of historical copies | Repository owner | Public artifacts and visibility changes in D01/M4 |
| Intended host editions, supported delivery format and artifact release location | Maintainer with release owner | Final D04 packaging and V02 client matrix |
| Disposable site/container, test operator, permitted actions and any cost ceiling | Test owner with asset owner | Live V02/C01 execution; no paid autonomous loop without a fail-closed ceiling |
| Released contracts for new MCP operations | Integration owner | Only the corresponding C01 operation |

The initial execution slice is implemented in the existing homes. Current delivery
and acceptance states appear below. The next customer-acceptance action is to run
one full beginner journey on an explicitly designated disposable site/container,
with a named operator and permitted effects. Production destinations and new MCP
writers remain independent dependencies, not reasons to stop the manual route.

This repository delivers instructions, references and local tools. It does not
provide a persistent service, automatic cross-chat memory or background maintenance.
Private architectural research is not part of the customer distribution.

Planning review: separate journey and distribution readers checked the proposed
scope. Their corrections preserve a fully manual Consent Pro route, make GTM
snippet order depend on the published container, align M1's completion criteria
and keep internal source material outside this repository even while private.
The repository checker passed for 203 local Markdown links and authored punctuation;
its two existing positive/failure-control tests passed. This was documentation
validation, not a new customer journey, package or live capability test.

The validation record below is updated from commands run against this implementation.
Do not convert an offline passing test into a claim of a live customer setup.

## 6. Expected impact and limits

The agent can resume from a client's real state instead of treating every request
as a new GTM installation. Drafts, queued work, publication and observed browser
behavior have explicit meanings. Future GTM writing has an entry contract without
being advertised as already available. No time saving or conversion improvement
has been measured.

The archive contains extracted page content and assets, not raw HTML or the whole
Webflow documentation tree. All asset hashes were checked; not every screenshot
was visually inspected. New HTTP header guards were added after the original
download, whose response headers were not retained. They cannot retroactively
prove those responses' header framing.

No real customer container, scan, banner, privacy link, category, publication or
email request was changed during implementation. Live Google writes, all MCP
mutations and production runtime behavior remain outside the completed local
verification. Hosted package delivery is tracked separately from those operations.

### Baseline validation and evidence

Measured on 2026-10-16 for the earlier implementation delivered in
[PR #3](https://github.com/redeuno/consentpro-gtm-ai/pull/3). These baseline measurements
are preserved separately from the later onboarding revision below:

| Check | Observed result | Limit |
| --- | --- | --- |
| Standard-library unit suite | 116 tests passed | Google API and OAuth responses are simulated |
| Mutation controls | 36 deliberate guard removals rejected by assertions | Selected controls, not exhaustive mutation coverage |
| Script statement coverage | 87% overall; writer 87%, OAuth 92%, inspector 88%, package builder 85% | Statement coverage is not behavior proof |
| Collector tests | Two header tests and seven collector tests passed | Fault injection and real HTTPResponse parsing, not a production proxy test |
| Archive checks | 13 Web App pages, six references and 71 assets verified; four negative controls rejected | Original response headers were not archived |
| Bounded collector smoke | One 53,486-byte public PNG downloaded and matched the archived SHA-256; repeat reused it with zero transfer | Original archive stayed unchanged |
| Package user path | Both packages built outside the checkout; script help and local references passed; modified installation refused | No customer credential was used |
| Native Codex discovery | Codex 0.163.0 found both skills through `skills/list` in a disposable project | No model or business-tool call; native Claude not tested |
| Skill behavior scenarios | No-connector, read-only ambiguity and an already-authorized draft edit produced the expected boundaries | Simulated conversations, no real mutation |
| Public-site inspection | Revised inspector ran against the staging lab HTML | HTML declarations only; no browser behavior or project identity inferred |
| Independent review | Approved for commit after the three reported defects were fixed and the 116 tests and 36 mutation controls passed again | Live Google API compatibility and browser behavior remain unverified |

The first independent review found three defects: filtered page-view triggers
could prevent trackers from starting after acceptance, version readback omitted
non-tag collections, and valueless image sources could crash HTML inspection.
Regression tests now cover each defect. The second independent review found no
blocking issue in the corrected scope and approved it for commit.

The local GTM writer has no transaction or automatic rollback. It reads the
container's declared capabilities and all supported version collections, then
compares every collection and container settings before publication. Unsupported
collections must remain empty. An API race cannot be made atomic by these scripts;
readback prevents an unapproved resulting version from being published by this run.
Strict response comparison may refuse unmodeled Google defaults; isolated live
acceptance is required before a client rollout.

### Earlier onboarding revision and delivery

What changed: consolidated the guided conversation from the parallel proposal with
first-chat installation, recovery, precise dashboard handoffs and evidence-based
continuation. Both skills use the same procedure. Customer concerns become practical
checks for blocking, Consent Mode, records, regional configuration and maintenance.

The execution decision is capability-based, not date-based. New GTM editing must be
reviewed and tested per operation before use; unrelated supported work can continue
while a permission or tool is missing. The local writer implementation is unchanged.

Measured again for this revision on 2026-10-16:

| Check | Result | Scope |
|---|---|---|
| Unit/package suite and mutation controls | 116 tests passed; 36 altered guards rejected | Offline APIs and fixtures, no customer writes |
| Collector and archive checks | Two header and seven collector tests passed; original archive and four negative controls passed | Historical bytes and local failure controls |
| Supplemental MCP guidance | Three body hashes and complete-page markers verified; changed-content control rejected | Public documentation obtained through MCP, not effective grants |
| Packaged skills | Both built outside the checkout; ZIP roots and every manifest hash checked; both skill validators passed | Local package delivery, not hosted installation |
| Native Codex discovery | Both packages discovered in a disposable project; zero business calls | Client discovery only |
| Instruction behavior | Nine future-capability and three delivery-team cases produced the expected simulated decisions | No real future MCP tool or browser behavior exercised |
| Independent native review | No concrete defect found in the documentation and skills; accepted for integration | Reviewer rechecked selected tests and integrity; did not repeat the full suite or live acceptance |

The scenario method is recorded in [tests](../../tests/README.md). Hosted
ChatGPT/Claude plugin updates, native Claude execution, actual new MCP writes and
customer browser acceptance remain unverified. An updated repository or built ZIP
does not update an installed hosted plugin.

These measurements precede the customer-entry implementation below. New MCP
operations still need separate isolated acceptance under C01.

### Customer-entry implementation, 2026-10-16

| Work | Delivered state | Acceptance still required |
| --- | --- | --- |
| J01/J02 | Official account entry, access recovery guidance, purchase/workspace/license reconciliation and first-project routing | Real account and entitlement cases; no private recovery URL or assistance entitlement is assumed |
| J03/J04/J05 | GTM choice, direct integrations and complete manual CP/GTM procedures; existing published-container and CMP transition checks | Full browser/network/storage path with a consenting test operator and disposable targets |
| J06/J07 | Verified public assistance routes, minimal support handoff, copyable continuation record and successor access checks | A real support/service outcome and customer handoff; preparing text sends nothing |
| D01 | 80 source files privately preserved and hash-verified before removal; synthetic CI archive fixtures; retained template code attributed and licensed | Historical Git objects are not cleared for public redistribution; current visibility is recorded above |
| D02 | Customer service, internal product staging and customer test hostnames separated; production endpoint left unverified | Product owner supplies and verifies the production connector and effective permissions |
| D03 | Versioned package builder, explicit source allowlist, checksums, pinned provenance and deterministic preview ZIPs from `7925bbb` | Stable production distribution remains a separate release decision |
| D04 | Ready-artifact installation, upgrade/recovery and removal routes; actual local Codex installation and private ChatGPT plugin update | Claude web upload and the remaining host-specific acceptance below |
| V01 | 23 fictional customer responses independently generated and coordinator-reviewed against explicit criteria, with manual negative alternatives | Repeated response reliability and human beginner sessions are not measured |
| V02 | Native Codex and Claude Code package discovery measured outside the checkout | Complete host-specific OAuth, resume, update and site behavior acceptance |
| C01 | Operation-specific discovery, review, permissions, concurrency and recovery procedure retained | Announced GTM writes are not considered available until their actual contracts and isolated behavior are verified |

The scenario inputs, responses, criteria and limits are linked from
[local verification](../../tests/README.md#guided-onboarding-behavior-evaluation).
The first native review reproduced three package defects: Windows path separators,
CRLF checkout provenance and a parent-directory alias that bypassed archive nesting
checks. The second review found an additional case-insensitive filesystem alias.
All four have targeted regressions and failure controls. The final native review
reproduced the fixed CLI boundaries and the old defective comparison, verified
Claude discovery/isolation controls, and approved this scope for integration.
The writer and OAuth implementations are unchanged in this delivery.

| Local measurement | Observed result | Boundary |
| --- | --- | --- |
| Offline suite | 143 tests passed, including 29 package tests | Simulated APIs and local filesystem behavior |
| Writer/inspector mutation suite | All 36 deliberately changed guards rejected | Selected executable safeguards |
| Package controls | Eight code mutations rejected, plus a missing-LF-rule control; all 29 package tests passed in native Windows CI | Includes Windows path representation, real CRLF checkout and native macOS case aliases; no live customer operations |
| Archive and boundary checks | Six synthetic tests; private original archive verification and four negative controls passed | Original source bytes remain outside the repository |
| Asset collector checks | Two header and seven collector tests passed | No new customer data or site writes |
| Codex 0.163.0 | Both packaged skills discovered in a disposable project | No model or business call |
| Claude Code 2.1.296 | Both skills discovered, one removed and absent, both rediscovered after restoration | Network and credential access denied; no model prompt; not Claude web/Desktop acceptance |
| Fictional conversations | 23 recorded next responses met the reviewed scenario criteria | Independent response probes and manual grading, not a human customer study |

The artifacts are a preview of the customer instructor, not a claim that every
supported client or a live customer setup has passed acceptance. Repository
privacy was the delivery boundary for that revision; customer packages exclude
the private archive and do not need it at runtime. No background agent, automatic cross-chat memory or
continuous consent monitoring is installed by these instructions.

### Preview delivery and client acceptance

The `0.2.0` preview packages are built from clean source commit
[`7925bbb`](https://github.com/redeuno/consentpro-gtm-ai/tree/7925bbbfd859882df520548dcf868bcee32a070c).
Two consecutive builds produced identical archives and manifests. Both ZIPs passed
their `SHA256SUMS` check. The [release](https://github.com/redeuno/consentpro-gtm-ai/releases/tag/v0.2.0)
contains the two archives and checksum file; the repository was private at delivery.
Later status-only commits do not change these pinned package bytes.

Native Windows CI initially exposed two package tests that relied on the default
text encoding. Their fixture I/O now explicitly uses UTF-8. The corrected
[Linux and Windows run](https://github.com/redeuno/consentpro-gtm-ai/actions/runs/38972533492)
passed, including all 29 Windows package tests. The final installation-guide edit
also passed those 29 tests locally and the repository checker.

| Client or delivery surface | Status and measured evidence | Remaining limit |
| --- | --- | --- |
| Local Codex installation | PASS for package installation: both skills installed and updated to `7925bbb`; all 26 payload hashes in each package matched its manifest; previous folders preserved outside discovery | Native CLI discovery was measured separately. Codex app UI, a new-session invocation and a complete customer journey are not established by file installation |
| ChatGPT private plugin | PASS for update/readback: version `1.1.1`, both skills, all 56 hosted files equal the reviewed archive; existing app binding and audience preserved | Plugin version and skill-package version are separate. This does not establish public distribution or every ChatGPT edition |
| Authenticated Consent Pro read after plugin update | PASS: a read returned the same intended workspace and matching project after both updates | No new OAuth grant, Google write, scan, account mutation or publication was performed |
| New ChatGPT Work conversations | PASS for instruction loading: the final conversation read both `0.2.0` preview manifests, exact `7925bbb` source and the corrected pre-install verification. The earlier candidate continued the fictional manual GTM route without requiring Google OAuth | Final chat could not read the plugin wrapper version; `1.1.1` was verified through the backend and plugin UI. These checks do not establish a complete beginner journey or automatic onboarding |
| Claude Code | PASS for native discovery, missing-skill control and restoration in an isolated project | No real account connection, model prompt, write or live site test |
| Claude web | UNAVAILABLE at upload: the actual Customize, Skills, Add Skill, Upload Skill path opened and accepted file selection intent, but the browser extension required additional local-file access before upload | Permission was not expanded. No skill was imported; conversation loading, update and removal remain NOT TESTED |
| Claude Desktop and Codex app UI | NOT TESTED in their native interfaces | CLI and browser evidence cannot establish desktop-interface acceptance |
| Live customer completion and new MCP writers | NOT TESTED | Require a designated disposable site/container, effective permissions and operation-specific acceptance |

The private plugin has an onboarding-skill entry, but connecting an MCP by itself
does not prove an instructor was automatically activated. The supported entry
remains selecting the installed plugin or skill and asking for setup help.
Installation proofs and account-specific screenshots stay in the private evidence
home. No account identifiers or customer exports are needed in this repository.

Next action: run one full beginner journey on a designated disposable site and
container, with a named operator and explicitly agreed effects. Record the actual
browser checks, pauses, resumption and remaining dependencies before claiming
customer-ready end-to-end support.

### Claude first-conversation correction, 2026-10-16

A customer-reported Claude web trial exposed a confusing entry path: a failed
repository read, a repository overview, a second prompt to copy and repeated setup
questions. A later reader succeeded, and the customer reported uploading the
`0.2.0` skill. That report is useful feedback, not a maintainer-observed upload or
a complete customer setup test.

The README and both skills now direct the assistant to use readable instructions
in the current conversation. Persistent installation is optional. The next action
uses existing site/project evidence, and an explicit skill or connector request
can be completed before obtaining a website URL. Claude guidance prepares a ZIP
when tools permit, guides only the remaining account actions, and resumes after
"installed" without repeating known facts. Missing tools do not prove account
restrictions. A plain-text README link provides an alternative reading route;
instructions cannot control a reader before it retrieves any repository content.

The [first-conversation evaluation](../../tests/README.md#claude-first-conversation-instruction-checks-2026-10-16)
records six reviewed fictional cases and two additional Portuguese response probes.
No business calls were made. A separate document review corrected target discovery
and file-verification wording. The released `0.2.1` preview carries these changes;
installed `0.2.0` skills and the previously tested ChatGPT plugin remain unchanged.
Package checks establish bundled-file integrity, not actual Claude behavior.

Local verification for this correction passed 30 tests (29 package checks and
the public-content boundary check), 249 local Markdown links and punctuation,
and whitespace validation. The built-in web reader could not fetch the repository
or its raw README; a direct unauthenticated HTTPS read of the raw README returned
200. This verifies that one public reading route worked in this environment,
not that another host's reader will succeed.

The [0.2.1 release](https://github.com/redeuno/consentpro-gtm-ai/releases/tag/v0.2.1)
is pinned to clean source
[`26a99ac`](https://github.com/redeuno/consentpro-gtm-ai/tree/26a99acc4ab9cd661a1dd285df6835510c2b3e96).
Two builds produced identical archives. Every manifest hash and release checksum
matched; the two downloaded ZIPs and checksum file equaled the reviewed build.
An unauthenticated download of the primary ZIP also returned the reviewed bytes.
The [candidate CI run](https://github.com/redeuno/consentpro-gtm-ai/actions/runs/38989368205)
passed both Linux checks and Windows package checks. These are artifact and
repository checks, not a new Claude web installation or hosted-plugin update.

Next acceptance: start a fresh Claude conversation with the repository URL and a
plain setup request, then check the first reply, a missing-connector path and
resumption after optional skill upload. Record reader failures separately from
instruction failures. Full site setup and public-history review remain open.

### Connection choice and inspection evidence, 2026-10-16

A further reported Claude trial read the guide successfully but chose manual work
without offering the supported connector. The earlier entry criteria favored asking
for a site URL and preventing mandatory uploads; they did not require an active
connection recommendation. The `0.2.2` preview corrects that route choice for full
setup, offers the reusable skill once and preserves explicit manual choices and
narrow public-site inspections. It still verifies the product environment before
offering an endpoint and does not advertise an unverified production MCP.
A contrasting customer-reported ChatGPT trial already had its plugin, instructions
and MCP active. That path should reuse the connection, resolve the client's target
and preserve deliberate lab controls until the goal is clear. No reinstall is needed
merely because a fresh conversation began; this report does not establish the exact
package revision or independently verify the reported audit findings.

Independent source inspection also showed why rendered HTML can mislead diagnosis.
The operating guide now distinguishes declared scripts from injected DOM elements,
explains the standard GTM bootstrap and keeps the project's single core snippet
separate from component assets. Runtime host changes require the intended product
environment; a test hostname or old website comment does not authorize migration.
No customer identifiers, source HTML or private account evidence are included here.

The new [evaluation criteria](../../tests/README.md#connection-choice-and-source-evidence)
cover connection choices, environment preservation and rendered-HTML false positives.
All ten fictional responses met the reviewed decisions, including reuse of an
already configured ChatGPT plugin. Manual negative alternatives were rejected.
These are instruction probes, not observed actions in those hosts.
Local package/content checks passed 30 tests; both skill validators passed. These
checks do not establish that Claude follows the new instructions or that a site's
trackers respect consent. Live runtime behavior and the actual Claude journey remain
separate acceptance work.

The [0.2.2 release](https://github.com/redeuno/consentpro-gtm-ai/releases/tag/v0.2.2)
uses clean source
[`1541859`](https://github.com/redeuno/consentpro-gtm-ai/tree/154185945962d7e36630414f1d879eea86f4860b).
Two preview builds were byte-identical, with every manifest hash and release
checksum verified. Anonymous downloads of both ZIPs and `SHA256SUMS` matched the
reviewed files. The [candidate CI run](https://github.com/redeuno/consentpro-gtm-ai/actions/runs/38991932444)
passed Linux checks and Windows package checks. Existing installed skills and the
previously tested private ChatGPT plugin were not updated by this repository release.
Next acceptance: compare a fresh Claude setup with no connector against an already
configured ChatGPT conversation, then verify the chosen path on an authorized test
target. Keep actual tool execution separate from the response probes above.

### Public sources and release boundaries

Account entry is verified against [Finsweet Account](https://finsweet.com/products/account).
Project/workspace and license guidance comes from the
[Web App](https://docs.consentpro.com/web-app/) and
[licenses](https://docs.consentpro.com/web-app/licenses) pages. Recovery controls
must be read from the live official login; no deep recovery URL is assumed.
The [support guide](https://docs.consentpro.com/web-app/troubleshooting),
[expert contact](https://consentpro.com/talk-to-expert) and
[implementation service](https://consentpro.com/implement-for-us) establish public
help routes, not a customer's specific commercial entitlement.

The raw archive and earlier feasibility notes were removed from the current tree
after private preservation and hash verification. Source attribution remains in
the authored guides. The retained template fixture is reviewed, reduced and carries
its upstream license. No internal strategy, roadmap or draft policy was added.
This review does not establish that historical Git objects are suitable for public
release; a clean customer package and a public repository are separate deliverables.

- [Checks](checks/README.md): historical writer reproductions and current regressions.
- [Tests](../../tests/README.md): executable suite and mutation controls.
- [Collector](tools/README.md): bounded public reads and explicit local collection.
- [Installation](../07-agent-installation/README.md): package verification and upgrades.
