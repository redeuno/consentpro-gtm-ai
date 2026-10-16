"""Run the writer's current safety regressions using only the local fake API.

READS repository scripts and tests. WRITES disposable test files in temporary
directories, which the tests remove. No network, credential or repository writes.
Usage: python3 -B docs/06-agent-readiness/checks/reproduce-writer.py [REPOSITORY].
Safe to repeat; temporary state is discarded and no external rollback is needed.
A zero exit status means the selected safety regressions passed on current code.
Historical unsafe baseline observations remain in writer-results.json.
"""

import argparse
import contextlib
import datetime
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import socket
import sys
import unittest
import urllib.request
from unittest import mock

sys.dont_write_bytecode = True

CASES = (
    "test_wrong_named_trigger_fails_before_writes",
    "test_verified_trigger_is_reused_even_if_renamed",
    "test_business_event_keeps_trigger_and_gains_consent_checks",
    "test_multiregion_and_optional_parameters_are_preserved",
    "test_explicit_multiregion_replacement_fails_before_writes",
    "test_single_region_change_preserves_unrelated_parameters",
)


def load_cases(repo):
    sys.path.insert(0, str(repo / "tests"))
    try:
        spec = importlib.util.spec_from_file_location("writer_safety_regressions", repo / "tests/test_wire_safety.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return unittest.TestSuite(module.WireSafetyTests(name) for name in CASES)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository", nargs="?", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    repo = args.repository.resolve()
    with mock.patch.object(urllib.request, "urlopen", side_effect=AssertionError("Network access is forbidden")) as network, \
            mock.patch.object(socket, "socket", side_effect=AssertionError("Sockets are forbidden")), \
            contextlib.redirect_stdout(io.StringIO()):
        suite = load_cases(repo)
        result = unittest.TestResult()
        suite.run(result)
    report = {
        "evidence_kind": "current_offline_safety_regressions",
        "verified_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status": "passed" if result.wasSuccessful() and result.testsRun == len(CASES)
                  and not result.skipped and not result.expectedFailures else "failed",
        "tests_run": result.testsRun,
        "cases": list(CASES),
        "real_network_calls": network.call_count,
        "skipped": len(result.skipped),
        "expected_failures": len(result.expectedFailures),
        "failures": [{"test": test.id(), "message": trace.rstrip().splitlines()[-1]}
                     for test, trace in result.failures + result.errors],
        "source_files": [],
    }
    for name in ("scripts/wire-consent.py", "scripts/consent-template.py",
                 "tests/test_gallery_install.py", "tests/test_wire_safety.py"):
        data = (repo / name).read_bytes()
        report["source_files"].append({"path": name, "bytes": len(data),
                                       "sha256": hashlib.sha256(data).hexdigest()})
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "passed" and not network.call_count else 1


if __name__ == "__main__":
    sys.exit(main())
