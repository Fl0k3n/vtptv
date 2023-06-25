import logging
from parser.protocols.ospf import parse_ospf_commands
from parser.protocols.rip import parse_rip_commands
from parser.VirtualDeviceCommandsParser import \
    VirtualDeviceCommandsParser as Parser
from pathlib import Path

from Kathara.model.Lab import Lab as KatharaLab
from Kathara.model.Link import Link as KatharaLink
from Kathara.model.Machine import Machine as KatharaMachine

from model.devices.Host import Host
from model.devices.Node import Node
from model.devices.Router import Router
from model.devices.Switch import Switch
from model.links.Interface import Interface


class VirtualDeviceBuilder:
    _HOST_IMAGE = "kathara/base"

    def __init__(self, lab: KatharaLab, parser: Parser) -> None:
        self.kathara_lab = lab
        self.parser = parser

    def build_from_machine(self, machine: KatharaMachine) -> Node:
        if machine.get_image() == self._HOST_IMAGE or machine.name.startswith('pc'):  # TODO
            return self._create_host(machine)
        return self._create_router(machine)

    def build_switch(self, link: KatharaLink) -> Switch:
        interfaces = self._create_interfaces(len(link.machines))
        switch_vname = link.name
        return Switch(switch_vname, interfaces)

    def _create_router(self, machine: KatharaMachine) -> Router:
        interfaces = self._create_interfaces(len(machine.interfaces))
        router = Router(machine.name, interfaces)
        self._apply_startup_commands(machine, router)
        self._apply_routing_commands(machine, router)

        return router

    def _create_host(self, machine: KatharaMachine) -> Host:
        interfaces = self._create_interfaces(len(machine.interfaces))
        host = Host(machine.name, interfaces)
        self._apply_startup_commands(machine, host)
        return host

    def _apply_startup_commands(self, machine: KatharaMachine, node: Node):
        startup_commands = self._get_startup_commands(machine)

        for action in self.parser.parse(startup_commands):
            action.apply(node)

    def _apply_routing_commands(self, machine: KatharaMachine, router: Router):
        if rip_config_commands := self._get_rip_config_commands(machine):
            router.rip_config = parse_rip_commands(rip_config_commands)
        if ospf_config_commands := self._get_ospf_config_commands(machine):
            router.ospf_config = parse_ospf_commands(ospf_config_commands)

    def _create_interfaces(self, count: int) -> list[Interface]:
        return [Interface.down_virtual(f'{Node.VIRTUAL_INTERFACE_PREFIX}{idx}') for idx in range(count)]

    def _get_startup_commands(self, machine: KatharaMachine) -> list[str]:
        return self._read_commands(Path(machine.startup_path) if machine.startup_path is not None else None)

    def _get_rip_config_commands(self, machine: KatharaMachine) -> list[str]:
        return self._read_commands(self._get_machine_data_path(machine, 'etc/quagga/ripd.conf'))

    def _get_ospf_config_commands(self, machine: KatharaMachine) -> list[str]:
        return self._read_commands(self._get_machine_data_path(machine, 'etc/quagga/ospfd.conf'))

    def _get_machine_data_path(self, machine: KatharaMachine, file_relative_path: str) -> Path | None:
        return Path(machine.folder).joinpath(file_relative_path) if machine.folder is not None else None

    def _read_commands(self, path: Path | None) -> list[str]:
        if path is not None:
            try:
                with open(str(path.absolute()), 'r') as f:
                    return f.readlines()
            except Exception as e:
                logging.error(
                    f'Failed to read config commands from {path}', exc_info=e)
        return []
