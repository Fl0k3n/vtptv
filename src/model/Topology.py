from typing import Generator

from model.devices.Node import Node, NodeRole
from model.devices.Router import Router
from model.devices.Switch import Switch


class Topology:
    def __init__(self, nodes: list[Node]) -> None:
        self.nodes = nodes

    def traverse(self) -> Generator[Node, None, None]:
        # TODO establish traversal order e.g. routers first
        for node in self.nodes:
            yield node

    @property
    def routers(self) -> list[Router]:
        return self._filter_by_role(NodeRole.ROUTER)

    @property
    def switches(self) -> list[Switch]:
        return self._filter_by_role(NodeRole.SWITCH)

    def _filter_by_role(self, role: NodeRole):
        return [device for device in self.nodes if device.role == role]
