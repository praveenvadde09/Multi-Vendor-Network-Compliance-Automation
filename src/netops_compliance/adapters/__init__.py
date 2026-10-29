from .arista import AristaAdapter
from .base import UnsupportedOperation
from .cisco import CiscoAdapter
from .juniper import JuniperAdapter

ADAPTERS = {"cisco_ios": CiscoAdapter, "arista_eos": AristaAdapter, "juniper_junos": JuniperAdapter}


def get_adapter(platform):
    if platform not in ADAPTERS:
        raise UnsupportedOperation("unsupported platform")
    return ADAPTERS[platform]()
