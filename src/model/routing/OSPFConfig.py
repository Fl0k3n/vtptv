from dataclasses import dataclass, field
from typing import Tuple, Union

from configurer.RoutingConfigurer import RoutingConfigurer
from model.routing.RoutingConfig import RoutingConfig

import model.devices as devices

@dataclass
class OSPFConfig(RoutingConfig):
    router_id: str = None
    enabled_networks: list[Tuple[str, int, str]] = field(default_factory=list)

    def accept_configurer(self, configurer: RoutingConfigurer, router: devices.Router) -> None:
        configurer.configure_ospf(self, router)
