# NetOps compliance report

Run: 20261029T222045-70a3b5e425c9

Mode: offline fixture; dry run; no configuration writes.

Rule version: &quot;1.0.0&quot;

Summary: {&quot;pass&quot;: 0, &quot;fail&quot;: 0, &quot;error&quot;: 24, &quot;not-applicable&quot;: 0, &quot;device_errors&quot;: 3}

## Collection

| Device | Platform | Collected | Error |
|---|---|---|---|
| &quot;cisco01&quot; | &quot;cisco_ios&quot; | false | &quot;fixture_parse_error&quot; |
| &quot;arista01&quot; | &quot;arista_eos&quot; | false | &quot;fixture_parse_error&quot; |
| &quot;juniper01&quot; | &quot;juniper_junos&quot; | false | &quot;fixture_parse_error&quot; |

## Findings

| Device | Rule | Severity | Status | Expected | Evidence | Error |
|---|---|---|---|---|---|---|
| &quot;cisco01&quot; | &quot;ntp_required&quot; | &quot;medium&quot; | &quot;error&quot; | [&quot;192.0.2.20&quot;] | null | &quot;fixture_parse_error&quot; |
| &quot;cisco01&quot; | &quot;syslog_required&quot; | &quot;medium&quot; | &quot;error&quot; | [&quot;192.0.2.30&quot;] | null | &quot;fixture_parse_error&quot; |
| &quot;cisco01&quot; | &quot;ssh_required&quot; | &quot;high&quot; | &quot;error&quot; | true | null | &quot;fixture_parse_error&quot; |
| &quot;cisco01&quot; | &quot;telnet_disabled&quot; | &quot;high&quot; | &quot;error&quot; | true | null | &quot;fixture_parse_error&quot; |
| &quot;cisco01&quot; | &quot;banner_required&quot; | &quot;low&quot; | &quot;error&quot; | &quot;Authorized lab access only.&quot; | null | &quot;fixture_parse_error&quot; |
| &quot;cisco01&quot; | &quot;hostname_required&quot; | &quot;low&quot; | &quot;error&quot; | &quot;lab-*&quot; | null | &quot;fixture_parse_error&quot; |
| &quot;cisco01&quot; | &quot;services_disabled&quot; | &quot;high&quot; | &quot;error&quot; | [&quot;http&quot;, &quot;https&quot;, &quot;ftp&quot;] | null | &quot;fixture_parse_error&quot; |
| &quot;cisco01&quot; | &quot;snmp_disabled&quot; | &quot;high&quot; | &quot;error&quot; | true | null | &quot;fixture_parse_error&quot; |
| &quot;arista01&quot; | &quot;ntp_required&quot; | &quot;medium&quot; | &quot;error&quot; | [&quot;192.0.2.20&quot;] | null | &quot;fixture_parse_error&quot; |
| &quot;arista01&quot; | &quot;syslog_required&quot; | &quot;medium&quot; | &quot;error&quot; | [&quot;192.0.2.30&quot;] | null | &quot;fixture_parse_error&quot; |
| &quot;arista01&quot; | &quot;ssh_required&quot; | &quot;high&quot; | &quot;error&quot; | true | null | &quot;fixture_parse_error&quot; |
| &quot;arista01&quot; | &quot;telnet_disabled&quot; | &quot;high&quot; | &quot;error&quot; | true | null | &quot;fixture_parse_error&quot; |
| &quot;arista01&quot; | &quot;banner_required&quot; | &quot;low&quot; | &quot;error&quot; | &quot;Authorized lab access only.&quot; | null | &quot;fixture_parse_error&quot; |
| &quot;arista01&quot; | &quot;hostname_required&quot; | &quot;low&quot; | &quot;error&quot; | &quot;lab-*&quot; | null | &quot;fixture_parse_error&quot; |
| &quot;arista01&quot; | &quot;services_disabled&quot; | &quot;high&quot; | &quot;error&quot; | [&quot;http&quot;, &quot;https&quot;, &quot;ftp&quot;] | null | &quot;fixture_parse_error&quot; |
| &quot;arista01&quot; | &quot;snmp_disabled&quot; | &quot;high&quot; | &quot;error&quot; | true | null | &quot;fixture_parse_error&quot; |
| &quot;juniper01&quot; | &quot;ntp_required&quot; | &quot;medium&quot; | &quot;error&quot; | [&quot;192.0.2.20&quot;] | null | &quot;fixture_parse_error&quot; |
| &quot;juniper01&quot; | &quot;syslog_required&quot; | &quot;medium&quot; | &quot;error&quot; | [&quot;192.0.2.30&quot;] | null | &quot;fixture_parse_error&quot; |
| &quot;juniper01&quot; | &quot;ssh_required&quot; | &quot;high&quot; | &quot;error&quot; | true | null | &quot;fixture_parse_error&quot; |
| &quot;juniper01&quot; | &quot;telnet_disabled&quot; | &quot;high&quot; | &quot;error&quot; | true | null | &quot;fixture_parse_error&quot; |
| &quot;juniper01&quot; | &quot;banner_required&quot; | &quot;low&quot; | &quot;error&quot; | &quot;Authorized lab access only.&quot; | null | &quot;fixture_parse_error&quot; |
| &quot;juniper01&quot; | &quot;hostname_required&quot; | &quot;low&quot; | &quot;error&quot; | &quot;lab-*&quot; | null | &quot;fixture_parse_error&quot; |
| &quot;juniper01&quot; | &quot;services_disabled&quot; | &quot;high&quot; | &quot;error&quot; | [&quot;http&quot;, &quot;https&quot;, &quot;ftp&quot;] | null | &quot;fixture_parse_error&quot; |
| &quot;juniper01&quot; | &quot;snmp_disabled&quot; | &quot;high&quot; | &quot;error&quot; | true | null | &quot;fixture_parse_error&quot; |
