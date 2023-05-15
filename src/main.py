if __name__ == "__main__":
    from Kathara.parser.netkit.LabParser import LabParser
    lab = LabParser().parse("./resources/kathara-lab_static-routing")
    # from pprint import pprint
    # pprint(lab.links)
    # print('----------------------')
    # pprint(lab.machines)
    # print('----------------------')
    # print(list(lab.machines.values())[0].startup_commands)
    
    from parser.VirtualDeviceCommandsParser import VirtualDeviceCommandsParser

    from mapper.VirtualDeviceBuilder import VirtualDeviceBuilder
    from mapper.VirtualTopologyBuilder import VirtualTopologyBuilder
    parser = VirtualDeviceCommandsParser()
    device_builder = VirtualDeviceBuilder(lab, parser)
    topo = VirtualTopologyBuilder(lab, device_builder).build()
    nodes = topo.nodes # debug
    from utils.TopologyVisualizer import TopologyVisualizer

    TopologyVisualizer().visualize(topo) 

