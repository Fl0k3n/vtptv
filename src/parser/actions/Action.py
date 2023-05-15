from abc import ABC, abstractmethod

from model.devices.Node import Node
from model.devices.Router import Router


class NodeAction(ABC):

    @abstractmethod
    def apply(self, node: Node) -> None:
        pass

class RouterAction(NodeAction):

    @abstractmethod
    def apply(self, node: Router) -> None:
        pass
    