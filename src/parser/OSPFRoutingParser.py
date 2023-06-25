import re
from model.routing.OSPFConfig import OSPFConfig


class OSPFRoutingParser:
    @staticmethod
    def parse(commands: list[str]) -> OSPFConfig:
        config = OSPFConfig()
        for command in commands:
            if command.startswith('ospf router-id'):
                OSPFRoutingParser.__parse_router_id(config, command)
            elif command.startswith('network'):
                OSPFRoutingParser.__parse_network(config, command)
            else:
                continue
        return config

    @staticmethod
    def __parse_network(config: OSPFConfig, command: str) -> None:
        # command: 'network {ip/mask} area {area}'
        pattern = r"network (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/(\d+) area (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        matches = re.search(pattern, command.strip("\n"))
        if matches:
            ip = matches.group(1)
            mask = matches.group(2)
            area = matches.group(3)
            config.enabled_networks.append((ip,mask,area))
    

    @staticmethod
    def __parse_router_id(config: OSPFConfig, command: str) -> None:
        # command: 'ospf router-id {id}'
        router_id = command.strip('\n').split(' ')[2]
        config.router_id = router_id