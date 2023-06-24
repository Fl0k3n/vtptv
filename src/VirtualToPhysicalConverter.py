import logging
from parser.VirtualDeviceCommandsParser import VirtualDeviceCommandsParser
from pathlib import Path

from Kathara.parser.netkit.LabParser import LabParser

from configurer.DeviceConfigurer import DeviceConfigurer
from configurer.DeviceInitializer import DeviceInitializer
from mapper.VirtualDeviceBuilder import VirtualDeviceBuilder
from mapper.VirtualTopologyBuilder import VirtualTopologyBuilder
from model.Topology import Topology


class VirtualToPhysicalConverter:
    def __init__(self, kathara_lab_path: Path, device_initializer: DeviceInitializer, device_configurer: DeviceConfigurer) -> None:
        self.kathara_lab_path = kathara_lab_path
        self.device_initializer = device_initializer
        self.device_configurer = device_configurer

    def convert(self, configure_devices=True) -> Topology:
        logging.debug("preparing topology")
        topo = self._create_topology_from_virtual()

        if configure_devices:
            logging.debug("initilizing devices")
            self._initialize_devices(topo)

            logging.debug("configuring protocols")
            self._configure_protocols(topo)

        return topo

    def _create_topology_from_virtual(self) -> Topology:
        lab = LabParser().parse(str(self.kathara_lab_path.absolute()))
        parser = VirtualDeviceCommandsParser()
        device_builder = VirtualDeviceBuilder(lab, parser)
        topo = VirtualTopologyBuilder(lab, device_builder).build()
        return topo

    def _initialize_devices(self, topo: Topology) -> None:
        for device in topo.traverse():
            logging.debug(f"initializing: {device.name}")
            device.accept_physical_initializer(self.device_initializer)

    def _configure_protocols(self, topo: Topology) -> None:
        for device in topo.traverse():
            logging.debug(f"configuring: {device.name}")
            device.accept_physical_configurer(self.device_configurer)
