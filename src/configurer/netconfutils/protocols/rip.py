from typing import TYPE_CHECKING

from utils.netutil import network_contains

if TYPE_CHECKING:
    from model.devices.Router import Router
    from model.routing.RIPConfig import RIPConfig


def generate_rip_xml(config: 'RIPConfig', router: 'Router') -> str:
    return f'''
<config>
<routing>
    <control-plane-protocols>
        <control-plane-protocol>
            <rip>
                {_generate_redistribue(config)}
                {_generate_timers(config) if config.timers is not None else ""}
                {_generate_interfaces(config, router)}
            </rip>
        </control-plane-protocol>
    </control-plane-protocols>
</routing>
</config>
'''


def _generate_redistribue(config: 'RIPConfig') -> str:
    return f'''
<redistribute>
{"<connected/>" if config.redistribute.connected else ""}
{"<static/>" if config.redistribute.static else ""}
</redistribute>
'''


def _generate_timers(config: 'RIPConfig') -> str:
    return f'''
<timers>
<update-interval>{config.timers.update}</update-interval>
<invalid-interval>{config.timers.timeout}</invalid-interval>
<flush-interval>{config.timers.garbage}</flush-interval>
</timers>
'''


def _generate_interfaces(config: 'RIPConfig', router: 'Router') -> str:
    enabled_interfaces = config.enabled_interfaces
    for int_virt_name, interface in router.interfaces.items():
        if any(network_contains(network[0], network[1], interface.ipv4, interface.netmask) for network in config.enabled_networks):
            enabled_interfaces.append(int_virt_name)
    return f'''
<interfaces>
{"".join([_generate_interface(config, router, int_virt_name) for int_virt_name in enabled_interfaces])}
</interfaces>
'''


def _generate_interface(config: 'RIPConfig', router: 'Router', int_virt_name: str) -> str:
    return f'''
<interface>
<interface>{router.interfaces[int_virt_name].physical_name}</interface>
{_generate_neighbors(config, router, int_virt_name) if len(config.neighbors) > 0 else ""}
</interface>
'''


def _generate_neighbors(config: 'RIPConfig', router: 'Router', int_virt_name: str) -> str:
    int_ip = router.interfaces[int_virt_name].ipv4
    int_mask = router.interfaces[int_virt_name].netmask
    neighbors = [neighbor for neighbor in config.neighbors if network_contains(
        int_ip, int_mask, neighbor)]

    if len(neighbors) == 0:
        return ""

    return f'''
<neighbors>
{"".join([_generate_neighbor(neighbor) for neighbor in neighbors])}
</neighbors>
'''


@staticmethod
def _generate_neighbor(neighbor_ip: str) -> str:
    return f'''
<neighbor>
<address>{neighbor_ip}</address>
</neighbor>
'''
