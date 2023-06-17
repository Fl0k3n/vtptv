from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.routing.RIPConfig import RIPConfig
    from model.devices.Router import Router

class RIPConfigXMLGenerator:
    @staticmethod
    def generate(config: 'RIPConfig', router: 'Router') -> str:
        return f'''
<config>
    <routing>
        <control-plane-protocols>
            <control-plane-protocol>
                <rip>
                    {RIPConfigXMLGenerator.__generate_redistribue(config)}
                    {RIPConfigXMLGenerator.__generate_timers(config) if config.timers is not None else ""}
                    {RIPConfigXMLGenerator.__generate_interfaces(config, router)}
                </rip>
            </control-plane-protocol>
        </control-plane-protocols>
    </routing>
</config>
'''

    @staticmethod
    def __generate_redistribue(config: 'RIPConfig') -> str:
        return f'''
<redistribute>
    {"<connected/>" if config.redistribute.connected else ""}
    {"<static/>" if config.redistribute.static else ""}
</redistribute>
'''

    @staticmethod
    def __generate_timers(config: 'RIPConfig') -> str:
        return f'''
<timers>
    <update-interval>{config.timers.update}</update-interval>
    <invalid-interval>{config.timers.timeout}</invalid-interval>
    <flush-interval>{config.timers.garbage}</flush-interval>
</timers>
'''

    @staticmethod
    def does_network_contain(network_ip: str, network_mask: int, ip: str, mask: int = 32) -> bool:
        network_ip = network_ip.split('.')
        network_mask = [255 for _ in range(network_mask // 8)] + [256 - 2 ** (8 - network_mask % 8)] + [0 for _ in range(3 - network_mask // 8)]
        ip = ip.split('.')
        mask = [255 for _ in range(mask // 8)] + [256 - 2 ** (8 - mask % 8)] + [0 for _ in range(3 - mask // 8)]
        for network_byte, network_mask_byte, ip_byte, mask_byte in zip(network_ip, network_mask, ip, mask):
            if int(network_byte) & int(network_mask_byte) != (int(ip_byte) & int(mask_byte)) & int(network_mask_byte):
                return False
        return True

    @staticmethod
    def __generate_interfaces(config: 'RIPConfig', router: 'Router') -> str:
        enabled_interfaces = config.enabled_interfaces
        enabled_interfaces += [int_virt_name for int_virt_name,interface in router.interfaces.items() if len(list(filter(lambda network: RIPConfigXMLGenerator.does_network_contain(network[0], network[1], interface.ipv4, interface.netmask), config.enabled_networks))) > 0]

        return f'''
<interfaces>
    {"".join([RIPConfigXMLGenerator.__generate_interface(config, router, int_virt_name) for int_virt_name in enabled_interfaces])}
</interfaces>
'''

    @staticmethod
    def __generate_interface(config: 'RIPConfig', router: 'Router', int_virt_name: str) -> str:
        return f'''
<interface>
    <interface>{router.interfaces[int_virt_name].physical_name}</interface>
    {RIPConfigXMLGenerator.__generate_neighbors(config, router, int_virt_name) if len(config.neighbors) > 0 else ""}
</interface>
'''

    @staticmethod
    def __generate_neighbors(config: 'RIPConfig', router: 'Router', int_virt_name: str) -> str:
        int_ip = router.interfaces[int_virt_name].ipv4
        int_mask = router.interfaces[int_virt_name].netmask
        neighbors = list(filter(lambda neighbor: RIPConfigXMLGenerator.does_network_contain(int_ip, int_mask, neighbor), config.neighbors))

        if len(neighbors) == 0:
            return ""

        return f'''
<neighbors>
    {"".join([RIPConfigXMLGenerator.__generate_neighbor(neighbor) for neighbor in neighbors])}
</neighbors>
'''

    @staticmethod
    def __generate_neighbor(neighbor_ip: str) -> str:
        return f'''
<neighbor>
    <address>{neighbor_ip}</address>
</neighbor>
'''