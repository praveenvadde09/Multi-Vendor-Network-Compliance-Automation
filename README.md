# NetOps Compliance Automation Lab

A Python 3.12+ offline lab for Cisco IOS/IOS XE, Arista EOS, and Juniper Junos
configuration compliance. Distribution name: `netops-compliance-lab`; import name:
`netops_compliance`. Phases 1â€“4 are implemented, with JSON/Markdown reporting
included to make the offline demonstration reviewable.

## Quick start

Run from this repository's root. Installation needs package index access;
the demonstration and tests need no network access or credentials.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[dev]"
.\.venv\Scripts\netops-compliance validate
.\.venv\Scripts\netops-compliance audit --all
.\.venv\Scripts\python -m unittest discover -s tests -v
.\.venv\Scripts\python scripts/demo.py
.\.venv\Scripts\ruff check .
.\.venv\Scripts\ruff format --check .
```

Linux/macOS:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/netops-compliance validate
.venv/bin/netops-compliance audit --all
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/demo.py
.venv/bin/ruff check .
.venv/bin/ruff format --check .
```

Alternatively, with the pinned runtime dependencies already installed:
set `PYTHONPATH=src` and use `python -m netops_compliance`.
Default inventory, rules, fixture, and output paths are relative to the working
directory; run from the project root or supply explicit paths.

## Commands and outcomes

```text
netops-compliance validate
netops-compliance collect --device cisco01
netops-compliance audit --group access
netops-compliance audit --all --scenario noncompliant
netops-compliance audit --all --scenario malformed
```

`--device` and `--group` can be repeated; repeated groups select their union.
Selection is mandatory for collect/audit. Unknown names or groups are errors.
`validate` checks all input definitions and optionally validates a selection.
`collect` records collection status and configuration hashes; it does not audit
or export raw facts. `audit` evaluates the baseline against normalized facts.

Exit codes: **0** successful collection/validation or no applicable audit failures;
**1** noncompliance; **2** input, execution, collection, or unsupported-operation error.
A collect-only exit 0 is not a compliance verdict. Not-applicable checks are
counted separately; a platform mismatch is the only applicability condition.

Every run writes `runs/<unique-id>/report.json` and `report.md`, including device
selection, input identities, rule version, timestamps, hashes, findings and errors.
The `runs/` directory is ignored. Raw configuration and credentials are not stored.
A baseline hash is provenance for fixture bytes, **not** a backup or stale-plan control.

## Feature matrix

| Capability | Cisco | Arista | Juniper |
|---|---|---|---|
| Synthetic offline fixture collection | Yes | Yes | Yes |
| Eight structured configuration checks | Yes | Yes | Yes |
| Compliant/noncompliant/malformed fixtures | Yes | Yes | Yes |
| Read-only live transport | Unsupported | Unsupported | Unsupported |
| Tested live image/version | None | None | None |
| Change plans / backups / apply | Unsupported | Unsupported | Unsupported |
| Persistence / rollback / post-change verification | Unsupported | Unsupported | Unsupported |

No lab image was available or contacted. The fixtures are handwritten examples,
not captures from a tested release. Their dialect labels do not establish live
compatibility with any IOS, IOS XE, EOS, or Junos release.

All rules have `remediation: manual`. `plan`, `apply`, and `--mode live` exit 2
before collection. Dry run is always on; there is no flag to enable writes.
Credential references are validated but never resolved in offline mode.
Do not put passwords, private keys, SNMP communities, or sensitive values in
inventory/rules. Rule expected values are included in reports and must be public
baseline policy. Any future live release must resolve references via an environment
or secret-provider boundary.

## Baseline and parser scope

The eight checks cover approved NTP and syslog destinations, SSH configuration,
disabled Telnet, exact login notice, a hostname glob (`lab-*`), disabled HTTP/HTTPS/FTP,
and disabled SNMP. All eight apply to each of the three platforms.

These are configuration checks. They do not verify NTP synchronization, syslog
delivery, SSH key presence, authentication, reachability, or effective service
state. Syslog severity is currently normalized only for the supported Junos
`any info` fixture syntax; no cross-vendor severity rule is claimed.

Parsing is intentionally strict and fixture-only. See
[the supported grammar](docs/fixture-format.md). Unknown commands and ambiguous
or incomplete required state produce collection errors instead of passing checks.
Each platform/scenario file is reused for selected devices of that platform;
inventory names identify results, while the configured hostname is evaluated independently.

## Verification and next phases

The standard-library unittest suite runs without live connections. It exercises
strict schema validation, parser behavior, deterministic evaluation, reporting,
explicit selection, redaction, and failure isolation. CLI tests assert the
connection, backup and apply boundaries are never invoked. The scripted demo
checks expected exit codes and emits artifacts for three scenarios.

See [architecture](docs/architecture.md), [demo](docs/demo.md), and
[implementation status](docs/implementation-status.md).
Phases 5â€“8 live transport and remediation are deferred. Before enabling writes:
record exact tested images, introduce protected backups and reviewable plans,
require explicit authorization and a lab allowlist, reject stale baselines,
verify post-change state, and document recovery separately from backup availability.
