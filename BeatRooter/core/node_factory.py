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
                'os': '',
                'services': '',
                'ports': '',
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
                'name_servers': '',
                'subnames': '',
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
                'phone': '',
                'last_login': '',
                'notes': ''
            }
        },
        'credential': {
            'name': 'Credential',
            'color': '#fdcb6e',
            'default_data': {
                'username': '',
                'domain': '',
                'credential_type': 'password',
                'password': '',
                'password_hash': '',
                'source': '',
                'compromised': False,
                'privilege_level': '',
                'notes': ''
            }
        },
        'attack': {
            'name': 'Attack',
            'color': "#ff0000",
            'default_data': {
                'type': '',
                'technique': '',
                'timestamp': '',
                'severity': 'high',
                'source': '',
                'target': '',
                'successful': False,
                'notes': ''
            }
        },
        'vulnerability': {
            'name': 'Vulnerability',
            'color': '#ffa500',
            'default_data': {
                'cve': 'CVE-XXXX-XXXX',
                'name': '',
                'severity': 'medium',
                'description': '',
                'exploited': False,
                'affected_hosts': '',
                'impact': '',
                'notes': ''
            }
        },
        'host': {
            'name': 'Host',
            'color': '#96ceb4',
            'default_data': {
                'hostname': 'server-01',
                'ip_address': '',
                'os': '',
                'domain': '',
                'role': '',
                'services': '',
                'notes': ''
            }
        },
        'note': {
            'name': 'Note',
            'color': '#ffeaa7',
            'default_data': {
                'title': '',
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
                'filename': '',
                'file_path': '',
                'image_data': '',
                'timestamp': '',
                'description': '',
                'tags': '',
                'file_size': '',
                'dimensions': '',
                'format': '',
                'metadata': {},
                'notes': ''
            }
        },
        'command': {
            'name': 'Command',
            'color': '#6c5ce7',
            'default_data': {
                'command': 'whoami',
                'output': '',
                'timestamp': '',
                'executed_on': '',
                'privilege_level': '',
                'exit_code': 0,
                'notes': ''
            }
        },
        'script': {
            'name': 'Script',
            'color': '#00b894',
            'default_data': {
                'filename': 'script.sh',
                'file_path': '',
                'language': 'bash',
                'content': '',
                'purpose': '',
                'execution_result': '',
                'parameters': '',
                'timestamp': '',
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