# Implementation status

| Phase | Status | Evidence |
|---|---|---|
| 1 Repository/package/CLI/setup | Implemented | pyproject, README, unittest and Ruff commands |
| 2 Validated inventory and models | Implemented | strict schemas and negative-input tests |
| 3 Offline adapters and fixtures | Implemented for restricted grammar | 3 adapters, 9 synthetic fixtures |
| 4 Compliance engine | Implemented | 8 rules, deterministic fixture tests |
| 5 Reports and live reads | Reports implemented; live reads deferred | JSON/Markdown reports; live rejected |
| 6 Change plans | Deferred | plan rejected; all rules manual |
| 7 Controlled writes | Deferred | apply rejected; capabilities false |
| 8 Portfolio demo | Offline script/examples implemented; live demo deferred | scripts/demo.py |

Verified locally with Python 3.12.6, PyYAML 6.0.2 and Pydantic 2.13.4.
The runtime dependencies are pinned to versions exercised in the offline suite.
No transport has been selected or tested. No live image/version has been verified.

Failure tests inject timeout, permission, connection and unexpected exceptions
at the adapter boundary. These demonstrate isolation, not real authentication or
network behavior. Live wrong-password/unreachable-device tests remain unimplemented.
Backup failure, stale plans, interrupted writes and post-change validation are
future remediation tests, not claimed features of this release.

Future acceptance gates:
1. Read-only live collection, transport pinning and exact image/version records.
2. Narrow reversible vendor-specific change planning with traceable findings.
3. Protected backup success, reviewed plan identity, exact selected device set,
   explicit authorization, allowlist and fresh-baseline hash checks before writes.
4. Sequential writes, no blind retry after timeouts, post-change checks and
   independently verified persistence/recovery behavior.
5. Opt-in isolated-lab integration tests and evidence for each supported image.

An offline configuration hash is not recovery material. This release has no
automatic rollback, configuration persistence or successful remediation claim.

Local verification: 23 unittest tests passed; Ruff 0.14.3 lint and format checks passed.
Editable installation and the installed CLI entry point succeeded. The scripted
demo returned expected exit codes 0, 1 and 2. Windows installation verification
used a virtual environment inheriting the preinstalled pinned runtime dependencies;
the documented clean-environment installation and Linux CI have not been run here.
