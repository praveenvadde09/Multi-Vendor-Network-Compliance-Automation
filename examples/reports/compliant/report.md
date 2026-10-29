# NetOps compliance report

Run: 20261029T222044-f85a8189a6d3

Mode: offline fixture; dry run; no configuration writes.

Rule version: &quot;1.0.0&quot;

Summary: {&quot;pass&quot;: 24, &quot;fail&quot;: 0, &quot;error&quot;: 0, &quot;not-applicable&quot;: 0, &quot;device_errors&quot;: 0}

## Collection

| Device | Platform | Collected | Error |
|---|---|---|---|
| &quot;cisco01&quot; | &quot;cisco_ios&quot; | true | null |
| &quot;arista01&quot; | &quot;arista_eos&quot; | true | null |
| &quot;juniper01&quot; | &quot;juniper_junos&quot; | true | null |

## Findings

| Device | Rule | Severity | Status | Expected | Evidence | Error |
|---|---|---|---|---|---|---|
| &quot;cisco01&quot; | &quot;ntp_required&quot; | &quot;medium&quot; | &quot;pass&quot; | [&quot;192.0.2.20&quot;] | [&quot;192.0.2.20&quot;] | null |
| &quot;cisco01&quot; | &quot;syslog_required&quot; | &quot;medium&quot; | &quot;pass&quot; | [&quot;192.0.2.30&quot;] | [&quot;192.0.2.30&quot;] | null |
| &quot;cisco01&quot; | &quot;ssh_required&quot; | &quot;high&quot; | &quot;pass&quot; | true | true | null |
| &quot;cisco01&quot; | &quot;telnet_disabled&quot; | &quot;high&quot; | &quot;pass&quot; | true | false | null |
| &quot;cisco01&quot; | &quot;banner_required&quot; | &quot;low&quot; | &quot;pass&quot; | &quot;Authorized lab access only.&quot; | &quot;matches baseline&quot; | null |
| &quot;cisco01&quot; | &quot;hostname_required&quot; | &quot;low&quot; | &quot;pass&quot; | &quot;lab-*&quot; | &quot;matches naming pattern&quot; | null |
| &quot;cisco01&quot; | &quot;services_disabled&quot; | &quot;high&quot; | &quot;pass&quot; | [&quot;http&quot;, &quot;https&quot;, &quot;ftp&quot;] | [] | null |
| &quot;cisco01&quot; | &quot;snmp_disabled&quot; | &quot;high&quot; | &quot;pass&quot; | true | false | null |
| &quot;arista01&quot; | &quot;ntp_required&quot; | &quot;medium&quot; | &quot;pass&quot; | [&quot;192.0.2.20&quot;] | [&quot;192.0.2.20&quot;] | null |
| &quot;arista01&quot; | &quot;syslog_required&quot; | &quot;medium&quot; | &quot;pass&quot; | [&quot;192.0.2.30&quot;] | [&quot;192.0.2.30&quot;] | null |
| &quot;arista01&quot; | &quot;ssh_required&quot; | &quot;high&quot; | &quot;pass&quot; | true | true | null |
| &quot;arista01&quot; | &quot;telnet_disabled&quot; | &quot;high&quot; | &quot;pass&quot; | true | false | null |
| &quot;arista01&quot; | &quot;banner_required&quot; | &quot;low&quot; | &quot;pass&quot; | &quot;Authorized lab access only.&quot; | &quot;matches baseline&quot; | null |
| &quot;arista01&quot; | &quot;hostname_required&quot; | &quot;low&quot; | &quot;pass&quot; | &quot;lab-*&quot; | &quot;matches naming pattern&quot; | null |
| &quot;arista01&quot; | &quot;services_disabled&quot; | &quot;high&quot; | &quot;pass&quot; | [&quot;http&quot;, &quot;https&quot;, &quot;ftp&quot;] | [] | null |
| &quot;arista01&quot; | &quot;snmp_disabled&quot; | &quot;high&quot; | &quot;pass&quot; | true | false | null |
| &quot;juniper01&quot; | &quot;ntp_required&quot; | &quot;medium&quot; | &quot;pass&quot; | [&quot;192.0.2.20&quot;] | [&quot;192.0.2.20&quot;] | null |
| &quot;juniper01&quot; | &quot;syslog_required&quot; | &quot;medium&quot; | &quot;pass&quot; | [&quot;192.0.2.30&quot;] | [&quot;192.0.2.30&quot;] | null |
| &quot;juniper01&quot; | &quot;ssh_required&quot; | &quot;high&quot; | &quot;pass&quot; | true | true | null |
| &quot;juniper01&quot; | &quot;telnet_disabled&quot; | &quot;high&quot; | &quot;pass&quot; | true | false | null |
| &quot;juniper01&quot; | &quot;banner_required&quot; | &quot;low&quot; | &quot;pass&quot; | &quot;Authorized lab access only.&quot; | &quot;matches baseline&quot; | null |
| &quot;juniper01&quot; | &quot;hostname_required&quot; | &quot;low&quot; | &quot;pass&quot; | &quot;lab-*&quot; | &quot;matches naming pattern&quot; | null |
| &quot;juniper01&quot; | &quot;services_disabled&quot; | &quot;high&quot; | &quot;pass&quot; | [&quot;http&quot;, &quot;https&quot;, &quot;ftp&quot;] | [] | null |
| &quot;juniper01&quot; | &quot;snmp_disabled&quot; | &quot;high&quot; | &quot;pass&quot; | true | false | null |
