# Architecture

```text
CLI -> strict YAML schemas -> explicit selection -> offline vendor adapter
                                                -> normalized Facts
rules -> pure compliance engine <----------------------+
                    -> findings -> JSON + Markdown -> exit code
```

- `models.py`: strict Pydantic records and check-specific expected-value validation.
- `inventory.py`: safe YAML loading, duplicate-key rejection, identity and selection checks.
- `adapters/`: vendor syntax, capability flags, and explicit unsupported operations.
- `collector.py`: one device at a time, bounded input size, sanitized error codes.
- `compliance.py`: deterministic evaluations independent of transport and filesystem.
- `reporting.py`: public policy values and minimal evidence, unique run directories.
- `remediation.py`: unsupported-operation boundary for future work.

Inputs are validated before collection. Operations are checked again at the
collector boundary. Collection uses concurrency one and no credentials, sockets,
or network transport. Device timeouts/ports are validated for future use and have
no effect on filesystem reads. One adapter exception becomes a device error and
does not stop the other devices.

Rules have stable IDs, descriptions, severity, platforms, required inputs,
expected state, check method and manual remediation status. Required inputs must
match the check. Address lists are canonicalized during evaluation, and hostname
matching uses a bounded glob rather than executable code or arbitrary regex.

Applicability is resolved from the validated platform. A known mismatch is
not-applicable even if collection failed. An applicable rule with missing or
failed collection is error; a valid collected state that differs is fail.
Run-level collection errors always make the exit code 2.

The report contract includes a schema version, run ID, UTC timestamp, selected
device identities, input hashes, baseline version, device hashes/status,
per-rule severity/status/expected/observed/error, and explicit empty change,
backup, approval and post-change fields. Unknown endpoints, configured hostnames,
banner bodies, communities and raw exception strings are excluded from evidence.
Trusted baseline policy appears in expected values.

Future transport integration belongs behind adapters. No dependency on Netmiko
or another transport is included until read-only live support is implemented and
tested. Save, commit, confirmed-commit and recovery semantics must remain
vendor-specific and independently tested.
