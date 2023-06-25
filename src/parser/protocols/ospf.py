import re

from model.routing.RoutingConfig import OSPFConfig, OspfNetworkInfo


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
    if match := re.search(pattern, command.strip("\n")):
        config.enabled_networks.append(OspfNetworkInfo(
            ip=match.group(1),
            mask=int(match.group(2)),
            area=match.group(3)
        ))


def _parse_router_id(config: OSPFConfig, command: str) -> None:
    # command: 'ospf router-id {id}'
    router_id = command.strip('\n').split(' ')[2]
    config.router_id = router_id
