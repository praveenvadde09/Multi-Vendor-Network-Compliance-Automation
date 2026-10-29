# NetOps compliance report

Run: 20261029T222044-aa6ea6f4aa0a

Mode: offline fixture; dry run; no configuration writes.

Rule version: &quot;1.0.0&quot;

Summary: {&quot;pass&quot;: 1, &quot;fail&quot;: 23, &quot;error&quot;: 0, &quot;not-applicable&quot;: 0, &quot;device_errors&quot;: 0}

## Collection

| Device | Platform | Collected | Error |
|---|---|---|---|
| &quot;cisco01&quot; | &quot;cisco_ios&quot; | true | null |
| &quot;arista01&quot; | &quot;arista_eos&quot; | true | null |
| &quot;juniper01&quot; | &quot;juniper_junos&quot; | true | null |

## Findings

| Device | Rule | Severity | Status | Expected | Evidence | Error |
|---|---|---|---|---|---|---|
| &quot;cisco01&quot; | &quot;ntp_required&quot; | &quot;medium&quot; | &quot;fail&quot; | [&quot;192.0.2.20&quot;] | [] | null |
| &quot;cisco01&quot; | &quot;syslog_required&quot; | &quot;medium&quot; | &quot;fail&quot; | [&quot;192.0.2.30&quot;] | [] | null |
| &quot;cisco01&quot; | &quot;ssh_required&quot; | &quot;high&quot; | &quot;fail&quot; | true | false | null |
| &quot;cisco01&quot; | &quot;telnet_disabled&quot; | &quot;high&quot; | &quot;fail&quot; | true | true | null |
| &quot;cisco01&quot; | &quot;banner_required&quot; | &quot;low&quot; | &quot;fail&quot; | &quot;Authorized lab access only.&quot; | &quot;missing or different&quot; | null |
| &quot;cisco01&quot; | &quot;hostname_required&quot; | &quot;low&quot; | &quot;fail&quot; | &quot;lab-*&quot; | &quot;different naming pattern&quot; | null |
| &quot;cisco01&quot; | &quot;services_disabled&quot; | &quot;high&quot; | &quot;fail&quot; | [&quot;http&quot;, &quot;https&quot;, &quot;ftp&quot;] | [&quot;http&quot;] | null |
| &quot;cisco01&quot; | &quot;snmp_disabled&quot; | &quot;high&quot; | &quot;fail&quot; | true | true | null |
| &quot;arista01&quot; | &quot;ntp_required&quot; | &quot;medium&quot; | &quot;fail&quot; | [&quot;192.0.2.20&quot;] | [] | null |
| &quot;arista01&quot; | &quot;syslog_required&quot; | &quot;medium&quot; | &quot;fail&quot; | [&quot;192.0.2.30&quot;] | [] | null |
| &quot;arista01&quot; | &quot;ssh_required&quot; | &quot;high&quot; | &quot;fail&quot; | true | false | null |
| &quot;arista01&quot; | &quot;telnet_disabled&quot; | &quot;high&quot; | &quot;fail&quot; | true | true | null |
| &quot;arista01&quot; | &quot;banner_required&quot; | &quot;low&quot; | &quot;fail&quot; | &quot;Authorized lab access only.&quot; | &quot;missing or different&quot; | null |
| &quot;arista01&quot; | &quot;hostname_required&quot; | &quot;low&quot; | &quot;fail&quot; | &quot;lab-*&quot; | &quot;different naming pattern&quot; | null |
| &quot;arista01&quot; | &quot;services_disabled&quot; | &quot;high&quot; | &quot;pass&quot; | [&quot;http&quot;, &quot;https&quot;, &quot;ftp&quot;] | [] | null |
| &quot;arista01&quot; | &quot;snmp_disabled&quot; | &quot;high&quot; | &quot;fail&quot; | true | true | null |
| &quot;juniper01&quot; | &quot;ntp_required&quot; | &quot;medium&quot; | &quot;fail&quot; | [&quot;192.0.2.20&quot;] | [] | null |
| &quot;juniper01&quot; | &quot;syslog_required&quot; | &quot;medium&quot; | &quot;fail&quot; | [&quot;192.0.2.30&quot;] | [] | null |
| &quot;juniper01&quot; | &quot;ssh_required&quot; | &quot;high&quot; | &quot;fail&quot; | true | false | null |
| &quot;juniper01&quot; | &quot;telnet_disabled&quot; | &quot;high&quot; | &quot;fail&quot; | true | true | null |
| &quot;juniper01&quot; | &quot;banner_required&quot; | &quot;low&quot; | &quot;fail&quot; | &quot;Authorized lab access only.&quot; | &quot;missing or different&quot; | null |
| &quot;juniper01&quot; | &quot;hostname_required&quot; | &quot;low&quot; | &quot;fail&quot; | &quot;lab-*&quot; | &quot;different naming pattern&quot; | null |
| &quot;juniper01&quot; | &quot;services_disabled&quot; | &quot;high&quot; | &quot;fail&quot; | [&quot;http&quot;, &quot;https&quot;, &quot;ftp&quot;] | [&quot;http&quot;] | null |
| &quot;juniper01&quot; | &quot;snmp_disabled&quot; | &quot;high&quot; | &quot;fail&quot; | true | true | null |
