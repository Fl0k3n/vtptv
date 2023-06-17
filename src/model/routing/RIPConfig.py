from dataclasses import dataclass, field
from typing import Tuple, Union

from configurer.RoutingConfigurer import RoutingConfigurer
from model.routing.RoutingConfig import RoutingConfig

import model.devices as devices


@dataclass
class RIPTimers:
    update: int
    timeout: int
    garbage: int


@dataclass
class RIPConfig(RoutingConfig):
    version: int = 2
    enabled_interfaces: list[str] = field(default_factory=list)
    enabled_networks: list[Tuple[str, int]] = field(default_factory=list)
    neighbors: list[str] = field(default_factory=list)
    timers: Union[RIPTimers, None] = None

    def accept_configurer(self, configurer: RoutingConfigurer, router: devices.Router) -> None:
        configurer.configure_rip(self, router)
