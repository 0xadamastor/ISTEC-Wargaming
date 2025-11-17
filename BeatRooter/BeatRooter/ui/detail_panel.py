from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTextEdit, QComboBox, QPushButton,
                             QGroupBox, QFormLayout, QScrollArea)
from PyQt6.QtCore import pyqtSignal, Qt

class DetailPanel(QWidget):
    node_data_updated = pyqtSignal(object)
    node_deleted = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self.current_node = None
        self.setup_ui()
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(10)
        
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        layout = QVBoxLayout(scroll_widget)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(10)
        
        info_group = QGroupBox("Node Information")
        info_layout = QFormLayout(info_group)
        info_layout.setContentsMargins(10, 15, 10, 15)
        info_layout.setSpacing(8)
        
        self.node_type_label = QLabel("None")
        self.node_id_label = QLabel("None")
        
        info_layout.addRow("Type:", self.node_type_label)
        info_layout.addRow("ID:", self.node_id_label)
        
        layout.addWidget(info_group)
        
        self.data_group = QGroupBox("Edit Data")
        self.data_layout = QFormLayout(self.data_group)
        self.data_layout.setContentsMargins(10, 15, 10, 15)
        self.data_layout.setSpacing(8)
        self.data_group.setVisible(False)
        
        self.data_fields = {}
        
        layout.addWidget(self.data_group)
        
        notes_group = QGroupBox("Notes")
        notes_layout = QVBoxLayout(notes_group)
        notes_layout.setContentsMargins(10, 15, 10, 15)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setPlaceholderText("Add investigation notes here...")
        self.notes_edit.setMaximumHeight(120)
        self.notes_edit.textChanged.connect(self.on_notes_changed)
        notes_layout.addWidget(self.notes_edit)
        
        layout.addWidget(notes_group)

        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout(actions_group)
        actions_layout.setContentsMargins(10, 15, 10, 15)
        actions_layout.setSpacing(8)
        
        self.save_btn = QPushButton("Save Changes")
        self.save_btn.clicked.connect(self.save_changes)
        self.delete_btn = QPushButton("Delete Node")
        self.delete_btn.clicked.connect(self.delete_node)
        
        actions_layout.addWidget(self.save_btn)
        actions_layout.addWidget(self.delete_btn)
        
        layout.addWidget(actions_group)
        
        layout.addStretch()
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        main_layout.addWidget(scroll_area)
        
        self.clear_panel()
    
    def display_node(self, node):
        self.current_node = node
        self.node_type_label.setText(node.type.upper())
        self.node_id_label.setText(node.id)
        
        self.clear_data_fields()
        
        for key, value in node.data.items():
            if key == 'notes':
                self.notes_edit.setPlainText(str(value))
            else:
                self.create_data_field(key, value)
        
        self.data_group.setVisible(len(self.data_fields) > 0)
        self.setEnabled(True)
    
    def create_data_field(self, key, value):
        label = QLabel(key.replace('_', ' ').title() + ":")
        
        if isinstance(value, bool):
            field = QComboBox()
            field.addItems(["False", "True"])
            field.setCurrentText(str(value))
        elif key in ['threat_level', 'severity', 'priority']:
            field = QComboBox()
            field.addItems(["low", "medium", "high", "critical"])
            field.setCurrentText(str(value))
        elif isinstance(value, str) and len(value) > 50:
            field = QTextEdit()
            field.setPlainText(value)
            field.setMaximumHeight(80)
        else:
            field = QLineEdit()
            field.setText(str(value))
        
        field.setProperty('fieldKey', key)

        if isinstance(field, (QLineEdit, QTextEdit)):
            field.textChanged.connect(self.on_field_changed)
        elif isinstance(field, QComboBox):
            field.currentTextChanged.connect(self.on_field_changed)
        
        self.data_fields[key] = field
        self.data_layout.addRow(label, field)
    
    def clear_data_fields(self):
        for i in reversed(range(self.data_layout.count())):
            item = self.data_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
        
        self.data_fields.clear()
    
    def clear_panel(self):
        self.current_node = None
        self.node_type_label.setText("None")
        self.node_id_label.setText("None")

        for i in reversed(range(self.data_layout.count())):
            item = self.data_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
        
        self.data_fields.clear()
        self.notes_edit.clear()
        self.data_group.setVisible(False)
        self.setEnabled(False)
    
    def on_field_changed(self):
        if not self.current_node:
            return
            
        sender = self.sender()
        key = sender.property('fieldKey')
        
        if isinstance(sender, QLineEdit):
            self.current_node.data[key] = sender.text()
        elif isinstance(sender, QTextEdit):
            self.current_node.data[key] = sender.toPlainText()
        elif isinstance(sender, QComboBox):
            value = sender.currentText()
            if value.lower() in ['true', 'false']:
                self.current_node.data[key] = value.lower() == 'true'
            else:
                self.current_node.data[key] = value
    
    def on_notes_changed(self):
        if self.current_node:
            self.current_node.data['notes'] = self.notes_edit.toPlainText()
    
    def save_changes(self):
        if self.current_node:
            self.node_data_updated.emit(self.current_node)
    
    def delete_node(self):
        if self.current_node:
            self.node_deleted.emit(self.current_node)
            self.clear_panel()