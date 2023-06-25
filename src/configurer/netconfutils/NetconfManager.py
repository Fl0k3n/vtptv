import logging
import xml.etree.ElementTree as ET

from ncclient import manager

from model.links.Interface import Interface
from model.routing.StaticRoute import StaticRoute
from utils.netutil import netmask_from_dot_notation, netmask_to_dot_notation


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
        # TODO cleanup
        pass

    def configure(self, netconf_xml_data: str) -> None:
        resp = self.client.edit_config('running', netconf_xml_data)
        logging.debug(f"configure interface resp: {resp}")

    def configure_interface(self, name: str, ipv4: str, mask: int, enable: bool = True):
        self.configure(f'''
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>{name}</name>
                <enabled>{"true" if enable else "false"}</enabled>
                <description>interface configured via netconf</description>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>{ipv4}</ip>
                        <netmask>{netmask_to_dot_notation(mask)}</netmask>
                    </address>
                </ipv4>
                <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
            </interface>
        </interfaces>
</config>
''')

    def configure_static_route(self, static_route: StaticRoute):
        # https://github.com/ArRosid/netconf-static-route/blob/master/static_route_template.xml
        self.configure(f'''
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
                        <destination-prefix>{static_route.ipv4}/{static_route.netmask}</destination-prefix>
                        <next-hop>
                           <next-hop-address>{static_route.gateway_ipv4}</next-hop-address>
                        </next-hop>
                     </route>
                  </ipv4>
               </static-routes>
            </routing-protocol>
         </routing-protocols>
      </routing-instance>
   </routing>
</config>
        ''')

    def get_static_routes(self) -> list[StaticRoute]:
        query = f'''
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <ip>
      <route>
        <vrf>
          <name>default</name>
          <ip-route-interface-forwarding-list xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ip"/>
        </vrf>
      </route>
    </ip>
  </native>
</filter>
'''
        resp = self.client.get_config('running', query)
        # TODO parse it
        return []

    def get_interface_configs(self) -> list[Interface]:
        query = f'''
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface></interface>
    </interfaces>
</filter>
'''
        resp = self.client.get_config('running', query)
        interfaces = []

        root = ET.fromstring(resp)
        namespace = {'ns': 'urn:ietf:params:xml:ns:yang:ietf-interfaces'}
        interfaces_xml = root.findall('.//ns:interface', namespace)
        for interface_xml in interfaces_xml:
            try:
                name = interface_xml.find('ns:name', namespace).text
                enabled = interface_xml.find('ns:enabled', namespace).text

                if enabled != 'true':
                    continue

                ip_ns = {'ns': "urn:ietf:params:xml:ns:yang:ietf-ip"}
                ipv4_xml = interface_xml.find('ns:ipv4', ip_ns)

                ip = ipv4_xml.find('ns:address/ns:ip', ip_ns)
                netmask = ipv4_xml.find('ns:address/ns:netmask', ip_ns)
                interfaces.append(Interface(
                    None, name, ip.text, netmask_from_dot_notation(netmask.text), True))
            except:
                continue
        return interfaces
