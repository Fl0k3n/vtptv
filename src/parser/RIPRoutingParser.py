import re
from model.routing.RIPConfig import RIPConfig, RIPTimers


class RIPRoutingParser:
    @staticmethod
    def parse(commands: list[str]) -> RIPConfig:
        config = RIPConfig()
        for command in commands:
            if command.startswith('network'):
                RIPRoutingParser.__parse_network(config, command)
            elif command.startswith('version'):
                RIPRoutingParser.__parse_version(config, command)
            elif command.startswith('timer'):
                RIPRoutingParser.__parse_timer(config, command)
            elif command.startswith('redistribute'):
                RIPRoutingParser.__parse_redistribute(config, command)
            elif command.startswith('neighbor'):
                RIPRoutingParser.__parse_neighbor(config, command)
            else:
                continue
        return config

    @staticmethod
    def __parse_network(config: RIPConfig, command: str) -> None:
        # command: 'network {interface, ip/mask}'
        target = command.strip('\n').split(' ')[1]
        ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/(\d{1,2})')

        match = ip_pattern.match(target)
        if match:
            config.enabled_networks.append((match.group(1), int(match.group(2))))
        else:
            config.enabled_interfaces.append(target)

    @staticmethod
    def __parse_version(config: RIPConfig, command: str) -> None:
        # command: 'version <version>'
        version = command.strip('\n').split(' ')[1]
        config.version = int(version)

    @staticmethod
    def __parse_timer(config: RIPConfig, command: str) -> None:
        # command: 'timer <update> <timeout> <garbage>'
        update = int(command.split(' ')[1])
        timeout = int(command.split(' ')[2])
        garbage = int(command.strip('\n').split(' ')[3])
        config.timers = RIPTimers(update, timeout, garbage)

    @staticmethod
    def __parse_redistribute(config: RIPConfig, command: str) -> None:
        # command: 'redistribute <protocol>'
        protocol = command.strip('\n').split(' ')[1]
        match protocol:
            case 'connected':
                config.redistribute.connected = True
            case 'static':
                config.redistribute.static = True

    @staticmethod
    def __parse_neighbor(config: RIPConfig, command: str) -> None:
        # command: 'neighbor <ip>'
        ip = command.strip('\n').split(' ')[1]
        config.neighbors.append(ip)
