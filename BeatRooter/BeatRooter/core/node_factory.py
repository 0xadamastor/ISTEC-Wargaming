from PyQt6.QtCore import QPointF

class NodeFactory:
    NODE_TYPES = {
        'ip': {
            'name': 'IP Address',
            'color': '#ff6b6b',

            'default_data': {
                'address': '192.168.1.1',
                'geo_location': '',
                'threat_level': 'unknown',
                'notes': ''
            }
        },
        'domain': {
            'name': 'Domain',
            'color': '#4ecdc4',

            'default_data': {
                'name': 'example.com',
                'registrar': '',
                'creation_date': '',
                'notes': ''
            }
        },
        'user': {
            'name': 'User',
            'color': '#45b7d1',

            'default_data': {
                'username': 'john_doe',
                'email': '',
                'role': '',
                'department': '',
                'notes': ''
            }
        },
        'credential': {
            'name': 'Credential',
            'color': '#fdcb6e',

            'default_data': {
                'username': '',
                'password_hash': '',
                'source': '',
                'compromised': False,
                'notes': ''
            }
        },
        'attack': {
            'name': 'Attack',
            'color': "#ff0000",

            'default_data': {
                'type': '',
                'timestamp': '',
                'severity': 'high',
                'technique': '',
                'notes': ''
            }
        },
        'vulnerability': {
            'name': 'Vulnerability',
            'color': '#ffa500',

            'default_data': {
                'cve': 'CVE-XXXX-XXXX',
                'severity': 'medium',
                'description': '',
                'exploited': False,
                'notes': ''
            }
        },
        'host': {
            'name': 'Host',
            'color': '#96ceb4',

            'default_data': {
                'hostname': 'server-01',
                'ip': '',
                'os': '',
                'services': '',
                'notes': ''
            }
        },
        'note': {
            'name': 'Note',
            'color': '#ffeaa7',

            'default_data': {
                'content': 'Investigation note...',
                'category': '',
                'priority': 'medium',
                'notes': ''
            }
        },
        'screenshot': {
            'name': 'Screenshot',
            'color': '#dda0dd',

            'default_data': {
                'filename': 'screenshot.png',
                'timestamp': '',
                'description': '',
                'notes': ''
            }
        }
    }
    
    @classmethod
    def create_node_data(cls, node_type: str, custom_data: dict = None) -> dict:
        if node_type not in cls.NODE_TYPES:
            node_type = 'note'
        
        default_data = cls.NODE_TYPES[node_type]['default_data'].copy()
        if custom_data:
            default_data.update(custom_data)
        
        return default_data
    
    @classmethod
    def get_node_color(cls, node_type: str) -> str:
        return cls.NODE_TYPES.get(node_type, {}).get('color', '#ffffff')
    
    @classmethod
    def get_node_name(cls, node_type: str) -> str:
        return cls.NODE_TYPES.get(node_type, {}).get('name', 'Unknown')