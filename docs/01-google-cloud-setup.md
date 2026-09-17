# 1. Google Cloud, once

This is the longest part and you do it once per Google account, not once per site. Everything
here happens at [console.cloud.google.com](https://console.cloud.google.com). Budget fifteen
minutes the first time.

**Nothing in this document touches your website or your tag manager.** It only creates the
permission an agent will later use.

---

## 1.0 What you are actually setting up

Skip this if you have used the Google Cloud console before. If you have not, ten minutes here
saves an hour of clicking around wondering what any of it means.

### The console is the back door to products you already use

Google Tag Manager, Analytics, Ads, Search Console, Sheets, Drive and Calendar all have a
website you log into. **Every one of them also has an API**, which is the same product with the
buttons removed: the thing a program talks to instead of a person clicking.

The Google Cloud console is where you say who is allowed through that door. It is not a
separate product you are signing up for and it does not change anything about the accounts you
already have. **Your tag manager does not know or care that this exists.** You are issuing a
key, not modifying a lock.

### A project is a folder for permissions

Everything in the console lives inside a **project**. A project is not a piece of software; it
is a container that holds three things: which APIs are switched on, which credentials exist,
and who can use them.

You make one project and it can serve many sites. The reason to make a second one is
separation: a project for your own work and a project per client keeps their access from
depending on yours, and lets you hand one over or shut it down without touching the rest.

### Enabling an API is a switch, not an installation

A new project starts with **every** Google API switched off, deliberately. "Enable the Tag
Manager API" means flipping one switch in a list of hundreds. Nothing is installed, nothing is
downloaded, and nothing costs money at this scale.

**What the switch actually controls** is whether your project is allowed to make that kind of
call at all. With it off, a perfectly valid credential gets refused, and the error message
talks about permissions rather than saying the API is off. That single confusion is why this
step gets its own section below.

### What this opens, and it is bigger than one setup

This is the part worth understanding, because the work you do once here is reusable far beyond
this guide.

Once a project exists and a credential is authorised, **an agent can reach any Google API you
enable in that same project**, using the same credential pattern. The tag manager today.
Search Console next week to pull the queries a site ranks for. The Analytics Data API to build
a report nobody has to export by hand. Sheets to write results somewhere a colleague can read.

Each one is the same three moves: enable the API, add its scope to the authorisation, run
something. **The fifteen minutes in this document is the only part that is not repeatable.**

> ### ⛔ Which is exactly why the permissions deserve attention
>
> The same property that makes this useful makes it dangerous when it is careless.
>
> **Scopes are per API, and they are not per account.** Authorise write access to Tag Manager
> and the agent can write to **every tag manager container that Google account can reach**.
> Not the one you had in mind. Every one, including other clients and unrelated production
> properties. Google offers no way to narrow a token to a single container.
>
> Three habits follow, and they are cheap:
>
> 1. **Ask for the narrowest scope that works.** Read-only for anything that only inspects.
> 2. **Keep read and write in separate credentials**, so revoking one does not kill the other.
> 3. **Use the Google account that has the least access.** If a colleague's account can see
>    forty client containers and yours can see four, authorise from yours.
>
> Revoking is always available and immediate, at
> [myaccount.google.com/permissions](https://myaccount.google.com/permissions). Knowing where
> that page is matters more than most of this document.

---

## 1.1 Create a project

1. Open [console.cloud.google.com](https://console.cloud.google.com).
2. At the top left, next to the **Google Cloud** logo, there is a **project selector**. It
   shows either "Select a project" or the name of a project you used before. Click it.
3. In the dialog, click **New project** at the top right.
4. **Project name:** anything. `consent-pro-gtm` is a reasonable choice.
5. **Location:** this is the field that matters, and it is easy to click past.
   - If your company has Google Workspace, the selector offers your organisation, for
     example `yourcompany.com`. **Choose it.**
   - If it says **No organisation**, you are creating a personal project. That still works,
     and it costs you something in step 1.3. Read the box there before deciding.
6. Click **Create**. It takes a few seconds, then a notification appears. **Make sure the
   project selector at the top now shows your new project**, because the console often leaves
   you in the previous one and every later step would then apply to the wrong project.

---

## 1.2 Enable the Tag Manager API

A new project has every API switched off.

1. Left menu, **APIs & Services**, then **Library**. If the left menu is hidden, the hamburger
   icon at the very top left opens it.
2. In the search box, type `Tag Manager API`.
3. Click the result named exactly **Tag Manager API**. Do not pick Tag Manager for a different
   product.
4. Click **Enable**. The page turns into the API's dashboard when it is done.

> **Skipping this produces a misleading error.** Calls fail with a message about permissions,
> which reads like a credential problem. The credential is fine; the API is off.

---

## 1.3 Configure the OAuth consent screen

This comes **before** creating the credential, because Google will not let you create one
without it. It is also where you make the single decision that causes most of the confusion
later.

1. **APIs & Services**, then **OAuth consent screen**.
2. Google asks for the **User type**. This is the decision:

| Choice | When it is available | What it costs you |
|---|---|---|
| **Internal** | only when the project belongs to a Google Workspace organisation | nothing. Tokens do not expire on a schedule, and no verification is needed |
| **External** | always | **while the app stays in Testing, refresh tokens expire after seven days** |

> ### ⛔ Choose Internal if it is offered
>
> **This is the decision, and putting it off is what makes it painful.** An External app left
> in **Testing** expires its refresh token after **seven days**. Everything works, you forget
> about it, and about a week later the agent fails with a credential error that looks like
> something broke. Nothing broke. The token expired.
>
> **If Internal is greyed out**, your project has no organisation. Two options, in order of
> preference:
>
> 1. Go back to step 1.1 and recreate the project inside your organisation, if you have one.
> 2. Stay on External and accept one of these: re-run the authorisation weekly, or move the
>    app from **Testing** to **In production** using the **Publish app** button on this same
>    screen. Publishing an app that requests sensitive scopes can trigger Google's verification
>    process, which takes time. For an internal tool used by a handful of people, the weekly
>    re-run is usually less friction.
>
> Whatever you choose, **write it down now**. In a week nobody remembers which it was, and the
> symptom gives no clue.

3. Click **Create**, then fill the **App information** page:
   - **App name:** what you will see on the consent screen. `Consent Pro GTM agent` is clear.
   - **User support email:** pick your own address from the dropdown.
   - **Developer contact information:** your email again, at the bottom of the form.
   - Everything else on this page is optional. Leave it.
4. **Save and continue.**
5. The **Scopes** page appears. **Click Save and continue without adding anything.** The
   scripts request the scopes they need at authorisation time, and adding them here as well
   only creates a second place to keep in sync.
6. On **Test users**, if you chose External: click **Add users** and add the Google account
   you will authorise with. **An External app in Testing refuses any account not on this
   list**, with an error that says the app is blocked. Add yourself even though it seems
   redundant.
7. **Save and continue**, then review and go back to the dashboard.

---

## 1.4 Create the OAuth client

1. **APIs & Services**, then **Credentials**.
2. **Create credentials** at the top, then **OAuth client ID**.
3. **Application type:** choose **Desktop app**.
   - Not Web application. Desktop app is what allows the loopback redirect the authorisation
     script uses, and picking Web application leads to a redirect URI mismatch that is
     tedious to diagnose.
4. **Name:** something you will recognise in a list, such as `consent-pro-gtm-agent`.
5. Click **Create**.

> **Use a client dedicated to this.** If you reuse an OAuth client that other tooling depends
> on, revoking this agent's access later also revokes everything else that client does. A
> separate client costs nothing and keeps the two independent.

---

## 1.5 Download the JSON, and put it somewhere safe

1. The dialog that appears after **Create** shows the client ID and the client secret. Click
   **Download JSON**.
2. **The file lands in your Downloads folder with a long automatic name**, of the form:

   ```
   client_secret_123456789012-abcdefghijklmnop.apps.googleusercontent.com.json
   ```

3. **Move it out of Downloads and out of any project folder**, into somewhere meant for
   credentials:

   ```bash
   mkdir -p ~/.config/gcloud
   mv ~/Downloads/client_secret_*.apps.googleusercontent.com.json \
      ~/.config/gcloud/consent-pro-gtm-client.json
   chmod 600 ~/.config/gcloud/consent-pro-gtm-client.json
   ```

> ### ⚠️ That filename has caught people out
>
> The name Google gives the file starts with `client_secret`, which is not the pattern most
> `.gitignore` files are written to catch. A `.gitignore` covering `*oauth*.json` or
> `credentials.json` will happily let `client_secret_….json` through.
>
> **The `.gitignore` in this repository covers it.** If you are working in a different
> repository, check yours before the file goes anywhere near it. Better still, keep the file
> outside every project directory, which is what the commands above do.

4. Tell the scripts where it is, and where the token should go:

   ```bash
   export GTM_OAUTH_CLIENT=~/.config/gcloud/consent-pro-gtm-client.json
   export GTM_OAUTH_TOKEN=~/.config/gcloud/consent-pro-gtm-token.txt
   ```

   Put those two lines in your shell profile so they survive a new terminal. There is a
   `.env.example` in this repository showing the same thing.

---

## What you should have now

| Item | Where it is |
|---|---|
| A Google Cloud project | with the Tag Manager API enabled |
| An OAuth consent screen | Internal, or External with your account as a test user |
| A Desktop app OAuth client | downloaded as JSON |
| The JSON | outside any project folder, with `GTM_OAUTH_CLIENT` pointing at it |
| An empty token path | `GTM_OAUTH_TOKEN`, which the next step fills |

**Next:** [2. The tag manager account](02-tag-manager-account.md), which is the other thing
that cannot be automated.
