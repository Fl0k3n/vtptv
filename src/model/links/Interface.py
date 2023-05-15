class Interface:
    def __init__(self, virtual_name: str, physical_name: str, ipv4: str, netmask: int, enabled: bool) -> None:
        self.virtual_name = virtual_name
        self.physical_name = physical_name
        self.ipv4 = ipv4
        self.netmask = netmask
        self.enabled = enabled
        self.used = False
 
    @staticmethod
    def down_virtual(virtual_name: str, physical_name: str = None) -> "Interface":
        return Interface(virtual_name, physical_name, None, None, False)

    def use(self):
        self.used = True

    def __str__(self) -> str:
        return (f'vname: {self.virtual_name}, pname: {self.physical_name}, '
                f'address: {self.ipv4}/{self.netmask}, used: {self.used}, enabled={self.enabled}')
    