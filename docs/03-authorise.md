# 3. Authorise once

**For the local GTM scripts only.** MCP onboarding uses its own connector authentication;
it does not require this custom Google OAuth client. The manual
[Gallery path](reference/nine-steps.md#2-add-the-consent-pro-template-from-the-gallery) does not
use this script or a custom OAuth client JSON. For the scripts, browser authorisation lets
the agent renew access while the refresh token remains valid; Testing mode or revocation can
require authorisation again.

## What is about to happen

`authorise.py` simulates by default. With `--apply`, it opens a Google consent screen,
validates the callback and returned scopes, and saves a **refresh token** to `GTM_OAUTH_TOKEN`.
It starts the local callback listener before opening the browser and closes it on success,
refusal or timeout. Invalid or mismatched responses preserve an existing token file.

A refresh token is a long-lived credential. It is not a password and it cannot be used to log
in as you, but it does let a program act on your behalf within the scopes you approved, until
you revoke it. Treat the file like a password anyway.

## Check the two variables first

```bash
echo $GTM_OAUTH_CLIENT   # should print the path to the json you downloaded
echo $GTM_OAUTH_TOKEN    # should print where the token will be written
```

If either is empty, go back to [1.5](01-google-cloud-setup.md).

## Read only, or read and write

Run one of these. They differ in what the consent screen asks for.

```bash
python scripts/authorise.py                  # show the plan; no browser or token write
python scripts/authorise.py --apply          # authorise read only
python scripts/authorise.py --apply --write  # authorise read, edit and publish
```

**Start with read only for inspection.** The audit needs no write scope. Protect the token
and the data it can read; a read-only grant does not make account data public.

**`--write` prints a warning and makes you type a word to continue.** That is deliberate:

> Write access covers **every container the Google account can reach**, including other clients
> and unrelated production properties. Google offers no per-container scope. If the account you
> are about to authorise has access to forty containers, this token reaches forty containers.

**Keep the two in separate files.** Use different `GTM_OAUTH_TOKEN` paths. Reauthorising does
not prove the previous token was revoked. Review grants at
[Google account permissions](https://myaccount.google.com/permissions) when revoking access;
separate local files do not guarantee independent provider-side revocation.

## What you will see

1. A browser opens on `accounts.google.com`.
2. You pick the Google account. **Pick the one that owns the tag manager account from step 2.**
3. Google may show "Google hasn't verified this app". That is expected for an app in Testing.
   **Advanced**, then **Go to (your app name)**.
4. Review the permissions for the chosen mode. Continue only if you intend to grant them.
   The script rejects incomplete or broader returned scopes before replacing a token.
5. The tab says you can close it. The terminal prints where the token went and which scopes
   were granted.

## When it does not work

| What you see | What it is |
|---|---|
| **Access blocked: app has not completed verification** | your account is not in the test user list. [1.3](01-google-cloud-setup.md), step 6 |
| **redirect_uri_mismatch** | the OAuth client is a Web application, not a Desktop app. [1.4](01-google-cloud-setup.md) |
| The script says Google returned no refresh token | that account already granted these scopes before. Revoke at [myaccount.google.com/permissions](https://myaccount.google.com/permissions) and run it again |
| Local callback cannot start | check whether another process owns loopback port 8765 before retrying |
| The default browser cannot open | configure a working default browser and retry; no OAuth link is printed for manual copying |
| Refusal, timeout or invalid returned scopes | the listener closes and an existing token is preserved; inspect the reported reason before retrying |
| It worked, then failed about a week later | the seven day expiry of an External app in Testing. [1.3](01-google-cloud-setup.md) |

## Confirm it, without changing anything

```bash
python scripts/audit-container.py --account YOUR_ACCOUNT_ID --container GTM-XXXXXXX
```

It prints the account name and asks you to confirm it before doing anything else. **If the name
is not what you expected, stop and check the ID.** That prompt exists because an account ID is
easy to mistype and impossible to sanity check by eye, and the credential reaches more than
one account.

**Next:** [4. Hand it to the agent](04-run-it.md).
