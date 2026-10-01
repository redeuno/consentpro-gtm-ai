# Security

This repository holds scripts that you will point at a credential reaching your production
properties. That deserves a page rather than a footnote.

## Read the scripts before you run them

The scripts and their shared `consent-template.py` helper use only the Python standard
library. Read the code that will receive your credential before authorising it.

**This applies to any repository that asks for a credential, not just this one.** If a project
discourages you from reading its code, that is the finding.

## What the credential actually reaches

This credential is needed for **API automation**. Adding the template through the GTM
interface needs a Google login with container access, but no OAuth client JSON created for
this repository. See the [manual path](docs/reference/nine-steps.md).

**A Tag Manager write scope covers every container that Google account can access.** Not the
one you had in mind. Every one, including other clients and unrelated production properties.
Google offers no way to narrow a token to a single container, so the narrowing has to come from
how you set it up:

1. **Authorise from the account with the least access.** If a colleague's login can see forty
   client containers and yours can see four, use yours.
2. **Keep read and write in separate token files.** Then revoking write does not break your
   read-only tooling.
3. **Use an OAuth client dedicated to this.** Sharing one with other tooling means revoking
   here revokes there.
4. **Ask for read-only unless you are configuring.** The audit script needs nothing more.

**Revoke at any time** at [myaccount.google.com/permissions](https://myaccount.google.com/permissions).
It is immediate.

## What the scripts refuse to do

These are enforced in code, not suggested in documentation:

| Guard | Where |
|---|---|
| The account must be confirmed by its **live name**, not just its id | `audit-container.py`, `wire-consent.py` |
| Nothing is written without `--apply` | `wire-consent.py` |
| Nothing is published without a **second** flag, `--publish` | `wire-consent.py` |
| A version is not created when any tag failed to update, because a version made of half-applied state reads as complete in the history | `wire-consent.py` |
| A compile error stops the run loudly instead of printing an empty version id | `wire-consent.py` |
| Writes are not retried on server errors, because the result is undefined and retrying can duplicate | API scripts |
| There is no write path at all in the audit script | `audit-container.py` |
| New templates come from `finsweet/gtm-template-consent-pro` at a pinned Gallery SHA | `wire-consent.py`, `consent-template.py` |
| Unrecognised or modified template identity stops configuration before writes | `wire-consent.py`, `consent-template.py` |

The pinned version is `8a551897e5bfdecf03de59fa00058be442b7ac29`. The
[Gallery import API](https://developers.google.com/tag-platform/tag-manager/api/reference/rest/v2/accounts.containers.workspaces.templates/import_from_gallery)
requires acknowledgement of template permissions. Review the
[publisher's template](https://github.com/finsweet/gtm-template-consent-pro/blob/8a551897e5bfdecf03de59fa00058be442b7ac29/template.tpl)
before approving `--apply`; that approval includes the template import and its permissions.
The script does not choose the latest Gallery release automatically.

Recognised existing templates keep their IDs and source. A recognised manual import is not
converted to a Gallery installation, and its publisher/version are not proven by its name.
Read the audit's `template_identity` and any blocking reason before continuing. Those checks
describe template identity and configuration, not runtime behaviour or certification.

**Why the account guard checks the name and not just the id.** An id is easy to mistype and
impossible to check by eye. A name check alone would be worse, because names are mutable and
because a list of forbidden names defaults to permitting, which is the wrong default for a
token that reaches production. Confirming the live name of an explicitly given id catches the
typo without pretending to be an allowlist.

## The category map defaults to over-blocking, on purpose

`--scaffold` writes every tag as `marketing`, the strictest category. It is not a guess about
your tags.

Someone who applies that file without reading gets trackers blocked that should not be, which
they notice within minutes and fix. The opposite default, `essential`, would mean every tracker
firing without consent while every screen looks correct. **A safe default is the one whose
failure is visible.**

## Things this repository will not do

- **Decide whether a tracker is essential.** Legal and product judgement about a specific site.
- **Assert that a site is compliant.** The scripts configure a container and can prove what
  they configured. That is one input to a judgement, not the judgement.
- **Send telemetry.** The scripts run locally. The API scripts call Google for authorisation
  and container operations; `inspect-site.py` reads the public site URL you supply. The
  Gallery API imports new templates from the pinned publisher
  repository. The scripts no longer fetch a template download from the Consent Pro docs.
  OAuth tokens and optional reports are stored locally at the paths you choose.

## Reporting something

Open an issue for anything that is not itself a vulnerability. For a security problem, contact
the maintainer directly rather than filing publicly.

## One thing to check before you trust any copy of this

A public repository can be forked, renamed and modified. **Confirm you are on the address you
were given by a source you trust**, rather than one you found in a search result or a comment.
This applies to every repository that asks for a credential, and it is the reason the scripts
here are kept short enough to read.
