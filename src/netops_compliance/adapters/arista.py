from .base import Adapter
from .cli_config import parse_cli


class AristaAdapter(Adapter):
    def normalize(self, config):
        return parse_cli(config, eos=True)
