import re

from model.routing.OSPFConfig import OSPFConfig


def parse_ospf_commands(commands: list[str]) -> OSPFConfig:
    config = OSPFConfig()
    for command in commands:
        if command.startswith('ospf router-id'):
            _parse_router_id(config, command)
        elif command.startswith('network'):
            _parse_network(config, command)
    return config


def _parse_network(config: OSPFConfig, command: str) -> None:
    # command: 'network {ip/mask} area {area}'
    pattern = r"network (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/(\d+) area (\S+)"
    matches = re.search(pattern, command.strip("\n"))
    if matches:
        ip = matches.group(1)
        mask = int(matches.group(2))
        area = matches.group(3)
        config.enabled_networks.append((ip, mask, area))


def _parse_router_id(config: OSPFConfig, command: str) -> None:
    # command: 'ospf router-id {id}'
    router_id = command.strip('\n').split(' ')[2]
    config.router_id = router_id
