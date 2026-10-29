"""Reports contain allowlisted evidence, never raw configuration or exception messages."""

import hashlib
import html
import json
import uuid
from collections import Counter
from datetime import UTC, datetime


def digest(model):
    data = json.dumps(model.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode()).hexdigest()


def make_report(inventory, rules, collections, findings, command, scenario):
    counts = Counter(f.status.value for f in findings)
    device_errors = sum(c.error is not None for c in collections)
    exit_code = 2 if device_errors or counts["error"] else (1 if counts["fail"] else 0)
    now = datetime.now(UTC)
    return {
        "schema_version": "1",
        "run_id": now.strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:12],
        "timestamp": now.isoformat(),
        "mode": "offline",
        "dry_run": True,
        "command": command,
        "scenario": scenario,
        "inventory_identity": digest(inventory),
        "rule_version": rules.version,
        "rule_identity": digest(rules),
        "selected_devices": [c.device for c in collections],
        "summary": {
            **{s: counts[s] for s in ("pass", "fail", "error", "not-applicable")},
            "device_errors": device_errors,
        },
        "exit_code": exit_code,
        "devices": [
            {
                "device": c.device,
                "platform": c.platform,
                "baseline_hash": c.baseline_hash,
                "collected": c.facts is not None,
                "error": c.error,
            }
            for c in collections
        ],
        "findings": [f.model_dump(mode="json") for f in findings],
        "changes": [],
        "backups": [],
        "approval": None,
        "post_change_findings": [],
    }


def cell(value):
    return html.escape(json.dumps(value, ensure_ascii=True)).replace("|", "&#124;")


def markdown(report):
    lines = [
        "# NetOps compliance report",
        "",
        f"Run: {report['run_id']}",
        "",
        "Mode: offline fixture; dry run; no configuration writes.",
        "",
        f"Rule version: {cell(report['rule_version'])}",
        "",
        f"Summary: {cell(report['summary'])}",
        "",
        "## Collection",
        "",
        "| Device | Platform | Collected | Error |",
        "|---|---|---|---|",
    ]
    for device in report["devices"]:
        lines.append(
            "| "
            + " | ".join(cell(device[k]) for k in ("device", "platform", "collected", "error"))
            + " |"
        )
    lines += [
        "",
        "## Findings",
        "",
        "| Device | Rule | Severity | Status | Expected | Evidence | Error |",
        "|---|---|---|---|---|---|---|",
    ]
    for finding in report["findings"]:
        lines.append(
            "| "
            + " | ".join(
                cell(finding[k])
                for k in (
                    "device",
                    "rule_id",
                    "severity",
                    "status",
                    "expected",
                    "observed",
                    "error",
                )
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def write_report(report, root):
    directory = root / report["run_id"]
    directory.mkdir(parents=True, exist_ok=False)
    (directory / "report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (directory / "report.md").write_text(markdown(report), encoding="utf-8")
    return directory
