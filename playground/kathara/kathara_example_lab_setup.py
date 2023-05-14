from Kathara.manager.Kathara import Kathara
from Kathara.model.Lab import Lab

'''
pc1 --(Subnet A)-- r1 --(Subnet B)-- pc2
'''
lab = Lab("test1")

r1 = lab.get_or_new_machine("r1")
lab.connect_machine_to_link(r1.name, "A")
lab.connect_machine_to_link(r1.name, "B")

r1.update_meta(args={
    "image": "kathara/quagga",
    "exec_commands": [
        "ifconfig eth0 195.11.14.1/24 up",
        "ifconfig eth1 195.11.15.1/24 up"
    ]
})

pc1 = lab.get_or_new_machine("pc1")
lab.connect_machine_to_link(pc1.name, "A")
pc1.update_meta(args={
    "image": "kathara/base",
    "exec_commands": [
        "ifconfig eth0 195.11.14.2/24 up",
        "route add default gw 195.11.14.1 dev eth0"
    ]
})

pc2 = lab.get_or_new_machine("pc2")
lab.connect_machine_to_link(pc2.name, "B")
pc2.update_meta(args={
    "image": "kathara/base",
    "exec_commands": [
        "ifconfig eth0 195.11.15.2/24 up",
        "route add default gw 195.11.15.1 dev eth0"
    ]
})

Kathara.get_instance().deploy_lab(lab)



