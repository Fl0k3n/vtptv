
from model.devices.Router import Router
from model.routing.RoutingConfig import OSPFConfig
from utils.netutil import get_wildcard_mask


def generate_ospf_xml(router: Router) -> str:
    config = router.ospf_config
    return f'''
<config>
<native>
<router>
    <ospf>
    <router-id>{config.router_id}</router-id>
    {_generate_networks(config)}
    </ospf>
</router>
</native>
</config>
'''


def _generate_networks(config: OSPFConfig) -> str:
    return f'''
    {"".join([_generate_network(network) for network in config.enabled_networks])}
'''


@staticmethod
def _generate_network(network: tuple[str, int, str]) -> str:
    return f'''
    <network>
        <ip>{network[0]}</ip>
        <mask>{get_wildcard_mask(network[1])}</mask>
        <area>{network[2]}</area>
    </network>
'''
