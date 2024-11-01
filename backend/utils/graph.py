# backend/utils/graph.py

class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_vertex(self, vertex: str):
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, vertex1: str, vertex2: str):
        if vertex1 in self.adj_list and vertex2 in self.adj_list:
            self.adj_list[vertex1].append(vertex2)
            self.adj_list[vertex2].append(vertex1)

    def get_neighbors(self, vertex: str):
        return self.adj_list.get(vertex, [])

    def display_graph(self):
        for vertex, edges in self.adj_list.items():
            print(f"{vertex} --> {', '.join(edges)}")
