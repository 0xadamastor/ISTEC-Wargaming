from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Edge:
    id: str
    source_id: str
    target_id: str
    label: str
    edge_type: str
    color: str
    style: str
    
    def __init__(self, edge_id: str, source_id: str, target_id: str, label: str = "", 
                 edge_type: str = "connection", color: str = "#ff4444", style: str = "solid"):
        self.id = edge_id
        self.source_id = source_id
        self.target_id = target_id
        self.label = label
        self.edge_type = edge_type
        self.color = color
        self.style = style
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'source': self.source_id,
            'target': self.target_id,
            'label': self.label,
            'type': self.edge_type,
            'color': self.color,
            'style': self.style
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            data['id'],
            data['source'],
            data['target'],
            data.get('label', ''),
            data.get('type', 'connection'),
            data.get('color', '#ff4444'),
            data.get('style', 'solid')
        )