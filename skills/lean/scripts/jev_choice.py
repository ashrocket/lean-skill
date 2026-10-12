#!/usr/bin/env python3
"""jev_choice: ask Jev (TypeSafe System One) one typed choice question.

Usage:
  jev_choice.py --state state.json --instructions "..." \
      --option yes="the text names a secret" --option no="it does not"

Prints the JSON answer (choice + probabilities) and appends a usage line
(model, tokens, latency; no state or key) to $LEAN_LEDGER or
${TMPDIR}/lean/jev-usage.jsonl. Reads the key from TYPESAFE_API_KEY or
~/.typesafe.env and never prints it. Docs: https://docs.typesafe.ai/llms.txt
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ENDPOINT = "https://api.typesafe.ai/v1/systemone"


def api_key():
    if os.environ.get("TYPESAFE_API_KEY"):
        return os.environ["TYPESAFE_API_KEY"]
    source = Path.home() / ".typesafe.env"
    if source.is_file():
        for line in source.read_text().splitlines():
            line = line.strip().removeprefix("export ").strip()
            if line.startswith("TYPESAFE_API_KEY="):
                return line.split("=", 1)[1].strip().strip("'\"")
    sys.exit("Set TYPESAFE_API_KEY or create ~/.typesafe.env")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--state", required=True, help="JSON file with the facts Jev may read")
    parser.add_argument("--instructions", required=True)
    parser.add_argument("--option", action="append", required=True, metavar="NAME=CRITERION")
    parser.add_argument("--model", default=os.environ.get("JEV_MODEL", "jev-1.13.0"))
    args = parser.parse_args()

    criteria = {}
    for item in args.option:
        name, _, criterion = item.partition("=")
        if not name or not criterion:
            sys.exit(f"--option needs NAME=CRITERION, got {item!r}")
        criteria[name.strip()] = criterion.strip()
    state = json.loads(Path(args.state).read_text())
    payload = {
        "model": args.model,
        "state": state,
        "questions": {"answer": {"type": "choice", "instructions": args.instructions, "criteria": criteria}},
    }

    started = time.monotonic()
    result = None
    for attempt in range(3):
        request = urllib.request.Request(
            ENDPOINT, data=json.dumps(payload).encode(),
            headers={"Authorization": "Bearer " + api_key(), "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                result = json.load(response)
            break
        except urllib.error.HTTPError as error:
            if error.code not in {429, 502, 503, 529} or attempt == 2:
                sys.exit(f"Jev HTTP {error.code}")
            time.sleep(min(30, 2 ** (attempt + 1)))

    usage = result.get("usage", {})
    ledger = Path(os.environ.get("LEAN_LEDGER") or Path(os.environ.get("TMPDIR", "/tmp")) / "lean" / "jev-usage.jsonl")
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a") as stream:
        stream.write(json.dumps({
            "time": time.time(), "model": result.get("model"),
            "input_tokens": usage.get("input_tokens"), "output_tokens": usage.get("output_tokens"),
            "latency_ms": round((time.monotonic() - started) * 1000),
        }) + "\n")
    print(json.dumps({"model": result.get("model"), "usage": usage, "answer": result["answers"]["answer"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
