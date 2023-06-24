import json
from typing import Iterable

import netmiko
import requests as req
from gns3fy import Gns3Connector, Link, Node, Project

server = Gns3Connector("http://localhost:3080")

BASE_URL = 'http://localhost:3080/v2/'
ROUTER_IMG = 'c7200-adventerprisek9-mz.152-4.M7.image'


def api(*elements: Iterable[object]):
    return BASE_URL + '/'.join(list(map(str, elements)))


def data(data_dict):
    return json.dumps(data_dict)


def build_simple_topo():
    # create project
    project_info = req.post(api('projects'), data({'name': 'api-test'})).json()
    if project_info['status'] == 409:
        project_info = {'auto_close': True, 'auto_open': False, 'auto_start': False, 'drawing_grid_size': 25, 'filename': 'api-test.gns3', 'grid_size': 75, 'name': 'api-test', 'path': '/home/flok3n/GNS3/projects/3867434f-b3e4-47bd-8c38-17caa794226e',
                        'project_id': '3867434f-b3e4-47bd-8c38-17caa794226e', 'scene_height': 1000, 'scene_width': 2000, 'show_grid': False, 'show_interface_labels': False, 'show_layers': False, 'snap_to_grid': False, 'status': 'opened', 'supplier': None, 'variables': None, 'zoom': 100}

    # create 2 hosts
    host1 = req.post(api('projects', project_info['project_id'], 'nodes'), data({
        "compute_id": "local",
        "name": "VPCS 1",
        "node_type": "vpcs",
    })).json()

    host2 = req.post(api('projects', project_info['project_id'], 'nodes'), data({
        "compute_id": "local",
        "name": "VPCS 2",
        "node_type": "vpcs",
    })).json()

    # create 2 routers

    router1 = req.post(api('projects', project_info['project_id'], 'nodes'), data({
        "compute_id": "local",
        "name": "R1",
        "node_type": "dynamips",
    })).json()

    print(router1)
    for template in server.get_templates():
        print(f"Template: {template['name']} -- ID: {template['template_id']}")
    try:
        # this for some reason throws error, but router is created successfuly
        router1 = Node(
            project_id=project_info['project_id'],
            connector=server,
            name='RR1',
            template='c7200_1'
        )

        router1.create()
    except:
        # ugly workaround
        for node in server.get_nodes(project_info['project_id']):
            if node['node_type'] == 'dynamips':
                router1 = node
                break

    try:
        router2 = Node(
            project_id=project_info['project_id'],
            connector=server,
            name='RR1',
            template='c7200_1'
        )

        router2.create()
    except:
        for node in server.get_nodes(project_info['project_id']):
            if node['node_type'] == 'dynamips' and node['node_id'] != router1['node_id']:
                router2 = node
                break

    print(router1['ports'][0])

    # project = Project(project_id=project_info['project_id'], connector=server)
    # link = Link(project_id=project.project_id, connector=server, nodes=[
    #     dict(node_id=router1['node_id'], adapter_number=0, port_number=0),
    #     dict(node_id=router2['node_id'], adapter_number=0, port_number=0),
    # ])
    # link.create()
    # project.create_link(router1['name'], router1['ports'][0]['name'], router2['name'], router2['ports'][0]['name'])
    print(router1['node_id'])
    req.post(api('projects', project_info['project_id'], 'links'), data({
        "nodes": [
            {"adapter_number": 0,
                "node_id": router1['node_id'], "port_number": 0},
            {"adapter_number": 0,
                "node_id": router2['node_id'], "port_number": 0}
        ]
    }))

    req.post(
        api('projects', project_info['project_id'], 'nodes', router1['node_id'], 'start'))
    req.post(
        api('projects', project_info['project_id'], 'nodes', router2['node_id'], 'start'))

    import time
    time.sleep(10)
    print('awake')
    # set addressing of router1
    ios_device = {
        'device_type': 'cisco_ios_telnet',
        'ip': 'localhost',
        'port': router1['console']
    }

    with netmiko.ConnectHandler(**ios_device) as con:
        con.config_mode()
        con.send_config_set([
            "interface fastEthernet0/0",
            "ip address 10.0.0.1 255.255.255.0",
            "no shutdown"
        ])
        con.exit_config_mode()


if __name__ == '__main__':
    build_simple_topo()
