import logging

from configurer.hints.hints import (ConfigurationHintsExtractor,
                                    RouterConfigurationHint)
from configurer.netconfutils.NetconfManager import NetconfManager
from model.devices.Router import Router
from model.devices.Switch import Switch
from utils.userio import require_router_netconf_port_connected

'''
Configures virtual device representation based on physical configuration.
'''
class VirtualConfigurer:
    def __init__(self, netconf_mgr: NetconfManager, hints_extractor: ConfigurationHintsExtractor) -> None:
        self.netconf_mgr = netconf_mgr
        self.hints_extractor = hints_extractor

    def configure_router(self, router: Router) -> None:
        hints = set(self.hints_extractor.extract_router_config_hints(router.running_conf_data))

        if hints:
            logging.debug(f'router {router.name}: Got configuration hints: {hints}')
        else:
            logging.info(f'router {router.name}: Failed to extract any configuration hint, assuming router is not configured')
            return

        require_router_netconf_port_connected(router.name, router.netconf_interface.physical_name)

        if RouterConfigurationHint.IP_INTERFACE in hints:
            self._setup_ip_interface_config(router)
        if RouterConfigurationHint.RIP in hints:
            self._setup_rip_config(router)
            

    def _setup_ip_interface_config(self, router: Router) -> None:
        pass

    def _setup_rip_config(self, router: Router) -> None:
        pass

    def configure_switch(self, switch: Switch) -> None:
        pass
