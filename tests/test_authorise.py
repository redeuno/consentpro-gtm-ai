"""Offline OAuth tests. No real credentials, browser, sockets or Google requests."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import stat
import tempfile
import unittest
from unittest import mock
import urllib.parse


SPEC = importlib.util.spec_from_file_location("authorise", Path(__file__).resolve().parents[1] / "scripts/authorise.py")
AUTHORISE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUTHORISE)


def callback(handler_type, path):
    handler = handler_type.__new__(handler_type)
    handler.path = path
    handler.wfile = io.BytesIO()
    statuses = []
    handler.send_response = statuses.append
    handler.send_header = lambda *args: None
    handler.end_headers = lambda: None
    handler.do_GET()
    return statuses[0], handler.wfile.getvalue().decode()


class OAuthTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="consent-oauth-test-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.client = self.root / "client.json"
        self.target = self.root / "token.txt"
        self.client.write_text(json.dumps({"installed": {
            "client_id": "test-client", "client_secret": "test-client-secret"}}))
        self.environment = mock.patch.dict(os.environ, {
            "GTM_OAUTH_CLIENT": str(self.client), "GTM_OAUTH_TOKEN": str(self.target)})
        self.environment.start()
        self.addCleanup(self.environment.stop)
        self.network = mock.patch.object(socket, "socket", side_effect=AssertionError("Real sockets are forbidden"))
        self.network.start()
        self.addCleanup(self.network.stop)

    def run_main(self, token, args=None):
        output = io.StringIO()
        with mock.patch.object(AUTHORISE, "receive_code", return_value="test-code"), \
                mock.patch.object(AUTHORISE, "exchange_code", return_value=token), \
                mock.patch("builtins.input", return_value="write"), \
                contextlib.redirect_stdout(output):
            try:
                result = AUTHORISE.main(args or ["--apply"])
            except SystemExit as error:
                return error, output.getvalue()
        return result, output.getvalue()

    def test_default_is_dry_run_even_with_write_flag(self):
        with mock.patch.object(AUTHORISE, "receive_code") as receive, \
                mock.patch.object(AUTHORISE, "exchange_code") as exchange, \
                mock.patch.object(AUTHORISE, "save_token") as save, \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(AUTHORISE.main(["--write"]), 0)
        receive.assert_not_called()
        exchange.assert_not_called()
        save.assert_not_called()
        self.assertFalse(self.target.exists())

    def test_pkce_matches_rfc_vector_and_authorisation_binds_state(self):
        verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
        self.assertEqual(AUTHORISE.pkce_challenge(verifier), "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM")
        url = AUTHORISE.authorisation_url({"client_id": "test-client"}, [AUTHORISE.SCOPE_READ], "test-state", verifier)
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
        self.assertEqual(query["state"], ["test-state"])
        self.assertEqual(query["code_challenge_method"], ["S256"])
        self.assertEqual(query["code_challenge"], [AUTHORISE.pkce_challenge(verifier)])
        self.assertNotIn(verifier, url)

    def test_callback_rejects_unrelated_or_invalid_requests(self):
        invalid = ["/favicon.ico", "/?code=test-code", "/?state=wrong&code=test-code",
                   "/?state=test-state&state=test-state&code=test-code",
                   "/?state=test-state&code=one&code=two", "/?state=test-state&code=",
                   "/?state=test-state&code=test-code&error=access_denied",
                   "/?state=%E2%98%83&code=test-code"]
        for path in invalid:
            with self.subTest(path=path):
                result = {}
                status, body = callback(AUTHORISE.callback_handler("test-state", result), path)
                self.assertIn(status, (400, 404))
                self.assertEqual(result, {})
                self.assertNotIn("test-code", body)

    def test_callback_accepts_one_matching_response_without_echoing_secrets(self):
        result = {}
        handler = AUTHORISE.callback_handler("test-state", result)
        status, body = callback(handler, "/?state=test-state&code=test-code")
        self.assertEqual(status, 200)
        self.assertEqual(result, {"code": "test-code"})
        self.assertNotIn("test-code", body)
        self.assertNotIn("test-state", body)
        self.assertEqual(callback(handler, "/?state=test-state&code=second")[0], 409)
        self.assertEqual(result, {"code": "test-code"})

    def server_factory(self, paths, events):
        class FakeServer:
            def __init__(self, address, handler):
                self.handler = handler
                self.paths = list(paths)
                self.address = address
                self.closed = False
                events.append("bound")

            def __enter__(self):
                return self

            def __exit__(self, *args):
                self.closed = True
                events.append("closed")

            def handle_request(self):
                callback(self.handler, self.paths.pop(0))

        return FakeServer

    def test_listener_starts_before_browser_and_ignores_unrelated_gets(self):
        events = []
        factory = self.server_factory(["/favicon.ico", "/?state=wrong&code=bad",
                                       "/?state=test-state&code=test-code"], events)
        with mock.patch.object(AUTHORISE, "CallbackServer", factory), \
                mock.patch.object(AUTHORISE.webbrowser, "open", side_effect=lambda url: events.append("browser") or True), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(AUTHORISE.receive_code("https://example.invalid", "test-state"), "test-code")
        self.assertEqual(events, ["bound", "browser", "closed"])

    def test_listener_closes_on_denial_timeout_and_browser_failure(self):
        cases = [(["/?state=test-state&error=access_denied"], True, [0, 1], ValueError),
                 ([], True, [0, 301], TimeoutError), ([], False, [0], ValueError)]
        for paths, opened, clock, error_type in cases:
            with self.subTest(opened=opened, paths=paths):
                events = []
                with mock.patch.object(AUTHORISE, "CallbackServer", self.server_factory(paths, events)), \
                        mock.patch.object(AUTHORISE.webbrowser, "open", return_value=opened), \
                        mock.patch.object(AUTHORISE.time, "monotonic", side_effect=clock), \
                        contextlib.redirect_stdout(io.StringIO()):
                    with self.assertRaises(error_type):
                        AUTHORISE.receive_code("https://example.invalid", "test-state")
                self.assertEqual(events[-1], "closed")

    def test_binding_failure_never_opens_browser(self):
        with mock.patch.object(AUTHORISE, "CallbackServer", side_effect=OSError("occupied")), \
                mock.patch.object(AUTHORISE.webbrowser, "open") as browser:
            with self.assertRaises(OSError):
                AUTHORISE.receive_code("https://example.invalid", "test-state")
        browser.assert_not_called()

    def test_exchange_sends_matching_verifier_to_only_the_token_endpoint(self):
        reply = io.BytesIO(json.dumps({"refresh_token": "test-refresh-token"}).encode())
        opener = mock.Mock()
        opener.open.return_value = reply
        with mock.patch.object(AUTHORISE.urllib.request, "build_opener", return_value=opener):
            AUTHORISE.exchange_code({"client_id": "test-client", "client_secret": "test-client-secret"},
                                    "test-code", "test-verifier")
        request = opener.open.call_args.args[0]
        fields = urllib.parse.parse_qs(request.data.decode())
        self.assertEqual(request.full_url, AUTHORISE.TOKEN_URL)
        self.assertEqual(fields["code_verifier"], ["test-verifier"])
        self.assertEqual(fields["code"], ["test-code"])
        self.assertEqual(fields["redirect_uri"], [AUTHORISE.REDIRECT])

    def test_success_replaces_token_privately_without_logging_secrets(self):
        self.target.write_text("previous-token\n")
        os.chmod(self.target, 0o644)
        result, output = self.run_main({"scope": AUTHORISE.SCOPE_READ, "refresh_token": "test-refresh-token"})
        self.assertEqual(result, 0)
        self.assertEqual(self.target.read_text(), "test-refresh-token\n")
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(self.target.stat().st_mode), 0o600)
        for secret in ("test-refresh-token", "test-code", "test-client-secret"):
            self.assertNotIn(secret, output)

    def test_each_attempt_has_fresh_bound_state_and_verifier_without_logging_them(self):
        attempts = []
        for _ in range(2):
            output = io.StringIO()
            token = {"scope": AUTHORISE.SCOPE_READ, "refresh_token": "test-refresh-token"}
            with mock.patch.object(AUTHORISE, "receive_code", return_value="test-code") as receive, \
                    mock.patch.object(AUTHORISE, "exchange_code", return_value=token) as exchange, \
                    mock.patch.object(AUTHORISE, "save_token"), contextlib.redirect_stdout(output):
                self.assertEqual(AUTHORISE.main(["--apply"]), 0)
            url, state = receive.call_args.args
            verifier = exchange.call_args.args[2]
            query = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
            self.assertEqual(query["state"], [state])
            self.assertEqual(query["code_challenge"], [AUTHORISE.pkce_challenge(verifier)])
            self.assertTrue(43 <= len(verifier) <= 128)
            for value in (url, state, verifier):
                self.assertNotIn(value, output.getvalue())
            attempts.append((state, verifier))
        self.assertNotEqual(attempts[0][0], attempts[1][0])
        self.assertNotEqual(attempts[0][1], attempts[1][1])

    def test_unexpected_error_text_cannot_leak_into_cli_output(self):
        self.target.write_text("previous-token\n")
        output = io.StringIO()
        with mock.patch.object(AUTHORISE, "receive_code", side_effect=ValueError("test-secret-error")), \
                contextlib.redirect_stdout(output), self.assertRaises(SystemExit) as stopped:
            AUTHORISE.main(["--apply"])
        self.assertNotIn("test-secret-error", output.getvalue() + str(stopped.exception))
        self.assertEqual(self.target.read_text(), "previous-token\n")

    def test_partial_missing_or_excess_scopes_preserve_existing_token(self):
        cases = [({}, ["--apply"]),
                 ({"scope": AUTHORISE.SCOPE_READ}, ["--apply", "--write"]),
                 ({"scope": " ".join(AUTHORISE.SCOPES_WRITE)}, ["--apply"]),
                 ({"scope": AUTHORISE.SCOPE_READ, "refresh_token": ""}, ["--apply"]),
                 ({"scope": AUTHORISE.SCOPE_READ, "refresh_token": "invalid\u0000token"}, ["--apply"])]
        for fields, args in cases:
            with self.subTest(fields=fields, args=args):
                self.target.write_text("previous-token\n")
                token = {"refresh_token": "test-refresh-token", **fields}
                result, output = self.run_main(token, args)
                self.assertIsInstance(result, SystemExit)
                self.assertEqual(self.target.read_text(), "previous-token\n")
                self.assertEqual(list(self.root.glob(".gtm-token-*")), [])
                self.assertNotIn("test-refresh-token", output + str(result))

    def test_write_grant_accepts_all_requested_scopes(self):
        result, _ = self.run_main({"scope": " ".join(AUTHORISE.SCOPES_WRITE),
                                  "refresh_token": "test-write-refresh"}, ["--apply", "--write"])
        self.assertEqual(result, 0)
        self.assertEqual(self.target.read_text(), "test-write-refresh\n")

    def test_atomic_save_failure_preserves_previous_token_and_removes_temporary_file(self):
        self.target.write_text("previous-token\n")
        with mock.patch.object(AUTHORISE.os, "replace", side_effect=OSError("test failure")):
            with self.assertRaises(OSError):
                AUTHORISE.save_token(self.target, "test-refresh-token")
        self.assertEqual(self.target.read_text(), "previous-token\n")
        self.assertEqual(list(self.root.glob(".gtm-token-*")), [])

    def test_token_endpoint_redirect_is_rejected_without_reading_body(self):
        response = mock.Mock()
        with self.assertRaises(ValueError):
            AUTHORISE.NoTokenRedirects().http_error_302(None, response, 302, "Redirect", {})
        response.close.assert_called_once()
        response.read.assert_not_called()


if __name__ == "__main__":
    unittest.main()
