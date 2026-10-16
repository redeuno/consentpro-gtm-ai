"""Check native Claude Code discovery without a model request (macOS only).

READS generated local skills and the CLI's initialize control response. WRITES
only disposable directories. The default is a dry run; --run starts the check.
No account, MCP or business API is used. Network access and writes outside the
disposable project are denied by sandbox-exec; inherited credentials are removed.
Safe to repeat: processes are bounded and temporary files are removed on exit.
This checks discovery, not model adherence or Claude web/Desktop installation.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ("consent-pro", "consent-pro-gtm")
TIMEOUT = 20
MAX_OUTPUT = 2_000_000


class Unavailable(RuntimeError):
    pass


def bounded(command, cwd, environment, root, label, payload="", timeout=TIMEOUT):
    stdout = root / (label + ".stdout")
    stderr = root / (label + ".stderr")
    with stdout.open("wb") as out, stderr.open("wb") as err:
        process = subprocess.Popen(command, cwd=cwd, env=environment,
                                   stdin=subprocess.PIPE, stdout=out, stderr=err,
                                   start_new_session=True)
        try:
            process.communicate(payload.encode(), timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(label + " exceeded its time limit") from exc
        finally:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait(timeout=5)
    if stdout.stat().st_size > MAX_OUTPUT or stderr.stat().st_size > MAX_OUTPUT:
        raise RuntimeError(label + " exceeded its output limit")
    return process.returncode, stdout.read_text(), stderr.read_text()


def profile(root, home, binary, credential_control, executables):
    quote = json.dumps
    allowed = " ".join("(literal " + quote(str(path)) + ")" for path in executables)
    return "\n".join([
        "(version 1)",
        "(allow default)",
        "(deny network*)",
        "(deny file-write*)",
        "(allow file-write* (subpath " + quote(str(root)) + ") (literal \"/dev/null\"))",
        "(deny file-read-data (require-all (subpath " + quote(str(home)) + ")",
        "  (require-not (literal " + quote(str(binary)) + "))))",
        "(deny file-read-data (literal " + quote(str(credential_control)) + "))",
        "(deny mach-lookup (global-name \"com.apple.securityd\")",
        "  (global-name \"com.apple.securityd.xpc\") (global-name \"com.apple.secd\"))",
        "(deny process-exec)",
        "(allow process-exec " + allowed + ")",
        "",
    ])


def verify_sandbox(sandbox, root, outside, environment, binary):
    control = outside / "synthetic-credential"
    control.write_text("synthetic test value, not a credential")
    python = Path(sys.executable).resolve()
    executables = [python]
    framework_python = Path(sys.base_prefix) / "Resources/Python.app/Contents/MacOS/Python"
    if framework_python.is_file():
        executables.append(framework_python.resolve())
    guard = root / "probe.sb"
    guard.write_text(profile(root, Path.home(), binary, control, executables))
    probe = root / "probe.py"
    probe.write_text(
        "import json, pathlib, socket, subprocess, sys\n"
        "checks = {}\n"
        "for name, operation in [\n"
        "    ('credential_read_denied', lambda: pathlib.Path(sys.argv[1]).read_bytes()),\n"
        "    ('outside_write_denied', lambda: pathlib.Path(sys.argv[2]).write_text('test')),\n"
        "    ('network_denied', lambda: socket.socket().bind(('127.0.0.1', 0))),\n"
        "    ('unapproved_exec_denied', lambda: subprocess.run(['/usr/bin/true'], check=True)),\n"
        "]:\n"
        "    try:\n"
        "        operation()\n"
        "        checks[name] = False\n"
        "    except PermissionError:\n"
        "        checks[name] = True\n"
        "pathlib.Path(sys.argv[3]).write_text('allowed')\n"
        "checks['temporary_write_allowed'] = True\n"
        "print(json.dumps(checks))\n"
    )
    command = [sandbox, "-f", str(guard), str(python), "-I", "-B", str(probe),
               str(control), str(outside / "forbidden-write"), str(root / "allowed-write")]
    code, output, _ = bounded(command, root, environment, root, "sandbox-probe", timeout=5)
    if code:
        raise Unavailable("The local sandbox probe could not execute safely")
    checks = json.loads(output)
    if len(checks) != 5 or not all(checks.values()):
        raise RuntimeError("Sandbox enforcement failed; Claude was not started")
    cli_profile = root / "claude.sb"
    cli_profile.write_text(profile(root, Path.home(), binary, control, (binary,)))
    return cli_profile, checks


def copy_skills(source, destination):
    copied = []
    for name in SKILLS:
        folder = source / name
        if not (folder / "SKILL.md").is_file():
            raise Unavailable("Missing generated skill: " + str(folder / "SKILL.md"))
        if folder.is_symlink() or any(path.is_symlink() for path in folder.rglob("*")):
            raise RuntimeError("Generated skill contains a symbolic link: " + name)
        shutil.copytree(folder, destination / name)
        original = hashlib.sha256((folder / "SKILL.md").read_bytes()).hexdigest()
        installed = destination / name / "SKILL.md"
        actual = hashlib.sha256(installed.read_bytes()).hexdigest()
        if original != actual:
            raise RuntimeError("Copied skill differs from its source: " + name)
        copied.append({"name": name, "source": str(folder / "SKILL.md"),
                       "discovered_project_path": str(installed), "sha256": actual})
    return copied


def initialize(command, cwd, environment, root, label, expected):
    log = root / (label + ".log")
    invocation = [*command, "--debug-file", str(log)]
    request_id = "consent-pro-discovery-" + label
    payload = {"type": "control_request", "request_id": request_id,
               "request": {"subtype": "initialize"}}
    code, output, stderr = bounded(invocation, cwd, environment, root, label,
                                   json.dumps(payload) + "\n")
    if code or stderr:
        raise RuntimeError(label + " initialization did not exit cleanly")
    messages = [json.loads(line) for line in output.splitlines() if line.strip()]
    if any(message.get("type") not in ("system", "control_response") for message in messages):
        raise RuntimeError("Unexpected response type; no model output is permitted")
    responses = [m["response"] for m in messages if m.get("type") == "control_response"
                 and m.get("response", {}).get("request_id") == request_id]
    if len(responses) != 1 or responses[0].get("subtype") != "success":
        raise RuntimeError("Missing successful initialize control response")
    response = responses[0]["response"]
    if response.get("account", {}).get("tokenSource") != "none":
        raise RuntimeError("The isolated client did not confirm tokenSource=none")
    found = [entry for entry in response.get("commands", []) if entry.get("name") in SKILLS]
    if sorted(entry["name"] for entry in found) != sorted(expected):
        raise RuntimeError(label + " discovery did not match the expected skill set")
    if any(not entry.get("description", "").endswith(" (project)") for entry in found):
        raise RuntimeError("A discovered skill was not identified as a project skill")
    log_text = log.read_text()
    skill_root = str(cwd / ".claude" / "skills")
    if skill_root not in log_text or "project: " + str(len(expected)) not in log_text:
        raise RuntimeError("Native discovery log did not confirm the disposable project")
    return {"case": label, "skills": sorted(expected), "command": invocation,
            "token_source": "none", "message_types": sorted({m["type"] for m in messages}),
            "evidence": [line for line in log_text.splitlines()
                         if "Loading skills from:" in line or "unique skills (" in line]}


def run(source):
    if sys.platform != "darwin":
        raise Unavailable("This check requires macOS sandbox-exec; no fallback starts Claude")
    sandbox = shutil.which("sandbox-exec")
    installed = shutil.which("claude")
    if not sandbox or not installed:
        raise Unavailable("Native Claude Code and sandbox-exec must already be installed")
    binary = Path(installed).resolve()
    with binary.open("rb") as stream:
        magic = stream.read(4)
    if magic not in (b"\xcf\xfa\xed\xfe", b"\xfe\xed\xfa\xcf",
                     b"\xca\xfe\xba\xbe", b"\xbe\xba\xfe\xca"):
        raise Unavailable("Only the native macOS executable is supported; wrappers are not run")
    with tempfile.TemporaryDirectory(prefix="consent-pro-claude-") as folder, \
            tempfile.TemporaryDirectory(prefix="consent-pro-denied-") as other:
        root, outside = Path(folder).resolve(), Path(other).resolve()
        project = root / "project"
        project.mkdir()
        environment = {
            "PATH": "/usr/bin:/bin:/usr/sbin:/sbin", "LANG": "en_US.UTF-8",
            "TMPDIR": str(root), "CLAUDE_CONFIG_DIR": str(root / "config"),
            "XDG_CONFIG_HOME": str(root / "xdg-config"),
            "XDG_CACHE_HOME": str(root / "xdg-cache"),
            "XDG_STATE_HOME": str(root / "xdg-state"),
            "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1", "DISABLE_TELEMETRY": "1",
        }
        guard, controls = verify_sandbox(sandbox, root, outside, environment, binary)
        base = [sandbox, "-f", str(guard), str(binary)]
        code, version, _ = bounded([*base, "--version"], project, environment,
                                   root, "version", timeout=5)
        if code or "Claude Code" not in version:
            raise Unavailable("The isolated native executable did not identify Claude Code")
        code, help_text, _ = bounded([*base, "--help"], project, environment,
                                     root, "help", timeout=5)
        required = ("--input-format", "--output-format", "--no-session-persistence",
                    "--strict-mcp-config", "--setting-sources", "--settings", "--tools")
        if code or any(flag not in help_text for flag in required):
            raise Unavailable("The installed CLI lacks the required isolation/control options")
        paths = copy_skills(source, project / ".claude" / "skills")
        mcp = root / "mcp-empty.json"
        mcp.write_text(json.dumps({"mcpServers": {}}))
        command = [*base, "--print", "--input-format", "stream-json", "--output-format",
                   "stream-json", "--verbose", "--no-chrome", "--strict-mcp-config",
                   "--mcp-config", str(mcp), "--setting-sources", "project", "--settings",
                   json.dumps({"disableAllHooks": True}), "--tools", "",
                   "--no-session-persistence"]
        checks = [initialize(command, project, environment, root, "positive", SKILLS)]
        moved = project / ".claude" / "skills" / SKILLS[0]
        held = root / "held-skill"
        moved.rename(held)
        try:
            checks.append(initialize(command, project, environment, root, "missing", SKILLS[1:]))
        finally:
            held.rename(moved)
        checks.append(initialize(command, project, environment, root, "restored", SKILLS))
        result = {"status": "verified_discovery", "native_client": version.strip(),
                  "source": str(source), "skill_paths": paths, "sandbox_controls": controls,
                  "checks": checks, "model_prompts_sent": 0, "business_tools_called": 0,
                  "scope": "Native local discovery only; no model adherence or hosted-client claim",
                  "hooks": "Custom hooks disabled; native built-in modules may still execute"}
    result["temporary_directories_removed"] = not root.exists() and not outside.exists()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", action="store_true", help="Run the isolated local discovery checks")
    parser.add_argument("--skills", type=Path, default=ROOT / "dist" / "skills",
                        help="Generated directory containing both skill packages")
    args = parser.parse_args()
    if not args.run:
        print(json.dumps({"status": "dry_run", "skills": str(args.skills),
                          "next": "Use --run on macOS with native Claude Code and sandbox-exec",
                          "effect": "No CLI, model, network or temporary project was started"}))
        return 0
    try:
        result = run(args.skills.resolve())
    except Unavailable as exc:
        print(json.dumps({"status": "UNAVAILABLE", "reason": str(exc)}))
        return 2
    except (OSError, ValueError, RuntimeError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(json.dumps({"status": "FAILED", "reason": str(exc)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
