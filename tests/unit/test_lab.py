import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pydantic import ValidationError

from netops_compliance.adapters import get_adapter
from netops_compliance.adapters.base import Adapter, ParseError, UnsupportedOperation
from netops_compliance.cli import main
from netops_compliance.collector import collect
from netops_compliance.compliance import evaluate
from netops_compliance.inventory import InputError, load_inventory, load_rules, select_devices
from netops_compliance.models import PLATFORMS, Device, Inventory, Rule, RuleSet, Status
from netops_compliance.reporting import make_report, markdown

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "tests/fixtures"


class LabTests(unittest.TestCase):
    def setUp(self):
        self.inventory = load_inventory(ROOT / "inventory/lab.example.yaml")
        self.rules = load_rules(ROOT / "rules/baseline.yaml")

    def test_all_compliant(self):
        for result in collect(self.inventory.devices, FIXTURES):
            with self.subTest(platform=result.platform):
                findings = evaluate(result, self.rules)
                self.assertEqual(len(findings), 8)
                self.assertEqual({f.status for f in findings}, {Status.PASS})
                self.assertEqual(findings, evaluate(result, self.rules))

    def test_noncompliant_exact_outcomes(self):
        for result in collect(self.inventory.devices, FIXTURES, "noncompliant"):
            with self.subTest(platform=result.platform):
                findings = evaluate(result, self.rules)
                expected = 7 if result.platform == "arista_eos" else 8
                self.assertEqual(sum(f.status == Status.FAIL for f in findings), expected)
                self.assertFalse(any(f.status == Status.ERROR for f in findings))

    def test_malformed_is_error_for_every_vendor(self):
        for result in collect(self.inventory.devices, FIXTURES, "malformed"):
            with self.subTest(platform=result.platform):
                self.assertEqual(result.error, "fixture_parse_error")
                self.assertEqual({f.status for f in evaluate(result, self.rules)}, {Status.ERROR})

    def test_unknown_or_ambiguous_commands_error(self):
        for platform in PLATFORMS:
            raw = (FIXTURES / platform / "compliant.cfg").read_text()
            terminator = "# end-fixture" if platform == "juniper_junos" else "end"
            bad = raw.replace("\n" + terminator + "\n", "\nunknown command\n" + terminator + "\n")
            with self.subTest(platform=platform), self.assertRaises(ParseError):
                get_adapter(platform).normalize(bad)
        raw = (FIXTURES / "cisco_ios/compliant.cfg").read_text()
        for bad in (
            raw.replace(" transport input ssh", " login local", 1),
            raw.replace("line vty 5 15", "line vty 4 15"),
            raw.replace("line vty 5 15\n transport input ssh\n", ""),
        ):
            with self.assertRaises(ParseError):
                get_adapter("cisco_ios").normalize(bad)

    def test_no_inference_from_missing_service_state(self):
        raw = (FIXTURES / "cisco_ios/compliant.cfg").read_text()
        with self.assertRaises(ParseError):
            get_adapter("cisco_ios").normalize(raw.replace("no ip http server\n", ""))

    def test_conflicting_snmp_state_in_either_order(self):
        for platform in ("cisco_ios", "arista_eos"):
            raw = (FIXTURES / platform / "compliant.cfg").read_text()
            for commands in (
                "no snmp-server\nsnmp-server community SYNTHETIC ro",
                "snmp-server community SYNTHETIC ro\nno snmp-server",
            ):
                with self.subTest(platform=platform, commands=commands):
                    with self.assertRaises(ParseError):
                        get_adapter(platform).normalize(raw.replace("no snmp-server", commands))

    def test_truncated_snapshot_is_error(self):
        for platform in PLATFORMS:
            raw = (FIXTURES / platform / "compliant.cfg").read_text()
            with self.subTest(platform=platform), self.assertRaises(ParseError):
                get_adapter(platform).normalize("\n".join(raw.splitlines()[:-1]))

    def test_selected_device_only_reaches_adapter(self):
        from netops_compliance.collector import get_adapter as real_get_adapter

        with (
            tempfile.TemporaryDirectory() as output,
            patch("netops_compliance.collector.get_adapter", wraps=real_get_adapter) as factory,
        ):
            self.assertEqual(
                self.cli(
                    "audit",
                    "--device",
                    "juniper01",
                    "--inventory",
                    str(ROOT / "inventory/lab.example.yaml"),
                    "--rules",
                    str(ROOT / "rules/baseline.yaml"),
                    "--fixture-dir",
                    str(FIXTURES),
                    "--output",
                    output,
                ),
                0,
            )
            factory.assert_called_once_with("juniper_junos")

    def test_applicability_known_even_when_collection_fails(self):
        data = self.rules.rules[0].model_dump()
        data["platforms"] = ["arista_eos"]
        rules = RuleSet(version="1", rules=[Rule(**data)])
        result = collect(self.inventory.devices[:1], FIXTURES, "malformed")[0]
        self.assertEqual(evaluate(result, rules)[0].status, Status.NOT_APPLICABLE)

    def test_missing_facts_is_error(self):
        result = collect(self.inventory.devices[:1], FIXTURES)[0]
        result.facts = None
        self.assertEqual({f.status for f in evaluate(result, self.rules)}, {Status.ERROR})

    def test_isolation_of_failures_and_redaction(self):
        for exception in (
            TimeoutError("PASSWORD_MARKER"),
            PermissionError("PASSWORD_MARKER"),
            ConnectionError("PASSWORD_MARKER"),
            RuntimeError("PASSWORD_MARKER"),
        ):
            with (
                self.subTest(error=type(exception).__name__),
                patch(
                    "netops_compliance.adapters.cisco.CiscoAdapter.normalize", side_effect=exception
                ),
            ):
                results = collect(self.inventory.devices, FIXTURES)
            self.assertIsNotNone(results[0].error)
            self.assertTrue(all(c.facts for c in results[1:]))
            findings = [f for c in results for f in evaluate(c, self.rules)]
            report = make_report(
                self.inventory, self.rules, results, findings, "audit", "compliant"
            )
            self.assertEqual(report["exit_code"], 2)
            self.assertNotIn("PASSWORD_MARKER", json.dumps(report))

    def test_sensitive_evidence_is_minimal(self):
        results = collect(self.inventory.devices, FIXTURES, "noncompliant")
        results[0].facts.banner = "PASSWORD_MARKER"
        results[0].facts.hostname = "PASSWORD_MARKER"
        results[0].facts.ntp_servers.append("203.0.113.99")
        findings = [f for c in results for f in evaluate(c, self.rules)]
        report = make_report(self.inventory, self.rules, results, findings, "audit", "noncompliant")
        output = json.dumps(report) + markdown(report)
        for secret in ("PASSWORD_MARKER", "SYNTHETIC_NOT_A_CREDENTIAL", "203.0.113.99"):
            self.assertNotIn(secret, output)

    def test_inventory_validation(self):
        base = self.inventory.devices[0].model_dump()
        for update in (
            {"platform": "unsupported"},
            {"host": "999.1.2.3"},
            {"host": "bad host"},
            {"timeout": 0},
            {"timeout": "15"},
            {"port": 65536},
            {"password": "SECRET"},
            {"name": "../escape"},
            {"allowed_operations": ["apply"]},
            {"groups": ["bad group"]},
        ):
            with self.subTest(update=update), self.assertRaises(ValidationError):
                Device(**(base | update))
        with self.assertRaises(ValidationError):
            Inventory(devices=[self.inventory.devices[0]] * 2)

    def test_rule_validation(self):
        base = self.rules.rules[0].model_dump()
        for update in (
            {"check": "eval"},
            {"expected": []},
            {"expected": True},
            {"expected": ["not-an-ip"]},
            {"unknown": "SECRET"},
            {"required_inputs": ["banner"]},
            {"remediation": "automatic"},
            {"platforms": ["cisco_ios", "cisco_ios"]},
        ):
            with self.subTest(update=update), self.assertRaises(ValidationError):
                Rule(**(base | update))
        with self.assertRaises(ValidationError):
            RuleSet(version="1", rules=[self.rules.rules[0]] * 2)

    def test_duplicate_yaml_and_secret_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.yaml"
            for content in (
                "devices: []\ndevices: []",
                "devices: SECRET",
                "!!python/object:bad {}",
            ):
                path.write_text(content)
                with self.assertRaises(InputError) as error:
                    load_inventory(path)
                self.assertNotIn("SECRET", str(error.exception))

    def test_explicit_selection_and_groups(self):
        self.assertEqual(len(select_devices(self.inventory, [], ["access"], False)), 2)
        self.assertEqual(
            select_devices(self.inventory, ["juniper01"], [], False)[0].name, "juniper01"
        )
        for names, groups, all_devices in (
            ([], [], False),
            (["missing"], [], False),
            ([], ["missing"], False),
            (["cisco01"], [], True),
        ):
            with self.assertRaises(InputError):
                select_devices(self.inventory, names, groups, all_devices)

    def test_operation_permission_at_boundary(self):
        device = self.inventory.devices[0].model_copy(update={"allowed_operations": ["collect"]})
        with patch("netops_compliance.collector.get_adapter") as adapter:
            self.assertEqual(collect([device], FIXTURES)[0].error, "operation_not_allowed")
            adapter.assert_not_called()

    def test_capabilities_and_unsupported_methods(self):
        for platform in PLATFORMS:
            adapter = get_adapter(platform)
            self.assertTrue(adapter.capabilities.offline)
            for operation in ("connect", "collect", "backup", "preview", "apply", "verify"):
                with self.subTest(platform=platform, operation=operation):
                    with self.assertRaises(UnsupportedOperation):
                        getattr(adapter, operation)()
        with self.assertRaises(UnsupportedOperation):
            get_adapter("unsupported")

    def cli(self, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return main(list(args))

    def test_cli_reports_exit_codes_and_no_writes(self):
        with (
            tempfile.TemporaryDirectory() as output,
            patch.object(Adapter, "apply") as apply,
            patch.object(Adapter, "backup") as backup,
            patch.object(Adapter, "connect") as connect,
        ):
            for scenario, code in (("compliant", 0), ("noncompliant", 1), ("malformed", 2)):
                self.assertEqual(
                    self.cli(
                        "audit",
                        "--all",
                        "--inventory",
                        str(ROOT / "inventory/lab.example.yaml"),
                        "--rules",
                        str(ROOT / "rules/baseline.yaml"),
                        "--fixture-dir",
                        str(FIXTURES),
                        "--scenario",
                        scenario,
                        "--output",
                        output,
                    ),
                    code,
                )
            apply.assert_not_called()
            backup.assert_not_called()
            connect.assert_not_called()
            reports = list(Path(output).glob("*/report.json"))
            self.assertEqual(len(reports), 3)
            for path in reports:
                report = json.loads(path.read_text())
                self.assertEqual(len(report["findings"]), 24)
                self.assertTrue(report["dry_run"])
                self.assertTrue(path.with_suffix(".md").exists())

    def test_cli_selection_enforced_before_collection(self):
        with patch("netops_compliance.cli.collect") as collector:
            self.assertEqual(
                self.cli(
                    "audit",
                    "--inventory",
                    str(ROOT / "inventory/lab.example.yaml"),
                    "--rules",
                    str(ROOT / "rules/baseline.yaml"),
                ),
                2,
            )
            collector.assert_not_called()

    def test_cli_unsupported_operations_do_not_collect(self):
        with patch("netops_compliance.cli.collect") as collector:
            for args in (
                ("apply", "--all"),
                ("plan", "--all"),
                ("audit", "--all", "--mode", "live"),
            ):
                self.assertEqual(self.cli(*args), 2)
            collector.assert_not_called()

    def test_missing_fixture_does_not_pass(self):
        with tempfile.TemporaryDirectory() as empty:
            results = collect(self.inventory.devices, Path(empty))
        self.assertTrue(all(c.error == "fixture_read_error" for c in results))
        self.assertTrue(
            all(f.status == Status.ERROR for c in results for f in evaluate(c, self.rules))
        )

    def test_html_and_markdown_escaping(self):
        results = collect(self.inventory.devices[:1], FIXTURES)
        findings = evaluate(results[0], self.rules)
        findings[0].expected = "<script>alert(1)</script>|"
        report = make_report(self.inventory, self.rules, results, findings, "audit", "compliant")
        text = markdown(report)
        self.assertNotIn("<script>", text)
        self.assertIn("&lt;script&gt;", text)
        self.assertIn("&#124;", text)


if __name__ == "__main__":
    unittest.main()
