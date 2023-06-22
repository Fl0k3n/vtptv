import logging
from pathlib import Path

from configurer.DeviceInitializer import DeviceInitializer
from configurer.VirtualConfigurer import VirtualConfigurer
from model.devices.Router import Router
from model.devices.Switch import Switch
from model.Topology import Topology


class PhysicalToVirtualConverter:
    def __init__(self, device_initializer: DeviceInitializer, configurer: VirtualConfigurer) -> None:
        self.device_initializer = device_initializer
        self.configurer = configurer

    def convert(self, routers_count: int, switches_count: int) -> Topology:
        logging.debug("initializing devices")
        routers, switches = self._initialize_devices(
            routers_count, switches_count)

        logging.debug("reading physical configuration")
        self._read_physical_configs(routers, switches)

        logging.debug("building topology")
        return self._build_topology(routers, switches)

    def save_as_kathara_file_tree(self, topo: Topology, root_dir: Path):
        pass

    def _build_topology(self, routers: list[Router], switches: list[Switch]) -> Topology:
        # TODO setup connections
        return Topology(routers + switches)

    def _read_physical_configs(self, routers: list[Router], switches: list[Switch]):
        for router in routers:
            self.configurer.configure_router(router)

        for switch in switches:
            self.configurer.configure_switch(switch)

    def _initialize_devices(self, routers_count: int, switches_count: int) -> tuple[list[Router], list[Switch]]:
        routers, switches = [], []

        for i in range(routers_count):
            routers.append(self.device_initializer.init_router_from_physical(
                self._router_name(i)))

        for i in range(switches_count):
            switches.append(
                self.device_initializer.init_switch_from_physical(self._switch_name(i)))

        return Topology(routers + switches)

    def _router_name(self, idx: int) -> str:
        return f'r{idx}'

    def _switch_name(self, idx: int) -> str:
        return f's{idx}'
