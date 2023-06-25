from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.routing.OSPFConfig import OSPFConfig
    from model.devices.Router import Router

    def generate(config: 'OSPFConfig', router: 'Router') -> str:
        x = f'''
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
        return x

    def _generate_networks(config: 'OSPFConfig') -> str:
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

    def get_wildcard_mask(prefix_mask: int) -> str:
        wildcard_mask = (1 << 32) - 1
        wildcard_mask = wildcard_mask ^ ((1 << (32 - prefix_mask)) - 1)
        return ".".join([str((wildcard_mask >> (8 * i)) & 255) for i in range(3, -1, -1)])
