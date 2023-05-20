from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from configurer.DeviceInitializer import DeviceInitializer

from model.devices.Node import Node


class Host(Node):
    def accept_physical_initializer(self, initilizer: 'DeviceInitializer') -> None:
        initilizer.init_host(self)
