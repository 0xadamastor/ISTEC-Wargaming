from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QListWidget, QListWidgetItem,
                             QComboBox, QGroupBox, QScrollArea)
from PyQt6.QtCore import pyqtSignal, Qt
from core.node_factory import NodeFactory

class ToolboxWidget(QWidget):
    node_created = pyqtSignal(str)
    
    def __init__(self, graph_manager):
        super().__init__()
        self.graph_manager = graph_manager
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        search_group = QGroupBox("Search & Filter")
        search_layout = QVBoxLayout(search_group)
        search_layout.setContentsMargins(8, 12, 8, 12)
        search_layout.setSpacing(6)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search nodes...")
        self.search_input.setMinimumHeight(30)
        search_layout.addWidget(self.search_input)
        
        search_layout.addWidget(QLabel("Filter by type:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Show All", [])
        for node_type, config in NodeFactory.NODE_TYPES.items():
            self.filter_combo.addItem(config['name'], [node_type])
        search_layout.addWidget(self.filter_combo)
        
        layout.addWidget(search_group)
        
        creation_group = QGroupBox("Create Nodes")
        creation_layout = QVBoxLayout(creation_group)
        creation_layout.setContentsMargins(8, 12, 8, 12)
        creation_layout.setSpacing(6)

        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(2, 2, 2, 2)
        scroll_layout.setSpacing(4)
        
        for node_type, config in NodeFactory.NODE_TYPES.items():
            btn = QPushButton(config['name'])
            btn.setProperty('nodeType', node_type)
            btn.clicked.connect(self.on_node_button_click)
            btn.setMinimumHeight(35)
            scroll_layout.addWidget(btn)
        
        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(400)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        creation_layout.addWidget(scroll_area)
        layout.addWidget(creation_group)
        
        layout.addStretch()
    
    def on_node_button_click(self):
        sender = self.sender()
        node_type = sender.property('nodeType')
        self.node_created.emit(node_type)