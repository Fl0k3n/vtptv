from abc import ABC, abstractmethod, abstractproperty
from enum import Enum
from typing import TYPE_CHECKING

from model.routes.StaticRoute import StaticRoute

if TYPE_CHECKING:
    from configurer.DeviceInitializer import DeviceInitializer
    from configurer.DeviceConfigurer import DeviceConfigurer

from model.links.Interface import Interface
from utils.netutil import get_subnet


class NodeRole(Enum):
    HOST = 0
    ROUTER = 1
    SWITCH = 2


class Node(ABC):
    VIRTUAL_INTERFACE_PREFIX = 'eth'

    def __init__(self, name: str, interfaces: list[Interface], neighbours: dict[str, "Node"] = None) -> None:
        self.name = name
        self.interfaces = {
            interface.virtual_name: interface for interface in interfaces}
        self.neighbours: dict[str,
                              "Node"] = neighbours if neighbours is not None else {}
        self.static_routes: list[StaticRoute] = []

    def add_neighbour(self, neighbour: "Node", interface_vname: str, neigh_interface_vname: str) -> None:
        self.neighbours[interface_vname] = neighbour
        neighbour.neighbours[neigh_interface_vname] = self

        my_int = self.interfaces[interface_vname]
        neighbour_int = self.interfaces[neigh_interface_vname]

        assert not my_int.used and not neighbour_int.used, \
            ('Attempted to plug cable to used interface: '
             f'{self.name} - ({interface_vname}, {neigh_interface_vname}) - {neighbour.name}')

        my_int.use()
        neighbour_int.use()

    def add_static_route(self, route: StaticRoute) -> None:
        self.static_routes.append(route)

    def get_common_network(self, neigh: "Node") -> str | None:
        iface = self.get_interface_to(neigh)
        if iface is None or iface.ipv4 is None or iface.netmask is None:
            return None
        return get_subnet(iface.ipv4, iface.netmask)

    def get_interface_to(self, neigh: "Node") -> Interface | None:
        for iface_name, node in self.neighbours.items():
            if neigh == node:
                return self.interfaces[iface_name]
        return None

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
