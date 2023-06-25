class StaticRoute:
    DEFAULT_DESCRIPTOR = 'default'
    DEFAULT_IPV4 = '0.0.0.0'
    DEFAULT_NETMASK = 0

    def __init__(self, ipv4: str, netmask: int, gateway_ipv4: str, interface_name: str) -> None:
        self.ipv4 = ipv4
        self.netmask = netmask
        self.gateway_ipv4 = gateway_ipv4
        self.interface_name = interface_name

    def is_default(self) -> bool:
        return self.ipv4 == self.DEFAULT_IPV4 and self.netmask == self.DEFAULT_NETMASK

    @staticmethod
    def default(gateway_ipv4: str, interface_name: str) -> 'StaticRoute':
        return StaticRoute(StaticRoute.DEFAULT_IPV4, StaticRoute.DEFAULT_NETMASK, gateway_ipv4, interface_name)

    def __str__(self) -> str:
        return f'{self.ipv4}/{self.netmask} via {self.gateway_ipv4} on {self.interface_name}'
