"""
What it does: authorises Google Tag Manager access through a browser, validates the
callback and granted scopes, then stores a refresh token for the other local scripts.
READS or WRITES: reads the OAuth client JSON, requests Google OAuth permission, and
writes only GTM_OAUTH_TOKEN. It does not configure or publish a GTM container.
How to apply: dry run by default. Use --apply to authorise read access, or
--apply --write for read/edit/publish access with an additional typed confirmation.
Safe to run again? It replaces the local token only after a complete valid grant.
It does not revoke earlier Google grants. To undo access, revoke the app through
myaccount.google.com/permissions; deleting the local file alone does not revoke it.

Write scopes reach every container the Google account can access. Keep read and
write tokens in separate files. An External OAuth app left in Testing may issue
refresh tokens that expire after seven days; see docs/03-authorise.md.

Set GTM_OAUTH_CLIENT to a Desktop app client JSON and GTM_OAUTH_TOKEN to the target
token path. Run: python scripts/authorise.py --apply [--write].
"""

import argparse
import base64
import hashlib
import http.client
import http.server
import json
import os
from pathlib import Path
import secrets
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
PORT = 8765
REDIRECT = "http://127.0.0.1:%d" % PORT

SCOPE_READ = "https://www.googleapis.com/auth/tagmanager.readonly"
SCOPES_WRITE = [
    SCOPE_READ,
    "https://www.googleapis.com/auth/tagmanager.edit.containers",
    "https://www.googleapis.com/auth/tagmanager.edit.containerversions",
    "https://www.googleapis.com/auth/tagmanager.publish",
]


class AuthorisationError(ValueError):
    pass


def pkce_challenge(verifier):
    return base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest()).rstrip(b"=").decode("ascii")


def authorisation_url(client, scopes, state, verifier):
    return AUTH_URL + "?" + urllib.parse.urlencode({
        "client_id": client["client_id"],
        "redirect_uri": REDIRECT,
        "response_type": "code",
        "scope": " ".join(scopes),
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
        "code_challenge": pkce_challenge(verifier),
        "code_challenge_method": "S256",
    })


def callback_handler(expected_state, result):
    class Handler(http.server.BaseHTTPRequestHandler):
        def respond(self, status, message):
            body = ("<!doctype html><html><body><p>" + message + "</p></body></html>").encode()
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if result:
                self.respond(409, "This authorisation attempt has already completed.")
                return
            try:
                parsed = urllib.parse.urlsplit(self.path)
                query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True, max_num_fields=32)
            except ValueError:
                self.respond(400, "Invalid callback.")
                return
            if parsed.path != "/" or parsed.scheme or parsed.netloc:
                self.respond(404, "Not found.")
                return
            states = query.get("state", [])
            if len(states) != 1 or not secrets.compare_digest(states[0].encode(), expected_state.encode()):
                self.respond(400, "Invalid callback state. Return to the original consent screen.")
                return
            codes = query.get("code", [])
            errors = query.get("error", [])
            if len(codes) == 1 and codes[0] and not errors:
                result["code"] = codes[0]
                self.respond(200, "Callback received. Return to the terminal to check authorisation.")
            elif len(errors) == 1 and errors[0] and not codes:
                result["error"] = True
                self.respond(200, "Authorisation was not completed. Return to the terminal.")
            else:
                self.respond(400, "Invalid callback response.")

        def log_message(self, *args):
            pass

    return Handler


class CallbackServer(http.server.HTTPServer):
    def get_request(self):
        connection, address = super().get_request()
        connection.settimeout(5)
        return connection, address


def receive_code(url, state, timeout=300):
    result = {}
    try:
        with CallbackServer(("127.0.0.1", PORT), callback_handler(state, result)) as server:
            deadline = time.monotonic() + timeout
            try:
                opened = webbrowser.open(url)
            except Exception:
                opened = False
            if not opened:
                raise AuthorisationError("The browser could not be opened. Set a default browser and retry.")
            print("Waiting for the callback on %s ..." % REDIRECT)
            while not result:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("Authorisation timed out. Retry from the terminal.")
                server.timeout = min(1, remaining)
                server.handle_request()
            if result.get("error"):
                raise AuthorisationError("Authorisation was refused. The existing token was preserved.")
            return result["code"]
    finally:
        result.clear()


