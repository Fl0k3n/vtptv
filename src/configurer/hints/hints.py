from enum import Enum
from typing import Iterator


class RouterConfigurationHint(Enum):
    IP_INTERFACE = 0
    STATIC_ROUTING = 1
    RIP = 2
    OSPF = 3
    BGP = 4

class SwitchConfigurationHint(Enum):
    VLAN = 0

"""
Hints extractor that is required to return hints about things that could have been configured.
It can return invalid hints (meaning the configured thing wasn't/isn't configured anymore).
"""
class ConfigurationHintsExtractor:
    _RUN_CONF_DELIM = '!'

    def extract_router_config_hints(self, router_running_cfg: str) -> list[RouterConfigurationHint]:
        hints = []

        lines_iter = iter(router_running_cfg.splitlines())
        for line in lines_iter:
            if line.startswith('router ospf'):
                hints.append(RouterConfigurationHint.OSPF)
            elif line.startswith('router rip'):
                hints.append(RouterConfigurationHint.RIP)
            elif line.startswith('router bgp'):
                hints.append(RouterConfigurationHint.BGP)
            elif line.startswith('ip route'):
                hints.append(RouterConfigurationHint.STATIC_ROUTING)
            elif line.startswith('interface') and \
                any(line.strip().startswith('ip address') for line in self._lines_before_run_conf_delim(lines_iter)):
                hints.append(RouterConfigurationHint.IP_INTERFACE)

        return hints
        
    def _lines_before_run_conf_delim(self, lines_iter: Iterator[str]) -> list[str]:
        return [line for line in lines_iter if not line.strip().startswith(self._RUN_CONF_DELIM)]

    def extract_switch_config_hints(self, switch_running_cfg: str) -> list[SwitchConfigurationHint]:
        # TODO
        return []