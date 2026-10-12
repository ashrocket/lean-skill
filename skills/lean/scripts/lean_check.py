#!/usr/bin/env python3
"""lean_check: one-shot resource and runner check for the lean skill.

Prints whether local work is OK or the machine is tight, which runners
exist, and which ones bill outside a subscription. Stdlib only. Never
prints secret values; it reports only whether a variable or file exists.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

HOME = os.path.expanduser("~")


def run(cmd, timeout=5):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return (out.stdout or out.stderr).strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def sysctl(name):
    value = run(["sysctl", "-n", name])
    return value or None


def find_sparecode():
    candidates = [
        os.environ.get("SPARECODE_BIN"),
        shutil.which("sparecode"),
        os.path.join(HOME, "ashcode/sparecode/bin/sparecode"),
        os.path.join(HOME, "sparecode/bin/sparecode"),
    ]
    for path in candidates:
        if path and os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-free-gb", type=float,
                        default=float(os.environ.get("LEAN_MIN_FREE_GB", "20")),
                        help="free disk below this is tight (default 20, or $LEAN_MIN_FREE_GB)")
    parser.add_argument("--json", action="store_true", help="print JSON only")
    args = parser.parse_args()

    volume = "/System/Volumes/Data" if os.path.isdir("/System/Volumes/Data") else "/"
    usage = shutil.disk_usage(volume)
    free_gb = round(usage.free / 1e9, 2)

    pressure_raw = sysctl("kern.memorystatus_vm_pressure_level")
    pressure = {"1": "normal", "2": "warn", "4": "critical"}.get(pressure_raw or "", "unknown")
    load1 = os.getloadavg()[0]
    cpus = os.cpu_count() or 1

    reasons = []
    if free_gb < args.min_free_gb:
        reasons.append(f"disk {free_gb} GB free < {args.min_free_gb} GB")
    if pressure in ("warn", "critical"):
        reasons.append(f"memory pressure {pressure}")
    if load1 > cpus * 0.9:
        reasons.append(f"load {load1:.1f} on {cpus} CPUs")

    codex_login = run(["codex", "login", "status"]) if shutil.which("codex") else ""
    runners = {
        "claude": shutil.which("claude"),
        "codex": shutil.which("codex"),
        "agy": shutil.which("agy"),
        "sparecode": find_sparecode(),
        "gh": shutil.which("gh"),
        "ollama": shutil.which("ollama"),
    }
    billing = {
        "claude_on_subscription": not bool(os.environ.get("ANTHROPIC_API_KEY")),
        "codex_on_chatgpt_plan": "ChatGPT" in codex_login,
        "jev_key_present": bool(os.environ.get("TYPESAFE_API_KEY"))
        or os.path.isfile(os.path.join(HOME, ".typesafe.env")),
        "openrouter_key_present": bool(os.environ.get("OPENROUTER_API_KEY")),
    }
    warnings = []
    if runners["claude"] and not billing["claude_on_subscription"]:
        warnings.append("ANTHROPIC_API_KEY is set: claude -p bills the API. "
                        "Run it as: env -u ANTHROPIC_API_KEY claude -p ...")
    if runners["codex"] and not billing["codex_on_chatgpt_plan"]:
        warnings.append("codex is not on a ChatGPT login: codex exec may bill the API.")
    if runners["sparecode"] and not billing["openrouter_key_present"]:
        warnings.append("sparecode hosted mode needs OPENROUTER_API_KEY "
                        "(pay per token); local Ollama mode does not.")

    report = {
        "verdict": "tight" if reasons else "local-ok",
        "advice": ("Prefer cloud runners. No local builds, local models, or wide local fan-out."
                   if reasons else
                   "Local background runners are OK. Keep fan-out small."),
        "reasons": reasons,
        "disk": {"volume": volume, "free_gb": free_gb},
        "memory_pressure": pressure,
        "load1": round(load1, 2),
        "cpus": cpus,
        "runners": runners,
        "billing": billing,
        "warnings": warnings,
    }

    if args.json:
        print(json.dumps(report, indent=2))
        return 0
    print(f"lean: {report['verdict'].upper()} - {report['advice']}")
    for reason in reasons:
        print(f"  reason: {reason}")
    print(f"  disk {free_gb} GB free on {volume} | memory {pressure} | load {load1:.1f}/{cpus} CPUs")
    present = [name for name, path in runners.items() if path]
    print(f"  runners: {', '.join(present) or 'none'}")
    for warning in warnings:
        print(f"  warn: {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
