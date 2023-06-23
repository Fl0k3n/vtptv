from abc import ABC, abstractmethod, abstractproperty
from enum import Enum
from typing import TYPE_CHECKING

from model.routes.StaticRoute import StaticRoute

if TYPE_CHECKING:
    from configurer.DeviceInitializer import DeviceInitializer
    from configurer.DeviceConfigurer import DeviceConfigurer

from model.links.Interface import Interface


class NodeRole(Enum):
    HOST = 0
    ROUTER = 1
    SWITCH = 2


class Node(ABC):
    VIRTUAL_INTERFACE_PREFIX = 'eth'

    def __init__(self, name: str, interfaces: list[Interface], neighbours: set["Node"] = None) -> None:
        self.name = name
        self.interfaces = {
            interface.virtual_name: interface for interface in interfaces}
        self.neighbours: set["Node"] = neighbours if neighbours is not None else set()
        self.static_routes: list[StaticRoute] = []

    def add_neighbour(self, neighbour: "Node", interface_vname: str, neigh_interface_vname: str) -> None:
        self.neighbours.add(neighbour)
        neighbour.neighbours.add(self)

        my_int = self.interfaces[interface_vname]
        neighbour_int = self.interfaces[neigh_interface_vname]

        assert not my_int.used and not neighbour_int.used, \
            ('Attempted to plug cable to used interface: '
             f'{self.name} - ({interface_vname}, {neigh_interface_vname}) - {neighbour.name}')

        my_int.use()
        neighbour_int.use()

    def add_static_route(self, route: StaticRoute) -> None:
        self.static_routes.append(route)

    def get_next_free_virtual_interface_name(self) -> str:
        for name, iface in self.interfaces.items():
            if not iface.used:
                return name
        raise Exception(f"All interfaces of {self.name} are already used")

    @abstractmethod
    def accept_physical_initializer(self, initilizer: 'DeviceInitializer') -> None:
        pass

    @abstractmethod
    def accept_physical_configurer(self, configurer: 'DeviceConfigurer') -> None:
        pass

    @abstractproperty
    def role(self) -> NodeRole:
        pass

    def __str__(self) -> str:
        return f'name: {self.name}'
