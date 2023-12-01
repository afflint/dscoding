from typing import List

import pandas as pd
from pyvis.network import Network


class Node:
    def __init__(self, id: str, name: str,
                 lat: float, lng: float):
        self.id = id
        self.name = name
        self.lat = lat
        self.lng = lng


class Edge:
    def __init__(self, start: Node, end: Node):
        self.start = start
        self.end = end
        self.weight = 1


class Graph:
    def __init__(self):
        self.nodes = {}
        self.node_list = []
        self.edges = {}

    def add_node(self, node: Node):
        if node.id in self.nodes.keys():
            pass
        else:
            self.nodes[node.id] = node
            self.node_list.append(node.id)

    def add_edge(self, start: Node, end: Node):
        if (start.id, end.id) in self.edges.keys():
            self.edges[(start.id, end.id)].weight += 1
        else:
            self.edges[(start.id, end.id)] = Edge(start, end)

    def directions(self, location: Node) -> List[Edge]:
        return [e for e in self.edges if e.start == location]

    def to_pyvis(self):
        net = Network()
        nodes = list(range(len(self.node_list)))
        names, lat, lng = [], [], []
        for node_id, node in self.nodes.items():
            names.append(node.name)
            lat.append(node.lat)
            lng.append(node.lng)
        net.add_nodes(nodes,
                      label=names,
                      y=lat,
                      x=lng)
        for edge in self.edges.values():
            net.add_edge(
                source=self.node_list.index(edge.start.id),
                to=self.node_list.index(edge.end.id),
                weight=edge.weight
            )
        return net

    @classmethod
    def from_bike_df(cls, df: pd.DataFrame):
        g = cls()
        for i, row in df.iterrows():
            start_node = Node(
                id=row.start_station_id,
                name=row.start_station_name,
                lat=row.start_lat,
                lng=row.start_lng
            )
            end_node = Node(
                id=row.end_station_id,
                name=row.end_station_name,
                lat=row.end_lat,
                lng=row.end_lng
            )
            g.add_node(start_node)
            g.add_node(end_node)
            g.add_edge(start_node, end_node)
        return g

