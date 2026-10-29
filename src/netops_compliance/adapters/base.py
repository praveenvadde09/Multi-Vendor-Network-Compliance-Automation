"""No transport or write implementation is enabled in this release."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..models import Facts


class ParseError(ValueError):
    pass


class UnsupportedOperation(RuntimeError):
    pass


@dataclass(frozen=True)
class Capabilities:
    offline: bool = True
    live_collect: bool = False
    backup: bool = False
    preview: bool = False
    apply: bool = False
    verify: bool = False
    persistence: bool = False
    rollback: bool = False


class Adapter(ABC):
    capabilities = Capabilities()

    @abstractmethod
    def normalize(self, config: str) -> Facts:
        """Parse the documented fixture grammar or raise ParseError."""

    def connect(self, *args, **kwargs):
        raise UnsupportedOperation("live collection is not implemented")

    def collect(self, *args, **kwargs):
        raise UnsupportedOperation("live collection is not implemented")

    def backup(self, *args, **kwargs):
        raise UnsupportedOperation("backup is not implemented")

    def preview(self, *args, **kwargs):
        raise UnsupportedOperation("remediation planning is not implemented")

    def apply(self, *args, **kwargs):
        raise UnsupportedOperation("configuration writes are not implemented")

    def verify(self, *args, **kwargs):
        raise UnsupportedOperation("live verification is not implemented")
