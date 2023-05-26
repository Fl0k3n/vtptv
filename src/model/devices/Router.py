from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from configurer.DeviceInitializer import DeviceInitializer
    from configurer.DeviceConfigurer import DeviceConfigurer

from model.devices.Node import Node
from model.links.Interface import Interface


class Router(Node):
    def __init__(self, name: str, interfaces: list[Interface], neighbours: set[Node] = None) -> None:
        super().__init__(name, interfaces, neighbours)
        self.netconf_interface: Interface = None

    def accept_physical_initializer(self, initilizer: 'DeviceInitializer') -> None:
        initilizer.init_router(self)

    def accept_physical_configurer(self, configurer: 'DeviceConfigurer') -> None:
        configurer.configure_router(self)
