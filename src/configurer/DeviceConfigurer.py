import logging

from configurer.netconfutils.NetconfManager import NetconfManager
from model.devices.Host import Host
from model.devices.Router import Router
from model.devices.Switch import Switch
from utils.userio import require_router_netconf_port_connected


class DeviceConfigurer:
    def __init__(self, netconf_mgr: NetconfManager) -> None:
        self.netconf_mgr = netconf_mgr

    def configure_router(self, router: Router) -> None:
        print("Assert interface of this PC has 9.9.9.10/24 ip addr")  # TODO
        require_router_netconf_port_connected(
            router.name, router.netconf_interface.physical_name)

        with self.netconf_mgr as mgr:
            for iface in router.interfaces.values():
                logging.debug(f"initializing {iface} with netconf")
                mgr.configure_interface(
                    iface.physical_name, iface.ipv4, iface.netmask, iface.enabled)

    def configure_switch(self, switch: Switch) -> None:
        pass

    def configure_host(self, host: Host) -> None:
        pass
