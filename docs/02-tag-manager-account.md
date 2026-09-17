# 2. The tag manager account

The second and last thing that cannot be handed to an agent. It takes two minutes.

## Why this one is manual

The Tag Manager API can create containers inside an account that already exists. **It cannot
create the account.** And the interface will not create an empty one either: the Create Account
form demands a container name on the same screen, so account and first container always arrive
together.

The practical consequence, which is worth stating plainly because it shapes what you can
promise: **an agent configures containers, it does not create accounts.** If you are starting
from nothing, you click through this once.

## If you already have an account and a container

Skip to the bottom and collect the two IDs. Nothing here needs redoing.

## Creating it

1. Go to [tagmanager.google.com](https://tagmanager.google.com), signed in as the Google
   account you will authorise in the next step. **The same account.** Authorising as one
   account and creating the container as another is a confusing failure later: the agent
   authenticates fine and then reports that the container does not exist.
2. **Create Account**, top right.
3. **Account Name:** your company, or the client's company. One account usually holds many
   containers.
4. **Country:** where the account is billed or based. It has no effect on consent behaviour.
5. **Container name:** the site's domain, for example `example.com`. Using the domain means
   anyone opening the list later knows which container is which without guessing.
6. **Target platform:** **Web**.
7. **Create**, accept the terms.

## Collect the two IDs

The agent needs both, and they look nothing alike:

| What | Where it is | Looks like |
|---|---|---|
| **Container ID** | top right of the workspace, next to the account name | `GTM-XXXXXXX` |
| **Account ID** | Admin, then Account Settings. Also visible in the URL as the number after `/accounts/` | a long number, such as `1234567890` |

**Copy both somewhere you can paste from.** The scripts take them as arguments, and the account
ID in particular is easy to confuse with the container's internal numeric ID, which is a
different number on the same screen.

## One thing not to do here

**Do not install the container snippet on your site by hand yet, and do not remove anything
yet.** The tag manager offers you the install snippet immediately after creating the container.
If your site already runs the tag manager, that snippet is already there. If it does not, adding
it is part of your site setup and not part of this guide.

What this guide **will** ask you to remove is the `<noscript>` half of that snippet, and that is
step one of the wiring, covered in [reference/nine-steps.md](reference/nine-steps.md).

**Next:** [3. Authorise once](03-authorise.md).
