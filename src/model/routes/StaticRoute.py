class StaticRoute:
    def __init__(self, network: str, netmask: str, gateway: str, interface: str) -> None:
        self.network = network
        self.netmask = netmask
        self.gateway = gateway
        self.interface = interface
