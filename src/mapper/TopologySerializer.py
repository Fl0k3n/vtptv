import os
import shutil
from datetime import datetime
from pathlib import Path

from model.devices.Node import NodeRole
from model.Topology import Topology


class TopologySerializer:
    _ROUTER_IMAGE = 'kathara/quagga'
    _HOST_IMAGE = 'kathara/base'
    _LAB_CONF_FILENAME = 'lab.conf'

    def serialize_as_kathara_file_tree(self, topo: Topology, root_dir: Path, overwrite: bool = False):
        self._create_directory_tree(topo, root_dir, overwrite)
        self._write_topology_config(topo, root_dir)
        self._write_startup_configs(topo, root_dir)

    def _write_topology_config(self, topo: Topology, root_dir: Path):
        with open(str(root_dir.joinpath(self._LAB_CONF_FILENAME).absolute()), 'w') as f:
            f.writelines([
                f'LAB_DESCRIPTION="lab created from physical topology at {datetime.now()}"\n',
                'LAB_VERSION=1.0\n',
                'LAB_AUTHOR="auto generated"\n',
                'LAB_EMAIL=none\n',
                'LAB_WEB=none\n'
            ])

            direct_connection_collision_domains: dict[frozenset[str], str] = {}

            for device in topo.nodes:
                if device.role in (NodeRole.ROUTER, NodeRole.HOST):
                    image_name = self._ROUTER_IMAGE if device.role == NodeRole.ROUTER else self._HOST_IMAGE
                    f.write(f'\n{device.name}[image]={image_name}\n')

                    for neigh_idx, neighbour in enumerate(device.neighbours):
                        cd_name = None
                        if neighbour.role != NodeRole.SWITCH:
                            devices = frozenset([device.name, neighbour.name])
                            if devices in direct_connection_collision_domains:
                                cd_name = direct_connection_collision_domains[devices]
                            else:
                                cd_name = f'A{len(direct_connection_collision_domains)}'
                                direct_connection_collision_domains[devices] = cd_name
                        else:
                            cd_name = neighbour.name

                        f.write(f'{device.name}[{neigh_idx}]="{cd_name}"\n')

    def _write_startup_configs(self, topo: Topology, root_dir: Path):
        for router in topo.routers:
            with open(str(root_dir.joinpath(f'{router.name}.startup').absolute()), 'w') as f:
                for iface in router.interfaces.values():
                    f.write(
                        f'ifconfig {iface.virtual_name} {iface.ipv4}/{iface.netmask} up\n')

                for route in router.static_routes:
                    if route.is_default():
                        f.write(
                            f'route add default gw {route.gateway_ipv4} dev {route.interface_name}\n')
                    else:
                        f.write(
                            f'route add -net {route.ipv4}/{route.netmask} gw {route.gateway_ipv4} dev {route.interface_name}\n')

    def _create_directory_tree(self, topo: Topology, root_dir: Path, overwrite: bool):
        if not overwrite:
            # TODO maybe pickle topo in some tmp file so that whole configuration won't need to be repeated
            assert not os.path.exists(
                str(root_dir.absolute())), f'{root_dir} path already exists, not overwriting'
        elif os.path.exists(str(root_dir.joinpath(self._LAB_CONF_FILENAME).absolute())):
            shutil.rmtree(str(root_dir.absolute()))

        os.makedirs(str(root_dir.absolute()))
