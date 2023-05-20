from typing import Generator

from model.devices.Node import Node


class Topology:
    def __init__(self, nodes: list[Node]) -> None:
        self.nodes = nodes

    def traverse(self) -> Generator[Node, None, None]:
        # TODO establish traversal order e.g. routers first
        for node in self.nodes:
            yield node
