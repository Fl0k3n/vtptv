import networkx as nx
from matplotlib import pyplot as plt

from model.devices.Node import NodeRole
from model.Topology import Topology


class TopologyVisualizer:
    def __init__(self, layout=nx.layout.planar_layout) -> None:
        self.layout = layout
        self.role_to_color = {
            NodeRole.HOST: 'green',
            NodeRole.SWITCH: 'blue',
            NodeRole.ROUTER: 'red'
        }

    def visualize(self, topology: Topology):
        G = nx.Graph()
        colors = []
        edge_labels = {}

        for node in topology.nodes:
            G.add_node(node.name)
            colors.append(self.role_to_color[node.role])

        for node in topology.nodes:
            for neigh in node.neighbours.values():
                G.add_edge(node.name, neigh.name)
                edge_labels[(node.name, neigh.name)
                            ] = node.get_common_network(neigh)

        node_positions = self.layout(G)
        nx.draw(G, node_positions, node_color=colors,
                node_size=700, with_labels=True)

        nx.draw_networkx_edge_labels(
            G, node_positions, edge_labels=edge_labels)

        plt.show()
