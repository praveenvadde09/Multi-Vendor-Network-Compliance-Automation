# Fixture contract, version 1

Fixtures are synthetic complete snapshots of a **restricted configuration model**,
not general device configurations. Do not paste a production running configuration
into this format. Every unrecognized command fails the device's collection;
the parser does not quietly ignore unknown security configuration.

IOS/EOS begin with `! netops-fixture-v1 complete` and end with `end`.
Junos begins with `# netops-fixture-v1 complete` and ends with `# end-fixture`.
The envelopes declare completeness for this lab model, not for real hardware.
Missing envelopes are errors. Blank lines are accepted.

| Data | IOS | EOS | Junos |
|---|---|---|---|
| Hostname | hostname NAME | hostname NAME | set system host-name NAME |
| NTP | ntp server IP | ntp server IP | set system ntp server IP |
| Syslog | logging host IP | logging host IP | set system syslog host IP any info |
| SSH | ip ssh version 2 + every modeled VTY permits ssh | management ssh + explicit shutdown/no shutdown | set system services ssh |
| Telnet | Any modeled VTY permits telnet | management telnet + explicit shutdown/no shutdown | set system services telnet |
| Banner | banner login ^TEXT^ | banner login EOF / TEXT / EOF | set system login message "TEXT" |
| HTTP/HTTPS | explicit ip http server and secure-server, each optionally prefixed no | management api http-commands + shutdown only | set system services web-management http/https |
| FTP | absent in restricted grammar; any FTP command is an error | absent in restricted grammar; any FTP command is an error | set system services ftp |
| SNMP | snmp-server community TOKEN ro/rw; or no snmp-server | same as IOS | set snmp community TOKEN authorization read-only/read-write |

IOS VTY blocks require the exact one-space-indented `transport input` line.
Supported modes: `ssh`, `telnet`, `ssh telnet`, `none`.
Ranges must cover 0â€“15 exactly once; other device VTY layouts are unsupported.
EOS management children use three spaces. Its HTTP API is modeled only when
explicitly shut down; enabled or ambiguous API syntax returns error.

Junos configuration must be flattened set syntax, without groups/inheritance,
inactive statements, bracket lists or unexpanded variables. Absence of services
means absent only inside this declared-complete synthetic model.
All destination values must be literal IP addresses. DNS names, VRFs, source
interfaces, NTP authentication, SNMPv3 and arbitrary vendor options are unsupported.

IOS banners are single-line caret-delimited; EOS uses EOF; Junos banners cannot
contain escaped quotes or backslashes. A missing banner in a valid snapshot is
noncompliant, not a parser error. Missing mandatory hostname or explicit IOS/EOS
service state is an error. NTP/syslog absence is valid normalized empty state.
Duplicate endpoint entries normalize to a sorted set.

The noncompliant EOS fixture deliberately keeps the HTTP API disabled: it has
seven failures and one pass. IOS/Junos noncompliant fixtures each have eight failures.
SNMP tokens in fixtures are obvious synthetic markers. Reports expose only the
SNMP enabled boolean.
