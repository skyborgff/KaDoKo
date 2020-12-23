import networkx as nx
import os
from networkx.readwrite import json_graph
import json
import pickle
import jsonpickle

database_folder = f'Settings/Database'
database_file = f'graph.gpickle'
database_path = os.path.join(database_folder, database_file)


class Database:
    def __init__(self):
        self.graph: nx.classes.DiGraph = None
        self.load_graph()


    def load_graph(self):
        os.makedirs(database_folder, exist_ok=True)
        if os.path.exists(database_path):
            self.graph = nx.read_gpickle(database_path)
        else:
            self.graph = nx.DiGraph()

    def save(self):
        nx.write_gpickle(self.graph, database_path)

    def generate_graph(self, path):
        print('Generating Graph')
        d = json_graph.node_link_data(self.graph)
        data = jsonpickle.encode(d, unpicklable=True, indent=1)
        with open(path, "w+") as file:
            file.write(data)
        print(f"Wrote node-link JSON data to {path}")

    def remove_successor_edges(self, node_hash):
        successors = self.graph.successors(node_hash)
        successors_list = []
        for successor in successors:
            successors_list.append(successor)
        for successor in successors_list:
            self.graph.remove_edge(node_hash, successor)

    def getByClass(self, node_class):
        found = []
        for node_hash in self.graph.nodes:
            node = self.graph.nodes[node_hash]
            node_raw = node.get('raw')
            if node_raw:
                if type(node_raw) == node_class:
                    found.append(node_hash)
        return found

    def add_node(self, node, label: str, raw: bool = False)-> str:
        if raw:
            raw_node = node
        else:
            raw_node = type(node)()
        try:
            n_hash = node.hash
        except:
            n_hash = str(hash(node))
        self.graph.add_node(n_hash, data_class=type(node).__name__, label=label, raw=raw_node)
        return n_hash

    def add_edge(self, edge1, edge2):
        self.graph.add_edge(edge1, edge2)


# Note To Self: Pickling stuff for the graph
# Todo: add the graph into the UI