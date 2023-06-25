from configurer.netconfutils.NetconfManager import NetconfManager
from configurer.netconfutils.protocols.ospf import generate_ospf_xml
from configurer.netconfutils.protocols.rip import generate_rip_xml
from model.devices.Host import Host
from model.devices.Node import Node
from model.devices.Router import Router
from model.devices.Switch import Switch
from utils.userio import require_router_netconf_port_connected


class DeviceConfigurer:
    """
    Configures physical devices based on virtual configuration.
    """

    def __init__(self, netconf_mgr: NetconfManager) -> None:
        self.netconf_mgr = netconf_mgr

    def configure_router(self, router: Router) -> None:
        # TODO
        print(
            "Assert interface of this PC has interface in same network as router (see .env)")
        require_router_netconf_port_connected(
            router.name, router.netconf_interface.physical_name)

        with self.netconf_mgr:
            self._configure_interfaces(router)
            self._configure_static_routes(router)
            self._configure_routing(router)

    def configure_switch(self, switch: Switch) -> None:
        pass

    def configure_host(self, host: Host) -> None:
        pass

    def _configure_interfaces(self, node: Node) -> None:
        for iface in node.interfaces.values():
            self.netconf_mgr.configure_interface(
                iface.physical_name, iface.ipv4, iface.netmask, iface.enabled)

    def _configure_static_routes(self, node: Node) -> None:
        for static_route in node.static_routes:
            self.netconf_mgr.configure_static_route(static_route)

    def _configure_routing(self, router: Router) -> None:
        xml_configs = []
        if router.rip_config is not None:
            xml_configs.append(generate_rip_xml(router))
        if router.ospf_config is not None:
            xml_configs.append(generate_ospf_xml(router))

        for netconf_xml in xml_configs:
            self.netconf_mgr.configure(netconf_xml)
