import logging
from parser.VirtualDeviceCommandsParser import VirtualDeviceCommandsParser

from Kathara.parser.netkit.LabParser import LabParser

from configurer.DeviceInitializer import DeviceInitializer
from configurer.utils.DeviceConsolePortManager import DeviceConsolePortManager
from mapper.VirtualDeviceBuilder import VirtualDeviceBuilder
from mapper.VirtualTopologyBuilder import VirtualTopologyBuilder
from model.Topology import Topology


class VirtualToPhysicalConverter:
    def __init__(self, kathara_lab_path: str, device_initializer: DeviceInitializer) -> None:
        self.kathara_lab_path = kathara_lab_path
        self.device_initializer = device_initializer
        self.lab = None

    def convert(self) -> Topology:
        logging.debug("preparing topology")
        topo = self._create_topology_from_virtual()

        logging.debug("initilizing devices")
        self._initialize_devices(topo)

        logging.debug("configuring protocols")
        self._configure_protocols(topo)

        return topo

    def _create_topology_from_virtual(self) -> Topology:
        self.lab = LabParser().parse(self.kathara_lab_path)
        parser = VirtualDeviceCommandsParser()
        device_builder = VirtualDeviceBuilder(self.lab, parser)
        topo = VirtualTopologyBuilder(self.lab, device_builder).build()
        return topo

    def _initialize_devices(self, topo: Topology) -> None:
        for device in topo.traverse():
            logging.debug(f"initializing: {device.name}")
            device.accept_physical_initializer(self.device_initializer)

    def _configure_protocols(self, topo: Topology) -> None:
        pass
