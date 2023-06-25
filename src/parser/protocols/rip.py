import re

from model.routing.RoutingConfig import RIPConfig, RIPTimers


def parse_rip_commands(commands: list[str]) -> RIPConfig:
    config = RIPConfig()
    for command in commands:
        if command.startswith('network'):
            _parse_network(config, command)
        elif command.startswith('version'):
            _parse_version(config, command)
        elif command.startswith('timer'):
            _parse_timer(config, command)
        elif command.startswith('redistribute'):
            _parse_redistribute(config, command)
        elif command.startswith('neighbor'):
            _parse_neighbor(config, command)
    return config


def _parse_network(config: RIPConfig, command: str) -> None:
    # command: 'network {interface, ip/mask}'
    target = command.strip('\n').split(' ')[1]
    ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/(\d{1,2})')

    match = ip_pattern.match(target)
    if match:
        config.enabled_networks.append((match.group(1), int(match.group(2))))
    else:
        config.enabled_interfaces.append(target)


def _parse_version(config: RIPConfig, command: str) -> None:
    # command: 'version <version>'
    version = command.strip('\n').split(' ')[1]
    config.version = int(version)


def _parse_timer(config: RIPConfig, command: str) -> None:
    # command: 'timer <update> <timeout> <garbage>'
    update = int(command.split(' ')[1])
    timeout = int(command.split(' ')[2])
    garbage = int(command.strip('\n').split(' ')[3])
    config.timers = RIPTimers(update, timeout, garbage)


def _parse_redistribute(config: RIPConfig, command: str) -> None:
    # command: 'redistribute <protocol>'
    protocol = command.strip('\n').split(' ')[1]
    match protocol:
        case 'connected':
            config.redistribute.connected = True
        case 'static':
            config.redistribute.static = True


def _parse_neighbor(config: RIPConfig, command: str) -> None:
    # command: 'neighbor <ip>'
    ip = command.strip('\n').split(' ')[1]
    config.neighbors.append(ip)
