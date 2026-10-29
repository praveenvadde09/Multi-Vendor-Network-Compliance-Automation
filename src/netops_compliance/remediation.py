"""Reserved remediation boundary: reject rather than silently simulate support."""

from .adapters.base import UnsupportedOperation


def plan(*args, **kwargs):
    raise UnsupportedOperation("planning is unavailable; all rules require manual remediation")


def apply(*args, **kwargs):
    raise UnsupportedOperation("apply is unavailable in the offline release")
