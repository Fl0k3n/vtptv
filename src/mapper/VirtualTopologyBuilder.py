from Kathara.model.Lab import Lab as KatharaLab
from Kathara.model.Link import Link as KatharaLink
from Kathara.model.Machine import Machine as KatharaMachine

from mapper.VirtualDeviceBuilder import VirtualDeviceBuilder
from model.devices.Node import Node
from model.devices.Switch import Switch
from model.Topology import Topology


class VirtualTopologyBuilder:
    def __init__(self, kathara_lab: KatharaLab, device_builder: VirtualDeviceBuilder) -> None:
        self.kathara_lab = kathara_lab
        self.device_builder = device_builder

    def build(self) -> Topology:
        nodes = {name: self.device_builder.build_from_machine(
            machine) for name, machine in self.kathara_lab.machines.items()}
        switches = self._create_switches()

        self._connect_devices(nodes, switches)
        nodes.update(switches)

        return Topology(list(nodes.values()))

    def _create_switches(self) -> dict[str, Switch]:
        switches = {}

        for link in self.kathara_lab.links.values():
            if self._collision_domain_requires_switch(link):
                switch = self.device_builder.build_switch(link)
                switches[switch.name] = switch

        return switches

    def _connect_devices(self, nodes: dict[str, Node], switches: dict[str, Switch]) -> None:
        for machine_name, node in nodes.items():
            machine = self.kathara_lab.get_machine(machine_name)

            for link in machine.interfaces.values():
                collision_domain = link.name
                iface_name = self._extract_virtual_interface_name(
                    link, machine)

                if collision_domain in switches:
                    switch = switches[collision_domain]
                    node.add_neighbour(
                        switch, iface_name, switch.get_next_free_virtual_interface_name())
                else:
                    m1, m2 = link.machines.values()
                    neighbour_machine = m1 if m2.name == machine_name else m2
                    if neighbour_machine.name > machine_name:
                        node.add_neighbour(
                            nodes[neighbour_machine.name],
                            iface_name,
                            self._extract_virtual_interface_name(
                                link, neighbour_machine)
                        )

    def _extract_virtual_interface_name(self, link: KatharaLink, machine: KatharaMachine) -> str:
        for iface_num, iface in machine.interfaces.items():
            if iface.name == link.name:
                return f'{Node.VIRTUAL_INTERFACE_PREFIX}{iface_num}'

        raise Exception(
            f"machine {machine.name} doesn't have an interface in domain {link.name}")

    def _collision_domain_requires_switch(self, link: KatharaLink) -> bool:
        cd_represents_direct_connection = len(link.machines) == 2
        return not cd_represents_direct_connection
