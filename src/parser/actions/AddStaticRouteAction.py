from parser.actions.Action import NodeAction

from model.devices.Node import Node
from model.routing.StaticRoute import StaticRoute


class AddStaticRouteAction(NodeAction):

    def __init__(self, static_route: StaticRoute) -> None:
        super().__init__()
        self.static_route = static_route

    def apply(self, node: Node) -> None:
        node.add_static_route(self.static_route)

    def __str__(self) -> str:
        return f'AddStaticRouteAction({self.static_route})'
