# Offline demonstration

From the project root after installation:

```sh
python scripts/demo.py
```

On Windows use `.venv\\Scripts\\python scripts/demo.py` if the environment is not activated.

The script runs validation and three full-fleet audits and checks their exit codes:
- Compliant: 24 passing findings, exit 0.
- Noncompliant: 23 failures and 1 pass, exit 1.
- Malformed: 24 errors and 3 device collection errors, exit 2.

Run artifacts are stored in separate unique directories under `runs/`.
Committed copies are in `examples/reports/`.
Each report identifies the selected devices, baseline rule version, hashes,
per-rule expected state and sanitized observed evidence.

To show selection:
`netops-compliance audit --device cisco01` or
`netops-compliance audit --group edge`.
To show failure isolation, run the unit test
`python -m unittest tests.unit.test_lab.LabTests.test_isolation_of_failures_and_redaction -v`.
It injects a failure for Cisco and verifies the other devices still collect.

To demonstrate boundaries:
`netops-compliance apply --all`,
`netops-compliance plan --all`, and
`netops-compliance audit --all --mode live` each exit 2 before collection.

Do not present the fixture audits as evidence of live compatibility, operational
NTP/SSH verification, change execution, recovery or remediation idempotency.
Those interview scenarios are reserved for later tested live phases.
