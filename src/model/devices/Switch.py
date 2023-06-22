from typing import TYPE_CHECKING

from model.devices.Node import NodeRole

if TYPE_CHECKING:
    from configurer.DeviceInitializer import DeviceInitializer
    from configurer.DeviceConfigurer import DeviceConfigurer

from model.devices.CiscoNetworkNode import CiscoNetworkNode


class Switch(CiscoNetworkNode):
    def accept_physical_initializer(self, initilizer: 'DeviceInitializer') -> None:
        initilizer.init_switch(self)

    def accept_physical_configurer(self, configurer: 'DeviceConfigurer') -> None:
        configurer.configure_switch(self)

    @property
    def role(self) -> NodeRole:
        return NodeRole.SWITCH
