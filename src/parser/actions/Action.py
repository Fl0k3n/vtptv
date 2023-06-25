from abc import ABC, abstractmethod

from model.devices.Node import Node
from model.devices.Router import Router


class NodeAction(ABC):

    @abstractmethod
    def apply(self, node: Node) -> None:
        pass

class RouterAction(NodeAction):

    def apply(self, node: Router) -> None:
        assert isinstance(node, Router), f'Router config action requires node to be a router, got {node}'
    