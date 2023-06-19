from model.devices.Node import Node
from model.links.Interface import Interface


class CiscoNetworkNode(Node):
    def __init__(self, name: str, interfaces: list[Interface], neighbours: set[Node] = None) -> None:
        super().__init__(name, interfaces, neighbours)
        self.netconf_interface: Interface = None
        self.running_conf_data: str = None