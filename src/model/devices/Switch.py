from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from configurer.DeviceInitializer import DeviceInitializer
    from configurer.DeviceConfigurer import DeviceConfigurer

from model.devices.Node import Node


class Switch(Node):
    def accept_physical_initializer(self, initilizer: 'DeviceInitializer') -> None:
        initilizer.init_switch(self)

    def accept_physical_configurer(self, configurer: 'DeviceConfigurer') -> None:
        configurer.configure_switch(self)