class NoTokenRedirects(urllib.request.HTTPRedirectHandler):
    def http_error_302(self, request, response, code, message, headers):
        response.close()
        raise AuthorisationError("The token endpoint returned an unexpected redirect.")

    http_error_301 = http_error_303 = http_error_307 = http_error_308 = http_error_302


def exchange_code(client, code, verifier):
    fields = {
        "code": code,
        "client_id": client["client_id"],
        "redirect_uri": REDIRECT,
        "grant_type": "authorization_code",
        "code_verifier": verifier,
    }
    if client.get("client_secret"):
        fields["client_secret"] = client["client_secret"]
    request = urllib.request.Request(TOKEN_URL, data=urllib.parse.urlencode(fields).encode())
    opener = urllib.request.build_opener(NoTokenRedirects())
    with opener.open(request, timeout=60) as response:
        return json.load(response)


def validate_grant(token, requested):
    if not isinstance(token, dict):
        raise AuthorisationError("Google returned an invalid token response.")
    granted = token.get("scope")
    if not isinstance(granted, str) or set(granted.split()) != set(requested):
        raise AuthorisationError("Granted scopes do not match the request. The existing token was preserved. "
                         "Retry and grant exactly the requested permissions.")
    refresh = token.get("refresh_token")
    if not isinstance(refresh, str) or not refresh or any(not 33 <= ord(character) <= 126 for character in refresh):
        raise AuthorisationError("Google did not return a valid refresh token. The existing token was preserved. "
                         "Check the app grant at myaccount.google.com/permissions and retry.")
    return refresh, granted.split()


def save_token(path, refresh):
    path = Path(path).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temporary = None
    try:
        descriptor, name = tempfile.mkstemp(prefix=".gtm-token-", dir=path.parent)
        temporary = Path(name)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(refresh + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="open Google authorisation and save a validated token")
    parser.add_argument("--write", action="store_true", help="request edit and publish permission as well as read")
    args = parser.parse_args(argv)
    requested = SCOPES_WRITE if args.write else [SCOPE_READ]
    if not args.apply:
        print("Dry run: no browser, network request or token file write.")
        print("Requested scopes:")
        for scope in requested:
            print("  " + scope)
        print("Use --apply to authorise, with --write only when edit/publish access is required.")
        return 0

    client_file = os.environ.get("GTM_OAUTH_CLIENT")
    token_file = os.environ.get("GTM_OAUTH_TOKEN")
    if not client_file or not token_file:
        raise SystemExit("Set GTM_OAUTH_CLIENT to your client JSON and GTM_OAUTH_TOKEN to the token path.")
    if args.write:
        print("Write and publish scopes cover every container this Google account can access.")
        print("Keep this token in a different file from your read-only token.")
        if input("Type 'write' to continue: ").strip() != "write":
            raise SystemExit("Stopped. Nothing was authorised.")
    try:
        with open(os.path.expanduser(client_file), encoding="utf-8") as handle:
            data = json.load(handle)
        client = data.get("installed") if isinstance(data, dict) else None
        if not isinstance(client, dict) or not client.get("client_id"):
            raise AuthorisationError("Use a Desktop app OAuth client JSON from the Google Cloud console.")
        state = secrets.token_urlsafe(32)
        verifier = secrets.token_urlsafe(64)
        url = authorisation_url(client, requested, state, verifier)
        print("Opening the Google consent screen in your browser.")
        code = receive_code(url, state)
        token = exchange_code(client, code, verifier)
        refresh, granted = validate_grant(token, requested)
        save_token(token_file, refresh)
    except AuthorisationError as error:
        raise SystemExit(str(error)) from None
    except (OSError, ValueError, http.client.HTTPException):
        raise SystemExit("Authorisation could not complete. The existing token was preserved. "
                         "Check the client file, local port and network connection, then retry.") from None

    print("Token written to %s" % os.path.expanduser(token_file))
    print("All requested scopes granted:")
    for scope in granted:
        print("  " + scope)
    print("External OAuth apps in Testing may issue refresh tokens that expire after seven days.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
