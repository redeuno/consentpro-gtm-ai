# 3. Authorise once

The last step with a human in it. After this the agent renews its own access and you do not
return to a browser.

## What is about to happen

`authorise.py` opens a Google consent screen, catches the answer on a local port, exchanges it
for a **refresh token**, and writes that token to the path in `GTM_OAUTH_TOKEN`.

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
python scripts/authorise.py            # read only
python scripts/authorise.py --write    # read, edit and publish
```

**Start with read only if you only want to inspect a container.** The audit script needs
nothing more, and a read-only token cannot damage anything no matter what an agent decides to
do with it.

**`--write` prints a warning and makes you type a word to continue.** That is deliberate:

> Write access covers **every container the Google account can reach**, including other clients
> and unrelated production properties. Google offers no per-container scope. If the account you
> are about to authorise has access to forty containers, this token reaches forty containers.

**Keep the two in separate files.** Different values for `GTM_OAUTH_TOKEN`, run the script
twice. Then revoking write access later does not also break your read-only tooling.

## What you will see

1. A browser opens on `accounts.google.com`.
2. You pick the Google account. **Pick the one that owns the tag manager account from step 2.**
3. Google may show "Google hasn't verified this app". That is expected for an app in Testing.
   **Advanced**, then **Go to (your app name)**.
4. The permission list appears. **Accept all of them.** The screen lets you untick individual
   permissions, and a missing one fails later as a confusing error rather than an obvious one.
   The script checks what was actually granted and tells you if something is missing.
5. The tab says you can close it. The terminal prints where the token went and which scopes
   were granted.

## When it does not work

| What you see | What it is |
|---|---|
| **Access blocked: app has not completed verification** | your account is not in the test user list. [1.3](01-google-cloud-setup.md), step 6 |
| **redirect_uri_mismatch** | the OAuth client is a Web application, not a Desktop app. [1.4](01-google-cloud-setup.md) |
| The script says Google returned no refresh token | that account already granted these scopes before. Revoke at [myaccount.google.com/permissions](https://myaccount.google.com/permissions) and run it again |
| Browser opens, nothing comes back | something else is on port 8765. Close it and retry |
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
