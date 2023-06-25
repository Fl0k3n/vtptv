import logging
import re
from parser.actions.Action import NodeAction
from parser.actions.AddStaticRouteAction import AddStaticRouteAction
from parser.actions.AddTranslationRuleAction import AddTranslationRuleAction
from parser.actions.ConfigureInterfaceAction import ConfigureInterfaceAction
from typing import Iterator

from model.routing.StaticRoute import StaticRoute
from model.translations.Nat import DNat, OverloadNat, SNat


class VirtualDeviceCommandsParser:
    COMMENT = "#"
    _IPV4_RE = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

    def parse(self, commands: list[str]) -> list[NodeAction]:
        actions = []

        commands_iter = iter(self._preprocess(commands))
        for command in commands_iter:
            try:
                action = self._dispatch(command, commands_iter)
                actions.append(action)
            except Exception as ex:
                logging.error(
                    f'Failed to parse command: {command}', exc_info=ex)

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
        elif command.startswith('iptables'):
            return self._parse_iptables_command(command)

    def _parse_ifconfig_command(self, command: str) -> NodeAction:
        pattern = r'^ifconfig\s+(\S+)\s+(' + \
            self._IPV4_RE + r')/(\d+)\s+(\S+)$'
        match = re.match(pattern, command)
        return ConfigureInterfaceAction(
            virtual_iface_name=match.group(1),
            ipv4=match.group(2),
            netmask=int(match.group(3)),
            state=match.group(4)
        )

    def _parse_route_add_command(self, command: str) -> NodeAction:
        pattern = r'^route add (-net (' + self._IPV4_RE + \
            r')/(\S+)|default) gw (\S+) dev (\S+)$'
        match = re.match(pattern, command)

        gateway, interface = match.group(4), match.group(5)

        if match.group(1) == StaticRoute.DEFAULT_DESCRIPTOR:
            route = StaticRoute.default(gateway, interface)
        else:
            route = StaticRoute(ipv4=match.group(2), netmask=int(
                match.group(3)), gateway_ipv4=gateway, interface_name=interface)

        return AddStaticRouteAction(route)

    def _parse_iptables_command(self, command: str) -> NodeAction:
        table_selector = r'-t\s+(\w+)'
        chain_selector = r'-(A|I)\s+(\w+)'

        table_match = re.search(table_selector, command)
        chain_match = re.search(chain_selector, command)

        if not table_match or not chain_match:
            raise Exception(f'Failed to parse iptables command: {command}')

        table = table_match.group(1)
        chain = chain_match.group(2)

        if table == 'nat':
            if chain == 'POSTROUTING':
                if 'MASQUERADE' in command:
                    src_match = re.search(
                        r'-s\s+(' + self._IPV4_RE + r')/(\d+)', command)
                    assert src_match, 'NAT overloading requires source subnet'
                    return AddTranslationRuleAction(
                        OverloadNat(src_ipv4=src_match.group(1), src_netmask=int(src_match.group(2))))
                elif 'SNAT' in command:
                    src_match = re.search(
                        r'-s\s+(' + self._IPV4_RE + r')', command)
                    new_src_match = re.search(
                        r'--to-source\s+(' + self._IPV4_RE + r')', command)
                    assert src_match and new_src_match, 'SNAT requires original source and new source'
                    return AddTranslationRuleAction(
                        SNat(original_src_ipv4=src_match.group(1), target_src_ipv4=new_src_match.group(1)))
            elif chain == 'OUTPUT':
                if 'DNAT' in command:
                    dst_match = re.search(
                        r'-d\s+(' + self._IPV4_RE + r')', command)
                    new_dest_match = re.search(
                        r'--to-destination\s+(' + self._IPV4_RE + r')', command)
                    assert dst_match and new_dest_match, 'DNAT requires original destination and new destination'
                    return AddTranslationRuleAction(
                        DNat(original_dest_ipv4=dst_match.group(1), target_dest_ipv4=new_dest_match.group(1)))

        raise Exception(
            f'Unsupported table {table}, chain {chain}, or option in: {command}')
