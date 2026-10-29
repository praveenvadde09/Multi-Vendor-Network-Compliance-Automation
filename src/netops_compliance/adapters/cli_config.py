"""Strict parser for synthetic IOS/EOS fixture snapshots, not arbitrary show output."""

import ipaddress
import re

from ..models import Facts
from .base import ParseError


def address(value):
    try:
        return str(ipaddress.ip_address(value))
    except ValueError as exc:
        raise ParseError("unsupported address syntax") from exc


def parse_cli(config: str, *, eos: bool) -> Facts:
    lines = config.splitlines()
    if not lines or lines[0] != "! netops-fixture-v1 complete":
        raise ParseError("missing fixture envelope")
    if lines[-1:] != ["end"]:
        raise ParseError("incomplete fixture")
    facts = dict(
        hostname="",
        ntp_servers=[],
        syslog_servers=[],
        ssh_enabled=False,
        telnet_enabled=False,
        banner="",
        enabled_services=[],
        snmp_enabled=False,
    )
    seen = set()
    vtys = []
    ssh_version = False
    ssh_state = None
    telnet_state = None
    service_states = {}
    index = 1
    while index < len(lines) - 1:
        line = lines[index]
        index += 1
        if line in ("", "!"):
            continue
        if line.startswith("hostname "):
            if "hostname" in seen or not re.fullmatch(r"hostname [A-Za-z0-9_-]{1,63}", line):
                raise ParseError("invalid hostname")
            seen.add("hostname")
            facts["hostname"] = line.split()[1]
        elif line.startswith("ntp server "):
            facts["ntp_servers"].append(address(line.removeprefix("ntp server ")))
        elif line.startswith("logging host "):
            facts["syslog_servers"].append(address(line.removeprefix("logging host ")))
        elif line == "ip ssh version 2" and not eos:
            ssh_version = True
        elif line.startswith("line vty ") and not eos:
            match = re.fullmatch(r"line vty (\d+) (\d+)", line)
            if not match or index >= len(lines) - 1:
                raise ParseError("invalid VTY block")
            start, end = map(int, match.groups())
            if not 0 <= start <= end <= 15:
                raise ParseError("unsupported VTY range")
            transport = re.fullmatch(r" transport input (ssh|telnet|ssh telnet|none)", lines[index])
            if not transport:
                raise ParseError("missing explicit VTY transport")
            index += 1
            vtys.append((start, end, transport[1].split()))
        elif line in ("management ssh", "management telnet") and eos:
            if line in seen or index >= len(lines) - 1:
                raise ParseError("invalid management block")
            seen.add(line)
            state = lines[index]
            index += 1
            if state not in ("   shutdown", "   no shutdown"):
                raise ParseError("missing explicit management state")
            if line == "management ssh":
                ssh_state = state == "   no shutdown"
            else:
                telnet_state = state == "   no shutdown"
        elif (
            line
            in (
                "ip http server",
                "no ip http server",
                "ip http secure-server",
                "no ip http secure-server",
            )
            and not eos
        ):
            service = "https" if line.endswith("secure-server") else "http"
            if service in service_states:
                raise ParseError("duplicate service state")
            service_states[service] = not line.startswith("no ")
        elif line in ("management api http-commands",) and eos:
            if "http" in service_states or index >= len(lines) - 1:
                raise ParseError("invalid API block")
            if lines[index] != "   shutdown":
                raise ParseError("only explicitly disabled EOS HTTP API is modeled")
            service_states.update(http=False, https=False)
            index += 1
        elif line.startswith("banner login "):
            if "banner" in seen:
                raise ParseError("duplicate banner")
            seen.add("banner")
            # One-line delimiter form for IOS, EOF block form for EOS.
            if eos:
                if line != "banner login" + " EOF":
                    raise ParseError("unsupported banner syntax")
                body = []
                while index < len(lines) - 1 and lines[index] != "EOF":
                    body.append(lines[index])
                    index += 1
                if index >= len(lines) - 1:
                    raise ParseError("unterminated banner")
                index += 1
                facts["banner"] = "\n".join(body)
            else:
                match = re.fullmatch(r"banner login \^(.+)\^", line)
                if not match:
                    raise ParseError("unsupported banner syntax")
                facts["banner"] = match[1]
        elif re.fullmatch(r"snmp-server community \S+ (ro|rw)", line):
            if "snmp_disabled" in seen:
                raise ParseError("contradictory SNMP state")
            facts["snmp_enabled"] = True
        elif line == "no snmp-server":
            if facts["snmp_enabled"]:
                raise ParseError("contradictory SNMP state")
            seen.add("snmp_disabled")
        else:
            raise ParseError("unrecognized fixture command")
    if not facts["hostname"] or set(service_states) != {"http", "https"}:
        raise ParseError("missing explicit fixture state")
    if eos:
        if ssh_state is None or telnet_state is None:
            raise ParseError("missing explicit management state")
        facts["ssh_enabled"] = ssh_state
        facts["telnet_enabled"] = telnet_state
    else:
        covered = set()
        for start, end, _ in vtys:
            slots = set(range(start, end + 1))
            if covered & slots:
                raise ParseError("overlapping VTY ranges")
            covered |= slots
        if covered != set(range(16)):
            raise ParseError("fixture must explicitly cover VTY 0 through 15")
        facts["ssh_enabled"] = ssh_version and all("ssh" in modes for _, _, modes in vtys)
        facts["telnet_enabled"] = any("telnet" in modes for _, _, modes in vtys)
    facts["enabled_services"] = sorted(k for k, enabled in service_states.items() if enabled)
    for key in ("ntp_servers", "syslog_servers"):
        facts[key] = sorted(set(facts[key]))
    return Facts(**facts)
