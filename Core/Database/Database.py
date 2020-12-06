import networkx as nx
import os

database_folder = f'Settings/Database'
database_file = f'graph.gpickle'
database_path = os.path.join(database_folder, database_file)


class Database:
    def __init__(self):
        self.graph: nx.classes.Graph = None
        self.load_graph()


    def load_graph(self):
        os.makedirs(database_folder, exist_ok=True)
        if os.path.exists(database_path):
            self.graph = nx.read_gpickle(database_path)
        else:
            self.graph = nx.Graph()

    def save(self):
        nx.write_gpickle(self.graph, database_path)


# Note To Self: I was seeing how to generate the graphs with classes.