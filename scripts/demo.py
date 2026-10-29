"""Reproducible offline demo. Run with the project's installed Python."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(args, expected):
    result = subprocess.run(
        [sys.executable, "-m", "netops_compliance", *args], cwd=ROOT, check=False
    )
    if result.returncode != expected:
        raise SystemExit(f"Unexpected exit {result.returncode}; expected {expected}")
    print(f"Verified expected exit {expected}", flush=True)


if __name__ == "__main__":
    run(["validate"], 0)
    for scenario, code in (("compliant", 0), ("noncompliant", 1), ("malformed", 2)):
        run(["audit", "--all", "--scenario", scenario], code)
