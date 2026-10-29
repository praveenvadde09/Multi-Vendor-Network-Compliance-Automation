"""Pure deterministic rule evaluation; applicability precedes required data checks."""

from fnmatch import fnmatchcase
from ipaddress import ip_address

from .models import REQUIRED, Finding, Status


def evaluate(collection, rules):
    findings = []
    for rule in rules.rules:
        status, observed, error = Status.ERROR, None, None
        if collection.platform not in rule.platforms:
            status = Status.NOT_APPLICABLE
        elif collection.error or collection.facts is None:
            error = collection.error or "required_data_unavailable"
        else:
            value = getattr(collection.facts, REQUIRED[rule.check])
            if rule.check in ("ntp_servers_include", "syslog_servers_include"):
                expected = {str(ip_address(v)) for v in rule.expected}
                passed = expected <= set(value)
                observed = sorted(expected & set(value))  # Never expose unapproved endpoints.
            elif rule.check == "services_disabled":
                observed = sorted(set(rule.expected) & set(value))
                passed = not observed
            elif rule.check in ("telnet_disabled", "snmp_disabled"):
                observed, passed = value, not value
            elif rule.check == "ssh_enabled":
                observed, passed = value, value
            elif rule.check == "banner_equals":
                passed = value == rule.expected
                observed = "matches baseline" if passed else "missing or different"
            else:
                passed = fnmatchcase(value, rule.expected)
                observed = "matches naming pattern" if passed else "different naming pattern"
            status = Status.PASS if passed else Status.FAIL
        findings.append(
            Finding(
                device=collection.device,
                rule_id=rule.id,
                severity=rule.severity,
                status=status,
                expected=rule.expected,
                observed=observed,
                error=error,
            )
        )
    return findings
