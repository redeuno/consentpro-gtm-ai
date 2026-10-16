"""Reproduce resume, truncated response and redirect failures without network access."""
import contextlib
import email.message
import http.client
import importlib.util
import io
import json
import pathlib
import socket
import sys
import tempfile
import unittest
import urllib.request
from unittest import mock


sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location(
    "asset_collector", pathlib.Path(__file__).with_name("collect-assets.py")
)
COLLECTOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COLLECTOR)


class MemorySocket:
    def __init__(self, raw):
        self.raw = raw

    def makefile(self, mode):
        return io.BytesIO(self.raw)


def response(url, raw):
    result = http.client.HTTPResponse(MemorySocket(raw))
    result.begin()
    result.url = url
    return result


class FakeOpener:
    def __init__(self, replies):
        self.replies = replies
        self.calls = []

    def open(self, request, timeout):
        self.calls.append(request.full_url)
        return response(request.full_url, self.replies[request.full_url])


class CollectorChecks(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="consent-assets-test-")
        self.addCleanup(self.directory.cleanup)
        self.root = pathlib.Path(self.directory.name)
        self.network = mock.patch.object(socket, "create_connection",
                                         side_effect=AssertionError("Network access is forbidden in this test"))
        self.network.start()
        self.addCleanup(self.network.stop)

    def collect(self, urls, opener):
        with mock.patch.object(COLLECTOR.urllib.request, "build_opener", return_value=opener), \
                mock.patch.object(COLLECTOR, "MAX_RETRIES", 0), \
                contextlib.redirect_stdout(io.StringIO()):
            result = COLLECTOR.collect(self.root, urls, [], 0)
        report = json.loads((self.root / "assets-index.json").read_text())
        return result, report

    def test_divergent_asset_preserves_expected_hash_and_can_resume(self):
        url = "https://docs.consentpro.com/a.png"
        original = b"original"
        relative = COLLECTOR.local_path(url)
        item = {"url": url, "path": relative, "kind": "image", "bytes": len(original),
                "sha256": COLLECTOR.digest(original), "status": "ok"}
        (self.root / "assets").mkdir()
        target = self.root / relative
        target.write_bytes(b"modified")
        (self.root / "assets-index.json").write_text(json.dumps({"assets": [item]}))
        opener = FakeOpener({})
        result, failed = self.collect({url: "image"}, opener)
        self.assertEqual(result, 1)
        self.assertEqual(failed["summary"]["successful"], 0)
        self.assertEqual(failed["summary"]["errors"], 1)
        self.assertEqual(failed["assets"][0]["sha256"], item["sha256"])
        self.assertEqual(failed["assets"][0]["status"], "verification_failed")
        self.assertEqual(target.read_bytes(), b"modified")
        target.write_bytes(original)
        result, recovered = self.collect({url: "image"}, opener)
        self.assertEqual(result, 0)
        self.assertEqual(recovered["summary"]["successful"], 1)
        self.assertEqual(recovered["summary"]["reused"], 1)
        self.assertEqual(recovered["summary"]["preserved_unverified"], 0)
        self.assertEqual(opener.calls, [])

    def test_incomplete_chunked_preserves_success_and_can_resume(self):
        first = "https://docs.consentpro.com/a.png"
        second = "https://docs.consentpro.com/b.png"
        urls = {first: "image", second: "image"}
        valid = b"HTTP/1.1 200 OK\r\nContent-Length: 3\r\nContent-Type: image/png\r\n\r\nabc"
        truncated = b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n5\r\nabc"
        result, failed = self.collect(urls, FakeOpener({first: valid, second: truncated}))
        self.assertEqual(result, 1)
        self.assertEqual(failed["summary"]["successful"], 1)
        self.assertEqual(failed["summary"]["errors"], 1)
        self.assertEqual(failed["failures"][0]["type"], "IncompleteRead")
        self.assertEqual((self.root / COLLECTOR.local_path(first)).read_bytes(), b"abc")
        self.assertFalse((self.root / COLLECTOR.local_path(second)).exists())
        resumed = FakeOpener({second: valid})
        result, recovered = self.collect(urls, resumed)
        self.assertEqual(result, 0)
        self.assertEqual(recovered["summary"]["successful"], 2)
        self.assertEqual(recovered["summary"]["reused"], 1)
        self.assertEqual(recovered["summary"]["downloaded"], 1)
        self.assertEqual(resumed.calls, [second])

    def test_redirect_is_closed_without_reading_body(self):
        class DrainTrap(io.BytesIO):
            def __init__(self):
                super().__init__(b"body that must not be read")
                self.read_calls = []

            def read(self, size=-1):
                self.read_calls.append(size)
                raise AssertionError("Redirect tried to read the body")

        handler_type = getattr(COLLECTOR, "RejectRedirects", None)
        if handler_type is None:
            handler_type = COLLECTOR.HostOnlyRedirect
        for code in (301, 302, 303, 307, 308):
            with self.subTest(code=code):
                handler = handler_type()
                body = DrainTrap()
                request = urllib.request.Request("https://docs.consentpro.com/a.png")
                headers = email.message.Message()
                headers["Location"] = "https://docs.consentpro.com/b.png"
                with self.assertRaises(ValueError):
                    getattr(handler, "http_error_" + str(code))(request, body, code, "Redirect", headers)
                self.assertTrue(body.closed)
                self.assertEqual(body.read_calls, [])

    def test_incomplete_read_counts_real_causal_partial_without_cycles(self):
        raw = b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n10000\r\n" + b"x" * 65535
        with response("https://docs.consentpro.com/a.png", raw) as stream:
            try:
                stream.read(65536)
            except http.client.IncompleteRead as error:
                self.assertEqual(error.partial, b"")
                self.assertEqual(len(error.__context__.partial), 65535)
                self.assertEqual(COLLECTOR.incomplete_read_bytes(error), 65535)
                error.__context__.__cause__ = error
                self.assertEqual(COLLECTOR.incomplete_read_bytes(error), 65535)
            else:
                self.fail("The response should be truncated")

    def test_no_request_or_retry_after_transfer_budget_is_exhausted(self):
        url = "https://docs.consentpro.com/a.png"
        raw = b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n10000\r\n" + b"x" * 65535
        for spent, expected_calls in ((0, 1), (65534, 1), (65535, 0)):
            with self.subTest(spent=spent):
                opener = FakeOpener({url: raw})
                budget = {"network_bytes": spent}
                with mock.patch.object(COLLECTOR, "MAX_TOTAL_BYTES", 65535), \
                        mock.patch.object(COLLECTOR.time, "sleep"):
                    with self.assertRaises(ValueError):
                        COLLECTOR.fetch(opener, url, budget)
                self.assertEqual(budget["network_bytes"], 65535)
                self.assertEqual(len(opener.calls), expected_calls)

    def test_causal_partial_leaves_only_remaining_byte_for_retry(self):
        url = "https://docs.consentpro.com/a.png"
        raw = b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n10000\r\n" + b"x" * 65535
        opener = FakeOpener({url: raw})
        budget = {"network_bytes": 0}
        with mock.patch.object(COLLECTOR, "MAX_TOTAL_BYTES", 65536), \
                mock.patch.object(COLLECTOR.time, "sleep"):
            with self.assertRaises(ValueError):
                COLLECTOR.fetch(opener, url, budget)
        self.assertEqual(budget["network_bytes"], 65536)
        self.assertEqual(len(opener.calls), 2)

    def test_exact_content_length_at_budget_needs_no_extra_read(self):
        url = "https://docs.consentpro.com/a.png"
        raw = b"HTTP/1.1 200 OK\r\nContent-Length: 3\r\n\r\nabc"
        opener = FakeOpener({url: raw})
        budget = {"network_bytes": 0}
        with mock.patch.object(COLLECTOR, "MAX_TOTAL_BYTES", 3):
            content, _, _ = COLLECTOR.fetch(opener, url, budget)
        self.assertEqual(content, b"abc")
        self.assertEqual(budget["network_bytes"], 3)
        self.assertEqual(len(opener.calls), 1)


if __name__ == "__main__":
    unittest.main()
