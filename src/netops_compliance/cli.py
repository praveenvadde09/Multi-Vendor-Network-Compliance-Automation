"""Explicit selection, offline-only defaults, and stable exit codes."""

import argparse
import sys
from pathlib import Path

from .collector import SCENARIOS, collect
from .compliance import evaluate
from .inventory import InputError, load_inventory, load_rules, select_devices
from .reporting import make_report, write_report


def parser():
    result = argparse.ArgumentParser(description="NetOps offline compliance lab")
    result.add_argument("command", choices=("validate", "collect", "audit", "plan", "apply"))
    result.add_argument("--inventory", type=Path, default=Path("inventory/lab.example.yaml"))
    result.add_argument("--rules", type=Path, default=Path("rules/baseline.yaml"))
    selection = result.add_mutually_exclusive_group()
    selection.add_argument("--device", action="append", default=[])
    selection.add_argument("--group", action="append", default=[])
    selection.add_argument("--all", action="store_true")
    result.add_argument("--fixture-dir", type=Path, default=Path("tests/fixtures"))
    result.add_argument("--scenario", choices=SCENARIOS, default="compliant")
    result.add_argument("--mode", choices=("offline", "live"), default="offline")
    result.add_argument("--output", type=Path, default=Path("runs"))
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command in ("plan", "apply") or args.mode == "live":
            raise InputError(
                "unsupported operation: this release only validates and audits fixtures"
            )
        inventory, rules = load_inventory(args.inventory), load_rules(args.rules)
        if args.command == "validate":
            if args.device or args.group or args.all:
                select_devices(inventory, args.device, args.group, args.all)
            print(f"Valid: {len(inventory.devices)} devices; {len(rules.rules)} rules")
            return 0
        devices = select_devices(inventory, args.device, args.group, args.all)
        collections = collect(devices, args.fixture_dir, args.scenario, args.command)
        findings = (
            [f for c in collections for f in evaluate(c, rules)] if args.command == "audit" else []
        )
        report = make_report(inventory, rules, collections, findings, args.command, args.scenario)
        directory = write_report(report, args.output)
        print(f"Report: {directory}")
        print(f"Summary: {report['summary']}; exit={report['exit_code']}")
        return report["exit_code"]
    except (InputError, OSError):
        # Do not print validation/OS exceptions: they can contain secrets or input content.
        print(
            "Input/output or unsupported operation error; check schema, selection, mode and paths.",
            file=sys.stderr,
        )
        return 2
