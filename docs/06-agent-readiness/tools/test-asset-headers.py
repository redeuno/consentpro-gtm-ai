"""Test header guards offline without network access or snapshot changes."""
import email.message
import importlib.util
import pathlib
import sys
import unittest


sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location(
    "asset_collector", pathlib.Path(__file__).with_name("collect-assets.py")
)
COLLECTOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COLLECTOR)


def headers(pairs):
    message = email.message.Message()
    for name, value in pairs:
        message[name] = value
    return message


class HeaderChecks(unittest.TestCase):
    def test_accepted_values(self):
        cases = [([], None), ([("Content-Length", "12")], 12),
                 ([("Content-Length", "0")], 0),
                 ([("Transfer-Encoding", "chunked")], None)]
        for pairs, expected in cases:
            with self.subTest(pairs=pairs):
                self.assertEqual(COLLECTOR.checked_response_headers(headers(pairs)), expected)

    def test_rejected_values(self):
        cases = [
            [("Content-Length", "12"), ("Content-Length", "12")],
            [("Content-Length", "12"), ("Content-Length", "13")],
            [("Content-Length", "12, 12")],
            [("Content-Length", "-1")],
            [("Content-Length", " 12")],
            [("Content-Length", "12 ")],
            [("Transfer-Encoding", "chunked"), ("Transfer-Encoding", "chunked")],
            [("Transfer-Encoding", "chunked"), ("Content-Length", "12")],
            [("Transfer-Encoding", "gzip")],
            [("Transfer-Encoding", "gzip, chunked")],
            [("Transfer-Encoding", "Chunked")],
            [("Transfer-Encoding", " chunked")],
            [("Transfer-Encoding", "chunked ")],
            [("Transfer-Encoding", "chunked\t")],
            [("Transfer-Encoding", "")],
        ]
        for pairs in cases:
            with self.subTest(pairs=pairs):
                with self.assertRaises(ValueError):
                    COLLECTOR.checked_response_headers(headers(pairs))


if __name__ == "__main__":
    unittest.main()
