from abc import abstractmethod
from dataclasses import dataclass

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from configurer.RoutingConfigurer import RoutingConfigurer
    from model.devices.Router import Router


@dataclass
class RedistributeConfig:
    connected: bool = False
    static: bool = False


@dataclass
class RoutingConfig:
    redistribute: RedistributeConfig = RedistributeConfig()

    @abstractmethod
    def accept_configurer(self, configurer: 'RoutingConfigurer', router: 'Router') -> None:
        pass
