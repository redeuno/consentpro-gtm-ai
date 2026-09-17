"""
What it does: the one-time browser authorisation. Opens a Google consent screen, catches the
          response on a local port, exchanges it for a refresh token and writes that token to
          disk. Run once per machine; after this the other scripts renew access on their own.
READS or WRITES: writes ONE file, the refresh token, to the path in GTM_OAUTH_TOKEN. It does
          not touch Google Tag Manager at all. It only obtains permission.
How to apply: there is nothing to apply. Running it IS the action, and it is the only script
          here that requires a human at a browser.
Safe to run again? Yes, and re-running is the fix when a token expires. It overwrites the
          token file with a fresh one. The old token stops working.

⛔ READ THIS BEFORE CHOOSING A SCOPE:
   --write asks for permission to create and publish in Google Tag Manager. That permission
   covers EVERY container the Google account can reach, including other clients and unrelated
   production properties. There is no per-container scope. Keep the read token and the write
   token in SEPARATE files, so revoking one does not kill the other.

⚠️ THE SEVEN DAY DEADLINE, and it catches people weeks later:
   if the OAuth consent screen is set to External and left in Testing, Google expires the
   refresh token after seven days. Scripts then fail with a credential error that looks like
   something broke. Two fixes: set the consent screen to Internal, available when the project
   belongs to an organisation, or publish the app. Decide at setup, not in a week.

Setup, once:
   export GTM_OAUTH_CLIENT=~/.config/gcloud/your-oauth-client.json
   export GTM_OAUTH_TOKEN=~/.config/gcloud/gtm-refresh-token.txt
   python authorise.py            # read only
   python authorise.py --write    # read and write
"""

import argparse
import http.server
import json
import os
import sys
import urllib.parse
import urllib.request
import webbrowser

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
PORT = 8765
REDIRECT = "http://localhost:%d" % PORT

SCOPE_READ = "https://www.googleapis.com/auth/tagmanager.readonly"
SCOPES_WRITE = [
    "https://www.googleapis.com/auth/tagmanager.readonly",
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
    "https://www.googleapis.com/auth/tagmanager.publish",
]

CLIENT_FILE = os.environ.get("GTM_OAUTH_CLIENT")
TOKEN_FILE = os.environ.get("GTM_OAUTH_TOKEN")

_code = {}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        _code["code"] = (q.get("code") or [None])[0]
        _code["error"] = (q.get("error") or [None])[0]
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        done = "You can close this tab and return to the terminal."
        bad = "Authorisation was refused. Close this tab and check the terminal."
        self.wfile.write(("<html><body style='font-family:system-ui;padding:40px'><p>%s</p>"
                          "</body></html>" % (bad if _code["error"] else done)).encode())

    def log_message(self, *a):
        pass


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--write", action="store_true",
                   help="ask for write and publish permission, not just read")
    a = p.parse_args()

    if not CLIENT_FILE or not TOKEN_FILE:
        raise SystemExit(
            "Set GTM_OAUTH_CLIENT to your OAuth client json and GTM_OAUTH_TOKEN to the file "
            "where the refresh token should be written.")

    scopes = " ".join(SCOPES_WRITE) if a.write else SCOPE_READ

    if a.write:
        print("\n⛔ You are about to authorise WRITE and PUBLISH access to Google Tag Manager.")
        print("   This covers every container this Google account can reach, including any")
        print("   production property and any other client. There is no per-container scope.")
        print("   Keep this token in a different file from your read-only one.\n")
        if input("   Type 'write' to continue: ").strip() != "write":
            raise SystemExit("   Stopped. Nothing was authorised.")

    with open(CLIENT_FILE, encoding="utf-8") as f:
        data = json.load(f)
    cli = data.get("installed") or data.get("web")
    if not cli:
        raise SystemExit("That json has neither an 'installed' nor a 'web' client. Create a "
                         "Desktop app credential in the Google Cloud console.")

    url = AUTH_URL + "?" + urllib.parse.urlencode({
        "client_id": cli["client_id"],
        "redirect_uri": REDIRECT,
        "response_type": "code",
        "scope": scopes,
        "access_type": "offline",
        "prompt": "consent",
    })

    print("\nOpening the consent screen in your browser.")
    print("If it does not open, paste this into a browser yourself:\n\n  %s\n" % url)
    try:
        webbrowser.open(url)
    except Exception:
        pass

    srv = http.server.HTTPServer(("localhost", PORT), Handler)
    srv.timeout = 300
    print("Waiting for the response on %s ..." % REDIRECT)
    srv.handle_request()

    if _code.get("error"):
        raise SystemExit("Google returned: %s" % _code["error"])
    if not _code.get("code"):
        raise SystemExit("No code came back. The browser may have timed out; run it again.")

    body = urllib.parse.urlencode({
        "code": _code["code"],
        "client_id": cli["client_id"],
        "client_secret": cli["client_secret"],
        "redirect_uri": REDIRECT,
        "grant_type": "authorization_code",
    }).encode()
    with urllib.request.urlopen(urllib.request.Request(TOKEN_URL, data=body), timeout=60) as r:
        tok = json.load(r)

    refresh = tok.get("refresh_token")
    if not refresh:
        raise SystemExit(
            "Google did not return a refresh token. This usually means the account had already "
            "granted these scopes. Revoke the app at myaccount.google.com/permissions and run "
            "this again.")

    path = os.path.expanduser(TOKEN_FILE)
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(refresh + "\n")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass

    granted = (tok.get("scope") or "").split()
    print("\nToken written to %s" % path)
    print("Scopes granted:")
    for s in granted:
        print("   %s" % s)

    asked = scopes.split()
    missing = [s for s in asked if s not in granted]
    if missing:
        print("\n⚠️ You asked for scopes that were not granted. The consent screen lets people")
        print("   uncheck individual permissions, and a missing one fails later as a")
        print("   confusing error. Missing:")
        for s in missing:
            print("   %s" % s)
        print("   Run this again and accept all of them.")
    else:
        print("\nAll requested scopes granted.")

    print("\n⚠️ If your OAuth consent screen is External and in Testing, this token expires in")
    print("   seven days. Set it to Internal, or publish the app, to remove that deadline.")


if __name__ == "__main__":
    sys.exit(main())
