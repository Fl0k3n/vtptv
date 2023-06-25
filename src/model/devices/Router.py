from typing import TYPE_CHECKING

from model.devices.Node import Node, NodeRole
from model.links.Interface import Interface
from model.routing.RoutingConfig import OSPFConfig, RIPConfig
from model.translations.Nat import DNat, OverloadNat, SNat

if TYPE_CHECKING:
    from configurer.DeviceInitializer import DeviceInitializer
    from configurer.DeviceConfigurer import DeviceConfigurer

from model.devices.CiscoNetworkNode import CiscoNetworkNode


class Router(CiscoNetworkNode):
    def __init__(self, name: str, interfaces: list[Interface], neighbours: set[Node] = None) -> None:
        super().__init__(name, interfaces, neighbours)
        self.snat_rules: list[SNat] = []
        self.dnat_rules: list[DNat] = []
        self.overload_nat_rules: list[OverloadNat] = []
        self.rip_config: RIPConfig = None
        self.ospf_config: OSPFConfig = None

    def accept_physical_initializer(self, initilizer: 'DeviceInitializer') -> None:
        initilizer.init_router(self)

    def accept_physical_configurer(self, configurer: 'DeviceConfigurer') -> None:
        configurer.configure_router(self)

    @property
    def role(self) -> NodeRole:
        return NodeRole.ROUTER
