import sys
import xml.dom.minidom
from argparse import ArgumentParser

from ncclient import manager


def edit(mgr):
    data = \
'''
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <hostname>NC-WAS-HERE</hostname>
    </native>
</config>
'''

    xml_resp = mgr.edit_config(data, target='running')
    return xml_resp

def print_capabilities(mgr):
    with open('cap.txt', 'w') as f:
        for cap in mgr.server_capabilities:
            print(cap, file=f)

def get_schema_of(mgr, schema_id):
    return mgr.get_schema(schema_id) 

def pretty_print(rpc_resp):
    print(xml.dom.minidom.parseString(str(rpc_resp)).toprettyxml(indent="  "))

def to_file(rpc_resp, name):
    with open(name, 'w') as f:
        print(xml.dom.minidom.parseString(str(rpc_resp)).toprettyxml(indent="  "), file=f)

def configure_hostname(mgr):
    data = '''
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <hostname>NETCONFH</hostname>
        </native>
     </config>
    '''
    
    return mgr.edit_config(data, target='running')

def configure_loopback(mgr):
    data = '''
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>Loopback13</name>
                    <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                    <enabled>false</enabled>
                    <description>my loopback feel free to remove</description>
                    <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                        <address>
                            <ip>3.3.3.3</ip>
                            <netmask>255.0.0.0</netmask>
                        </address>
                    </ipv4>
                    <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                </interface>
            </interfaces>
    </config>
'''
    pretty_print(mgr.edit_config(data, target='running'))

def delete_loopback(mgr):
    data = '''
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface operation='delete'>
                    <name>Loopback13</name>
                </interface>
            </interfaces>
    </config>
'''  
    pretty_print(mgr.edit_config(data, target='running'))

def get_loopback_config(mgr):
    filter = '''
    <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>Loopback13</name>
                </interface>
            </interfaces>
    </filter>
'''
    pretty_print(m.get_config('running', filter))


if __name__ == '__main__':
    # sandbox cisco devnet
    m =  manager.connect(host='sandbox-iosxe-latest-1.cisco.com',
                         port=830,
                         username='admin',
                         password='C1sco12345',
                         device_params={'name':"csr"})

    # physial
    # m =  manager.connect(host='1.1.1.1',
    #                      port=830,
    #                      username='cisco',
    #                      password='cisco123!',
    #                      device_params={'name':"csr"})


    hostname_filter = '''
                      <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
                          <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                          <hostname></hostname>
                          </native>
                      </filter>
                      '''

       # Pretty print the XML reply
    # xmlDom = xml.dom.minidom.parseString( str( m.get_config('running', hostname_filter)))
    # print(xmlDom.toprettyxml( indent = "  " ))
    # print_capabilities(m)
    # xml_resp = edit(m)
    # pretty_print(xml_resp)
    # to_file(get_schema_of(m, 'Cisco-IOS-XE-interface-common'), 'iface.yang')
    # to_file(m.get_config('running'), 'whole_config.yang')
    # pretty_print(configure_hostname(m))
    # pretty_print(m.get_config('running', hostname_filter))
    # get_loopback_config(m)
    # configure_loopback(m)
    # delete_loopback(m)
