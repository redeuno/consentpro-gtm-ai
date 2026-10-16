"""Check native Codex discovery of packages installed outside this checkout.

READS local source and Codex's skills/list API. WRITES only a disposable directory
with generated packages and an empty Git repository. No model request or business
tool is invoked. Run with --run; default is an explanation without starting Codex.
Safe to repeat: temporary files are removed and the app-server process is stopped.
Existing agent configuration and installed skills are not modified.
"""

import argparse
import importlib.util
import json
from pathlib import Path
import queue
import shutil
import subprocess
import tempfile
import threading
import time

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    if not args.run:
        print("Use --run to test native Codex skill discovery in a disposable project.")
        return
    binary = shutil.which("codex")
    if not binary:
        parser.exit(1, "Codex CLI is not installed; native discovery is unverified.\n")
    spec = importlib.util.spec_from_file_location("package_skills", ROOT / "scripts/package-skills.py")
    package = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(package)
    with tempfile.TemporaryDirectory(prefix="consent-pro-client-") as folder:
        cwd = Path(folder).resolve()
        subprocess.run(["git", "init", "--quiet", str(cwd)], check=True)
        package.install(cwd / ".agents/skills", apply=True)
        process = subprocess.Popen([binary, "app-server", "--stdio"], cwd=cwd, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        messages = queue.Queue()

        def reader():
            for line in process.stdout:
                try:
                    messages.put(json.loads(line))
                except ValueError:
                    continue
            messages.put(None)

        thread = threading.Thread(target=reader, daemon=True)
        thread.start()

        def send(method, params, identifier=None):
            payload = {"jsonrpc": "2.0", "method": method, "params": params}
            if identifier is not None:
                payload["id"] = identifier
            process.stdin.write(json.dumps(payload) + "\n")
            process.stdin.flush()

        def receive(identifier):
            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                message = messages.get(timeout=max(0.01, deadline - time.monotonic()))
                if message is None:
                    raise RuntimeError("App-server stopped before skill discovery")
                if message.get("id") == identifier:
                    if "error" in message:
                        raise RuntimeError("App-server rejected the discovery request")
                    return message["result"]
            raise TimeoutError("Native skill discovery timed out")

        try:
            send("initialize", {"clientInfo": {"name": "consent-pro-package-check", "version": "1.0"}}, 1)
            receive(1)
            send("initialized", {})
            send("skills/list", {"cwds": [str(cwd)], "forceReload": True}, 2)
            response = receive(2)
            installed = cwd / ".agents/skills"
            found = {}
            for entry in response.get("data", []):
                for skill in entry.get("skills", []):
                    path = Path(skill.get("path", "")).resolve()
                    if path.is_relative_to(installed):
                        found[skill.get("name")] = skill
            if set(found) != set(package.SKILLS):
                raise RuntimeError("Codex did not discover both installed skill names")
            if any(not value.get("enabled", True) for value in found.values()):
                raise RuntimeError("An installed skill is disabled")
            print(json.dumps({"status": "verified", "native_client": "codex",
                              "skills": sorted(found), "business_tools_called": 0}))
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
            process.stdin.close()
            process.stdout.close()
            thread.join(timeout=1)


if __name__ == "__main__":
    main()
