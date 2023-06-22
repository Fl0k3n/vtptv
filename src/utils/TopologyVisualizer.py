import networkx as nx
from matplotlib import pyplot as plt

from model.Topology import Topology


class TopologyVisualizer:
    def __init__(self, layout=nx.layout.planar_layout) -> None:
        self.layout = layout

    def visualize(self, topology: Topology):
        G = nx.Graph()

        for node in topology.nodes:
            G.add_node(node.name)

        for node in topology.nodes:
            for neigh in node.neighbours:
                G.add_edge(node.name, neigh.name)

        node_positions = self.layout(G)
        nx.draw(G, node_positions, with_labels=True)
        plt.show()
