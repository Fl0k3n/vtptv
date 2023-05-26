from model.devices.Host import Host
from model.devices.Router import Router
from model.devices.Switch import Switch
from utils.userio import require_router_netconf_port_connected


class DeviceConfigurer:
    def __init__(self) -> None:
        pass

    def configure_router(self, router: Router) -> None:
        require_router_netconf_port_connected(
            router.name, router.netconf_interface.physical_name)

    def configure_switch(self, switch: Switch) -> None:
        pass

    def configure_host(self, host: Host) -> None:
        pass
