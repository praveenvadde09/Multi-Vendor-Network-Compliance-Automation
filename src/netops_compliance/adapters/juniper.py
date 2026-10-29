"""Parse complete synthetic Junos display-set fixtures."""

import re

from ..models import Facts
from .base import Adapter, ParseError
from .cli_config import address


class JuniperAdapter(Adapter):
    def normalize(self, config):
        lines = config.splitlines()
        if (
            not lines
            or lines[0] != "# netops-fixture-v1 complete"
            or lines[-1:] != ["# end-fixture"]
        ):
            raise ParseError("incomplete fixture envelope")
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
        for line in lines[1:-1]:
            if not line or line.startswith("#"):
                continue
            if re.fullmatch(r"set system host-name [A-Za-z0-9_-]{1,63}", line):
                if facts["hostname"]:
                    raise ParseError("duplicate hostname")
                facts["hostname"] = line.split()[-1]
            elif line.startswith("set system ntp server "):
                facts["ntp_servers"].append(address(line.removeprefix("set system ntp server ")))
            elif line.startswith("set system syslog host "):
                match = re.fullmatch(r"set system syslog host (\S+) any info", line)
                if not match:
                    raise ParseError("unsupported syslog syntax")
                facts["syslog_servers"].append(address(match[1]))
            elif line in ("set system services ssh", "set system services telnet"):
                facts["ssh_enabled" if line.endswith("ssh") else "telnet_enabled"] = True
            elif line in (
                "set system services ftp",
                "set system services web-management http",
                "set system services web-management https",
            ):
                facts["enabled_services"].append(line.split()[-1])
            elif line.startswith("set system login message "):
                match = re.fullmatch(r'set system login message "([^"\\]*)"', line)
                if not match or facts["banner"]:
                    raise ParseError("unsupported login message")
                facts["banner"] = match[1]
            elif re.fullmatch(r"set snmp community \S+ authorization read-(only|write)", line):
                facts["snmp_enabled"] = True
            else:
                raise ParseError("unrecognized fixture command")
        if not facts["hostname"]:
            raise ParseError("missing hostname")
        for key in ("ntp_servers", "syslog_servers", "enabled_services"):
            facts[key] = sorted(set(facts[key]))
        return Facts(**facts)
