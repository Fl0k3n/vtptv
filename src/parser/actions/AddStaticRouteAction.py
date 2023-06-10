from src.model.devices.Node import Node
from src.parser.actions.Action import NodeAction


class AddStaticRouteAction(NodeAction):

    def __init__(self, network: str, netmask: int, gateway: str, interface: str) -> None:
        super().__init__()
        self.network = network
        self.netmask = netmask
        self.gateway = gateway
        self.interface = interface

    def apply(self, node: Node) -> None:
        node.add_static_route(self.network, self.netmask, self.gateway, self.interface)

    def __str__(self) -> str:
        return f'AddStaticRouteAction({self.network}/{self.netmask} via {self.gateway} on {self.interface})'
