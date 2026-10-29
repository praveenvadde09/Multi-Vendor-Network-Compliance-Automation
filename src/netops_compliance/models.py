"""Strict input schemas and normalized facts."""

import ipaddress
import re
from enum import StrEnum
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Platform = Literal["cisco_ios", "arista_eos", "juniper_junos"]
PLATFORMS = ("cisco_ios", "arista_eos", "juniper_junos")
Check = Literal[
    "ntp_servers_include",
    "syslog_servers_include",
    "ssh_enabled",
    "telnet_disabled",
    "banner_equals",
    "hostname_matches",
    "services_disabled",
    "snmp_disabled",
]
REQUIRED = {
    "ntp_servers_include": "ntp_servers",
    "syslog_servers_include": "syslog_servers",
    "ssh_enabled": "ssh_enabled",
    "telnet_disabled": "telnet_enabled",
    "banner_equals": "banner",
    "hostname_matches": "hostname",
    "services_disabled": "enabled_services",
    "snmp_disabled": "snmp_enabled",
}


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


def identifier(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", value):
        raise ValueError("invalid identifier")
    return value


class Device(StrictModel):
    name: str
    host: str
    platform: Platform
    credential_ref: str
    groups: list[str] = Field(default_factory=list)
    port: int = Field(default=22, ge=1, le=65535)
    timeout: int = Field(default=15, ge=1, le=120)
    allowed_operations: list[Literal["collect", "audit"]] = Field(
        default_factory=lambda: ["collect", "audit"]
    )

    _names = field_validator("name", "credential_ref")(identifier)

    @field_validator("host")
    @classmethod
    def valid_host(cls, value: str) -> str:
        try:
            ipaddress.ip_address(value)
            return value
        except ValueError:
            pass
        if (
            len(value) > 253
            or re.fullmatch(r"[0-9.]+", value)
            or not all(
                re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", p)
                for p in value.split(".")
            )
        ):
            raise ValueError("invalid address")
        return value

    @field_validator("groups", "allowed_operations")
    @classmethod
    def unique_values(cls, values: list[str]) -> list[str]:
        for value in values:
            identifier(value)
        if len(values) != len(set(values)):
            raise ValueError("duplicate values")
        return values


class Inventory(StrictModel):
    devices: list[Device] = Field(min_length=1)

    @model_validator(mode="after")
    def unique_names(self) -> Self:
        names = [d.name for d in self.devices]
        if len(names) != len(set(names)):
            raise ValueError("duplicate device names")
        return self


class Rule(StrictModel):
    id: str
    description: str = Field(min_length=1, max_length=300)
    severity: Literal["low", "medium", "high", "critical"]
    platforms: list[Platform] = Field(min_length=1)
    required_inputs: list[str]
    check: Check
    expected: str | bool | list[str]
    remediation: Literal["manual"] = "manual"

    _id = field_validator("id")(identifier)

    @model_validator(mode="after")
    def coherent(self) -> Self:
        if len(self.platforms) != len(set(self.platforms)):
            raise ValueError("duplicate platforms")
        if self.required_inputs != [REQUIRED[self.check]]:
            raise ValueError("required_inputs must match normalized field")
        if self.check in ("ntp_servers_include", "syslog_servers_include", "services_disabled"):
            if not isinstance(self.expected, list) or not self.expected:
                raise ValueError("expected must be a nonempty list")
            if len(self.expected) != len(set(self.expected)):
                raise ValueError("duplicate expected values")
            if self.check == "services_disabled":
                if not set(self.expected) <= {"http", "https", "ftp"}:
                    raise ValueError("unsupported service")
            else:
                for value in self.expected:
                    ipaddress.ip_address(value)
        elif self.check in ("ssh_enabled", "telnet_disabled", "snmp_disabled"):
            if self.expected is not True:
                raise ValueError("expected must be true for boolean checks")
        elif not isinstance(self.expected, str) or not self.expected or len(self.expected) > 500:
            raise ValueError("expected must be a nonempty bounded string")
        if self.check == "hostname_matches":
            if not re.fullmatch(r"[A-Za-z0-9*?_-]+", self.expected):
                raise ValueError("use a hostname glob with letters, digits, _, -, *, ?")
        return self


class RuleSet(StrictModel):
    version: str = Field(min_length=1, max_length=64)
    rules: list[Rule] = Field(min_length=1)

    @model_validator(mode="after")
    def unique_ids(self) -> Self:
        ids = [r.id for r in self.rules]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate rule IDs")
        return self


class Facts(StrictModel):
    hostname: str
    ntp_servers: list[str]
    syslog_servers: list[str]
    ssh_enabled: bool
    telnet_enabled: bool
    banner: str
    enabled_services: list[str]
    snmp_enabled: bool


class Status(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"
    NOT_APPLICABLE = "not-applicable"


class Collection(StrictModel):
    device: str
    platform: Platform
    facts: Facts | None = None
    baseline_hash: str | None = None
    error: str | None = None


class Finding(StrictModel):
    device: str
    rule_id: str
    severity: str
    status: Status
    expected: str | bool | list[str]
    observed: str | bool | list[str] | None
    error: str | None = None
