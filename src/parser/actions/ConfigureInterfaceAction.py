from parser.actions.Action import NodeAction

from model.devices.Node import Node


class ConfigureInterfaceAction(NodeAction):

    def __init__(self, virtual_iface_name: str, ipv4: str, netmask: int, state: str = 'up') -> None:
        super().__init__()
        self.virtual_iface_name = virtual_iface_name
        self.ipv4 = ipv4
        self.netmask = netmask
        self.state = state

    def apply(self, node: Node) -> None:
        iface = node.interfaces[self.virtual_iface_name]
        iface.enabled = self.state == 'up'
        iface.ipv4 = self.ipv4
        iface.netmask = self.netmask
