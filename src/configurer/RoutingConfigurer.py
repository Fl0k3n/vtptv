from configurer.routingutils.RIPConfigXMLGenerator import RIPConfigXMLGenerator

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.routing.RIPConfig import RIPConfig
    from model.devices.Router import Router


class RoutingConfigurer:
    def __init__(self, mgr) -> None:
        self.mgr = mgr

    def configure_rip(self, config: 'RIPConfig', router: 'Router') -> None:
        self.mgr.configure(RIPConfigXMLGenerator.generate(config, router))
