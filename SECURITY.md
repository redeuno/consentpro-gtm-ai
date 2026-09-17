# Security

This repository holds scripts that you will point at a credential reaching your production
properties. That deserves a page rather than a footnote.

## Read the scripts before you run them

There are three, they are short, and they use only the Python standard library so there is no
dependency tree to audit. Reading them takes about ten minutes and you do it once.

**This applies to any repository that asks for a credential, not just this one.** If a project
discourages you from reading its code, that is the finding.

## What the credential actually reaches

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
| Writes are not retried on server errors, because the result is undefined and retrying can duplicate | all three |
| There is no write path at all in the audit script | `audit-container.py` |

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
- **Store or transmit anything.** Everything runs locally against Google's API. There is no
  telemetry, no analytics and no external endpoint other than Google and the public Consent Pro
  documentation, which is where the tag manager template is downloaded from.

## Reporting something

Open an issue for anything that is not itself a vulnerability. For a security problem, contact
the maintainer directly rather than filing publicly.

## One thing to check before you trust any copy of this

A public repository can be forked, renamed and modified. **Confirm you are on the address you
were given by a source you trust**, rather than one you found in a search result or a comment.
This applies to every repository that asks for a credential, and it is the reason the scripts
here are kept short enough to read.
