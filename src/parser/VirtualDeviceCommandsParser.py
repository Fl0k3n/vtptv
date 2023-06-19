import logging
import re
from parser.actions.Action import NodeAction
from parser.actions.ConfigureInterfaceAction import ConfigureInterfaceAction
from typing import Iterator

from src.parser.actions.AddStaticRouteAction import AddStaticRouteAction


class VirtualDeviceCommandsParser:
    COMMENT = "#"

    def parse(self, commands: list[str]) -> list[NodeAction]:
        actions = []

        commands_iter = iter(self._preprocess(commands))
        for command in commands_iter:
            try:
                action = self._dispatch(command, commands_iter)
                actions.append(action)
            except Exception as ex:
                logging.error(f'Failed to parse command: {command}', exc_info=ex)

        return actions

    def _preprocess(self, commands: list[str]) -> list[str]:
        stripped = [command.strip() for command in commands]
        without_comments = [
            command for command in stripped if not command.startswith(self.COMMENT)]
        return without_comments

    def _dispatch(self, command: str, iter: Iterator[str]) -> NodeAction:
        if command.startswith('ifconfig'):
            return self._parse_ifconfig_command(command)
        elif command.startswith('route add'):
            return self._parse_route_add_command(command)

    def _parse_ifconfig_command(self, command: str) -> NodeAction:
        pattern = r'^ifconfig\s+(\S+)\s+(\S+)/(\d+)\s+(\S+)$'
        match = re.match(pattern, command)
        return ConfigureInterfaceAction(
            virtual_iface_name=match.group(1),
            ipv4=match.group(2),
            netmask=match.group(3),
            state=match.group(4)
        )

    def _parse_route_add_command(self, command: str) -> NodeAction:
        pattern = r'^route add (-net (\S+)/(\S+)|default) gw (\S+) dev (\S+)$'
        # 1 - default
        # 2,3 - network, netmask
        # 4 - gateway
        # 5 - interface

        match = re.match(pattern, command)

        target_network, target_mask = ("0.0.0.0", 0) if match.group(1) == 'default' else (match.group(2), int(match.group(3)))

        action = AddStaticRouteAction(
            network=target_network,
            netmask=target_mask,
            gateway=match.group(4),
            interface=match.group(5)
        )

        logging.debug(action)
        return action
