from typing import TYPE_CHECKING

from configurer.netconfutils.protocols.ospf import generate_ospf_xml
from configurer.netconfutils.protocols.rip import generate_rip_xml

if TYPE_CHECKING:
    from model.devices.Router import Router
    from model.routing.OSPFConfig import OSPFConfig
    from model.routing.RIPConfig import RIPConfig


class RoutingConfigurer:
    def __init__(self, mgr) -> None:
        self.mgr = mgr

    def configure_rip(self, config: 'RIPConfig', router: 'Router') -> None:
        self.mgr.configure(generate_rip_xml(config, router))

    def configure_ospf(self, config: 'OSPFConfig', router: 'Router') -> None:
        self.mgr.configure(generate_ospf_xml(config, router))
