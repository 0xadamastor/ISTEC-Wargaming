from PyQt6.QtCore import QPointF
from models.graph_data import GraphData
from models.node import Node
from models.edge import Edge

class GraphManager:
    def __init__(self):
        self.graph_data = GraphData()
        self.node_counter = 0
        self.edge_counter = 0
    
    def add_node(self, node_type: str, position: QPointF, data: dict = None) -> Node:
        node_id = f"node_{self.node_counter}"
        node = Node(node_id, node_type, position, data)
        self.graph_data.nodes[node_id] = node
        self.node_counter += 1
        return node
    
    def remove_node(self, node_id: str):
        if node_id in self.graph_data.nodes:
            edges_to_remove = []
            for edge_id, edge in self.graph_data.edges.items():
                if edge.source_id == node_id or edge.target_id == node_id:
                    edges_to_remove.append(edge_id)
            
            for edge_id in edges_to_remove:
                self.remove_edge(edge_id)
            
            del self.graph_data.nodes[node_id]
    
    def connect_nodes(self, source_id: str, target_id: str, label: str = "", 
                     edge_type: str = "connection") -> Edge:
        if source_id not in self.graph_data.nodes or target_id not in self.graph_data.nodes:
            raise ValueError("Source or target node not found")
        
        edge_id = f"edge_{self.edge_counter}"
        edge = Edge(edge_id, source_id, target_id, label, edge_type)
        self.graph_data.edges[edge_id] = edge
        
        self.graph_data.nodes[source_id].add_connection(edge_id)
        self.graph_data.nodes[target_id].add_connection(edge_id)
        
        self.edge_counter += 1
        return edge
    
    def remove_edge(self, edge_id: str):
        if edge_id in self.graph_data.edges:
            edge = self.graph_data.edges[edge_id]
        
            if edge.source_id in self.graph_data.nodes:
                self.graph_data.nodes[edge.source_id].remove_connection(edge_id)
            if edge.target_id in self.graph_data.nodes:
                self.graph_data.nodes[edge.target_id].remove_connection(edge_id)
            
            del self.graph_data.edges[edge_id]
    
    def get_node(self, node_id: str) -> Node:
        return self.graph_data.nodes.get(node_id)
    
    def get_edge(self, edge_id: str) -> Edge:
        return self.graph_data.edges.get(edge_id)
    
    def get_connected_nodes(self, node_id: str) -> list:
        connected = []
        if node_id in self.graph_data.nodes:
            node = self.graph_data.nodes[node_id]
            for edge_id in node.connections:
                edge = self.graph_data.edges[edge_id]
                other_id = edge.target_id if edge.source_id == node_id else edge.source_id
                if other_id in self.graph_data.nodes:
                    connected.append(self.graph_data.nodes[other_id])
        return connected
    
    def clear_graph(self):
        self.graph_data.clear()
        self.node_counter = 0
        self.edge_counter = 0