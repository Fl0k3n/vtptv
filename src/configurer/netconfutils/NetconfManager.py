import logging

from ncclient import manager

from utils.netutil import convert_to_dot_notation


class NetconfManager:
    def __init__(self, ssh_login: str, ssh_pass: str) -> None:
        self.client: manager.Manager = None
        self.ssh_login = ssh_login
        self.ssh_pass = ssh_pass

    def __enter__(self, host_ip: str) -> "NetconfManager":
        self.client = manager.connect(host=host_ip, port=830, username=self.ssh_login,
                                      password=self.ssh_pass, device_params={'name': "csr"})
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        # TODO
        pass

    def configure_interface(self, name: str, ipv4: str, mask: int, enable: bool = True):
        data = f'''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>{name}</name>
                <enabled>{"true" if enable else "false"}</enabled>
                <description>interface configured via netconf</description>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>{ipv4}</ip>
                        <netmask>{convert_to_dot_notation(mask)}</netmask>
                    </address>
                </ipv4>
                <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
            </interface>
        </interfaces>
</config>
'''
        resp = self.client.edit_config(data, target='running')
        logging.debug(f"configure interface resp: {resp}")

    def configure(self, data: str) -> None:
        resp = self.client.edit_config(data, target='running')
        logging.debug(f"configure interface resp: {resp}")
