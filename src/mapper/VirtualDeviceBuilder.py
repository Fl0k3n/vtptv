from parser.VirtualDeviceCommandsParser import \
    VirtualDeviceCommandsParser as Parser

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

    def _create_interfaces(self, count: int) -> list[Interface]:
        return [Interface.down_virtual(f'{Node.VIRTUAL_INTERFACE_PREFIX}{idx}') for idx in range(count)]

    def _get_startup_commands(self, machine: KatharaMachine) -> list[str]:
        if machine.startup_path:
            try:
                with open(machine.startup_path, 'r') as f:
                    return f.readlines()
            except Exception as e:
                print(f'Failed to read startup commands of {machine.name}')
                print(e)
        return []
