import logging
import re
from typing import Callable

from configurer.consoleutils.DeviceConsolePortManager import \
    DeviceConsolePortManager
from configurer.consoleutils.DeviceMode import (DeviceConfigMode,
                                                DeviceEnabledMode)
from model.devices.CiscoNetworkNode import CiscoNetworkNode
from model.devices.Host import Host
from model.devices.Router import Router
from model.devices.Switch import Switch
from model.links.Interface import Interface
from utils.netutil import convert_to_dot_notation
from utils.userio import (require_router_console_connected,
                          require_switch_console_connected)


class DeviceInitializer:
    _DEVICE_DOMAIN_NAME = "none.org"

    def __init__(self, console_port_manager: DeviceConsolePortManager, ssh_login: str, ssh_pass: str) -> None:
        self.console_port_manager = console_port_manager
        self.ssh_login = ssh_login
        self.ssh_pass = ssh_pass
        self._netconf_iface_counter = 0

    def init_router(self, router: Router) -> None:
        require_router_console_connected(router.name)

        # assuming device is already booted (and user declined initial config dialog)
        with self.console_port_manager as console:
            with DeviceEnabledMode(console):
                self._disable_CLI_paging(console)

                router.netconf_interface = self._init_physical_interfaces(
                    list(router.interfaces.values()), console)

                self._configure_physical_interface(
                    router.netconf_interface, console)

                self._enable_ssh_access(router.name, console)
                self._enable_netconf_access(console)

    def init_switch(self, switch: Switch) -> None:
        print(
            f"Switch initilization is not implemented, skipping: {switch.name}")

    def init_host(self, host: Host) -> None:
        print(f"Skipping host initialization for host: {host.name}")

    def init_router_from_physical(self, name: str) -> Router:
        require_router_console_connected(name)
        router = Router(name, [])
        self._init_cisco_device_from_physical(router, lambda console: self._get_name_of_free_interface(console))
        return router

    def init_switch_from_physical(self, name: str) -> Switch:
        require_switch_console_connected(name)
        switch = Switch(name, [])
        self._init_cisco_device_from_physical(switch, lambda _: 'vlan 0')
        return switch

    def _init_cisco_device_from_physical(self, node: CiscoNetworkNode,
                                         netconf_iface_name_supplier: Callable[[DeviceConsolePortManager], str]):
        with self.console_port_manager as console:
            with DeviceEnabledMode(console):
                self._disable_CLI_paging(console)
                running_conf = self._read_running_config(console)
                
                netconf_iface = self._create_netconf_interface(netconf_iface_name_supplier(console))
                self._configure_physical_interface(netconf_iface, console)

                self._enable_ssh_access(node.name)
                self._enable_netconf_access(console)
                self._enable_cisco_discovery_protocol(console)
        
        node.netconf_interface = netconf_iface
        node.running_conf_data = running_conf


    def _init_physical_interfaces(self, virtual_ifaces: list[Interface], console: DeviceConsolePortManager) -> Interface:
        interface_names = self._read_device_physical_interface_names(console)

        if len(interface_names) < len(virtual_ifaces) + 1:
            print(
                f'not enough router interfaces, got {len(interface_names)}, required {len(virtual_ifaces) + 1}')
            return

        for virtual_iface, physical_iface_name in zip(virtual_ifaces, interface_names):
            virtual_iface.physical_name = physical_iface_name

        return self._create_netconf_interface(interface_names[len(virtual_ifaces)])

    def _read_device_physical_interface_names(self, console: DeviceConsolePortManager) -> list[str]:
        ifaces_info = console.write_and_get_output(
            "show ip interface brief")
        iface_names = []

        for line in ifaces_info.splitlines():
            logging.debug(f'line from serial: {line}')
            # TODO also allow serial interfaces
            if 'ethernet' in line.lower():
                iface_names.append(line.split()[0])

        if not iface_names:
            logging.debug(
                f"Failed to read any interface names, got: {ifaces_info}")

        return iface_names
    
    def _read_running_config(self, console: DeviceConsolePortManager) -> str:
        # TODO consider fetching it with netconf instead
        return console.write_and_get_output("show running-config")

    def _get_name_of_free_interface(self, console: DeviceConsolePortManager) -> str:
        ifaces_info = console.write_and_get_output("show ip interface brief")
        
        pattern = re.compile(r'(\S*ethernet\S*)\s+\S+\s+yes\s+\S+\s+administratively down\s+down')
        for line in ifaces_info.splitlines():
            if match := pattern.search(line):
                return match.group(1)
            
        raise Exception(f"Failed to find free interface, got output: {ifaces_info}")
                

    def _create_netconf_interface(self, physical_name: str) -> Interface:
        # TODO don't hardcode and assert it doesn't overlap with ips in topology or on local machine
        self._netconf_iface_counter += 1
        ipv4 = f"9.9.9.{self._netconf_iface_counter}"
        mask = 24

        return Interface(None, physical_name, ipv4, mask, False)
    
    def _disable_CLI_paging(self, console: DeviceConsolePortManager):
        console.write('terminal length 0')

    def _configure_physical_interface(self, interface: Interface, console: DeviceConsolePortManager) -> None:
        assert not (interface.physical_name is None or interface.ipv4 is None or interface.netmask is None), \
            f"Interface is not ready to be configured: {interface}"

        with DeviceConfigMode(console):
            console.write(f"interface {interface.physical_name}")
            success = console.write_failable(
                f'ip address {interface.ipv4} {convert_to_dot_notation(interface.netmask)}')

            if not success:
                # TODO
                logging.error(f'Failed to configure interface {interface}')
                console.write('exit')
                return

            console.write('no shutdown')
            console.write('exit')

    def _enable_ssh_access(self, hostname: str, console: DeviceConsolePortManager) -> None:
        logging.debug(f"configuring ssh access on {hostname}")

        with DeviceConfigMode(console):
            console.write(f"hostname {hostname}")
            console.write(f"ip domain-name {self._DEVICE_DOMAIN_NAME}")

            if not console.write_failable("crypto key generate rsa modulus 2048"):
                logging.debug(f"'crypto key' command failed on {hostname}")
                if not console.write_failable("crypto key generate rsa general-keys modulus 2048"):
                    print(f"Failed to enable ssh on {hostname}")
                    return

            console.write(
                f"username {self.ssh_login} priv 15 pass {self.ssh_pass}")
            console.write("line vty 0")
            console.write("login local")
            console.write("transport input ssh")

        logging.debug(f"enabled ssh of {hostname}")

    def _enable_netconf_access(self, console: DeviceConsolePortManager) -> None:
        logging.debug(f"configuring netconf")

        with DeviceConfigMode(console):
            console.write('netconf-yang')

        logging.debug(f"configured netconf")

    def _enable_cisco_discovery_protocol(self, console: DeviceConsolePortManager) -> None:
        logging.debug("configuring CDP")

        with DeviceConfigMode(console):
            console.write("cdp run")

        logging.debug("configured CDP")
