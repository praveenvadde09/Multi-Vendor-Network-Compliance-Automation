from .base import Adapter
from .cli_config import parse_cli


class CiscoAdapter(Adapter):
    def normalize(self, config):
        return parse_cli(config, eos=False)
