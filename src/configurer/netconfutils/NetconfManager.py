import logging

from ncclient import manager

from utils.netutil import convert_to_dot_notation

from src.model.routes.StaticRoute import StaticRoute


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
    # https://github.com/ArRosid/netconf-static-route/blob/master/static_route_template.xml
    def configure_static_route(self, static_route: StaticRoute):
        data = f'''
<config>
   <routing xmlns="urn:ietf:params:xml:ns:yang:ietf-routing">
      <routing-instance>
         <name>default</name>
         <description>default-vrf [read-only]</description>
         <interfaces/>
         <routing-protocols>
            <routing-protocol>
               <type>static</type>
               <name>1</name>
               <static-routes>
                  <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ipv4-unicast-routing">
                     <route>
                        <destination-prefix>{static_route.network}/{static_route.netmask}</destination-prefix>
                        <next-hop>
                           <next-hop-address>{static_route.gateway}</next-hop-address>
                        </next-hop>
                     </route>
                  </ipv4>
               </static-routes>
            </routing-protocol>
         </routing-protocols>
      </routing-instance>
   </routing>
</config>
        '''
        resp = self.client.edit_config(data, target='running')
        logging.debug(f"configure static route resp: {resp}")
