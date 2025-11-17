from PyQt6.QtWidgets import QGraphicsObject, QMenu, QInputDialog
from PyQt6.QtCore import Qt, QRectF, pyqtSignal, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QFont, QAction, QLinearGradient
from models.node import Node
from core.node_factory import NodeFactory

class NodeWidget(QGraphicsObject):
    node_updated = pyqtSignal(object)
    connection_started = pyqtSignal(object)
    positionChanged = pyqtSignal()
    node_deleted = pyqtSignal(object)
    
    def __init__(self, node):
        super().__init__()
        self.node = node
        self.setPos(node.position)
        self.setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsObject.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        self.width = 140
        self.height = 90
        self.corner_radius = 12
        
        self.setZValue(1)
    
    def boundingRect(self):
        return QRectF(-self.width/2, -self.height/2, self.width, self.height)
    
    def paint(self, painter, option, widget):
        color = QColor(NodeFactory.get_node_color(self.node.type))

        gradient = QLinearGradient(
            QPointF(-self.width/2, -self.height/2), 
            QPointF(self.width/2, self.height/2)
        )
        gradient.setColorAt(0, color.lighter(120))
        gradient.setColorAt(1, color.darker(120))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(QColor(50, 50, 50), 2))
        
        rect = QRectF(-self.width/2, -self.height/2, self.width, self.height)
        painter.drawRoundedRect(rect, self.corner_radius, self.corner_radius)
        
        if self.isSelected():
            painter.setPen(QPen(QColor(255, 255, 0), 3))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRoundedRect(rect, self.corner_radius, self.corner_radius)
        
        painter.setPen(QPen(QColor(0, 0, 0)))
        font = QFont("Arial", 9, QFont.Weight.Bold)
        painter.setFont(font)

        type_text = NodeFactory.get_node_name(self.node.type)
        painter.drawText(int(-self.width/2 + 8), int(-self.height/2 + 18), type_text)
        
        font.setWeight(QFont.Weight.Normal)
        font.setPointSize(8)
        painter.setFont(font)
        
        data_lines = self.get_data_fields_to_display()
        
        y_offset = 35
        line_height = 15
        max_lines = 3
        
        for i, line in enumerate(data_lines[:max_lines]):
            painter.drawText(int(-self.width/2 + 8), int(-self.height/2 + y_offset + i * line_height), line)
    
    def get_data_fields_to_display(self):
        lines = []
        
        if self.node.type == 'ip':
            if 'address' in self.node.data and self.node.data['address']:
                lines.append(self.node.data['address'])
            if 'os' in self.node.data and self.node.data['os']:
                lines.append(f"OS: {self.node.data['os']}")
            if 'threat_level' in self.node.data and self.node.data['threat_level'] != 'unknown':
                lines.append(f"Threat: {self.node.data['threat_level']}")
                
        elif self.node.type == 'domain':
            if 'name' in self.node.data and self.node.data['name']:
                lines.append(self.node.data['name'])
            if 'registrar' in self.node.data and self.node.data['registrar']:
                lines.append(f"Reg: {self.node.data['registrar']}")
                
        elif self.node.type == 'user':
            if 'username' in self.node.data and self.node.data['username']:
                lines.append(self.node.data['username'])
            if 'role' in self.node.data and self.node.data['role']:
                lines.append(f"Role: {self.node.data['role']}")
            if 'department' in self.node.data and self.node.data['department']:
                lines.append(f"Dept: {self.node.data['department']}")
                
        elif self.node.type == 'credential':
            if 'username' in self.node.data and self.node.data['username']:
                lines.append(self.node.data['username'])
            if 'domain' in self.node.data and self.node.data['domain']:
                lines.append(f"Domain: {self.node.data['domain']}")
            cred_type = self.node.data.get('credential_type', 'password')
            if cred_type == 'password' and 'password' in self.node.data and self.node.data['password']:
                lines.append("Has Password")
            elif cred_type == 'hash' and 'password_hash' in self.node.data and self.node.data['password_hash']:
                lines.append("Has Hash")
            if 'compromised' in self.node.data and self.node.data['compromised']:
                lines.append("COMPROMISED")
                
        elif self.node.type == 'attack':
            if 'type' in self.node.data and self.node.data['type']:
                lines.append(self.node.data['type'])
            if 'technique' in self.node.data and self.node.data['technique']:
                lines.append(f"Tech: {self.node.data['technique']}")
            if 'severity' in self.node.data and self.node.data['severity']:
                lines.append(f"Sev: {self.node.data['severity']}")
                
        elif self.node.type == 'vulnerability':
            if 'cve' in self.node.data and self.node.data['cve']:
                lines.append(self.node.data['cve'])
            if 'name' in self.node.data and self.node.data['name']:
                lines.append(self.node.data['name'])
            if 'severity' in self.node.data and self.node.data['severity']:
                lines.append(f"Sev: {self.node.data['severity']}")
            if 'exploited' in self.node.data and self.node.data['exploited']:
                lines.append("EXPLOITED")
                
        elif self.node.type == 'host':
            if 'hostname' in self.node.data and self.node.data['hostname']:
                lines.append(self.node.data['hostname'])
            if 'ip_address' in self.node.data and self.node.data['ip_address']:
                lines.append(f"IP: {self.node.data['ip_address']}")
            if 'os' in self.node.data and self.node.data['os']:
                lines.append(f"OS: {self.node.data['os']}")
                
        elif self.node.type == 'note':
            if 'title' in self.node.data and self.node.data['title']:
                lines.append(self.node.data['title'])
            elif 'content' in self.node.data and self.node.data['content']:
                content = self.node.data['content']
                if len(content) > 20:
                    content = content[:20] + "..."
                lines.append(content)
                
        elif self.node.type == 'screenshot':
            if 'filename' in self.node.data and self.node.data['filename']:
                lines.append(self.node.data['filename'])
            if 'dimensions' in self.node.data and self.node.data['dimensions']:
                lines.append(self.node.data['dimensions'])
            if 'file_size' in self.node.data and self.node.data['file_size']:
                lines.append(self.node.data['file_size'])
            elif 'description' in self.node.data and self.node.data['description']:
                desc = self.node.data['description']
                if len(desc) > 20:
                    desc = desc[:20] + "..."
                lines.append(desc)

        elif self.node.type == 'command':
            if 'command' in self.node.data and self.node.data['command']:
                cmd = self.node.data['command']
                if len(cmd) > 25:
                    cmd = cmd[:25] + "..."
                lines.append(cmd)
            if 'executed_on' in self.node.data and self.node.data['executed_on']:
                lines.append(f"On: {self.node.data['executed_on']}")
            if 'exit_code' in self.node.data and self.node.data['exit_code'] != 0:
                lines.append(f"Exit: {self.node.data['exit_code']}")

        elif self.node.type == 'script':
            if 'filename' in self.node.data and self.node.data['filename']:
                lines.append(self.node.data['filename'])
            if 'language' in self.node.data and self.node.data['language']:
                lines.append(f"Lang: {self.node.data['language']}")
            if 'purpose' in self.node.data and self.node.data['purpose']:
                purpose = self.node.data['purpose']
                if len(purpose) > 20:
                    purpose = purpose[:20] + "..."
                lines.append(purpose)
        
        if not lines:
            lines.append(self.node.type)
            
        return lines
    
    def mouseDoubleClickEvent(self, event):
        self.node_updated.emit(self.node)
        super().mouseDoubleClickEvent(event)
    
    def contextMenuEvent(self, event):
        print(f"Node context menu requested for: {self.node.id}")
        
        menu = QMenu()
        
        menu.setStyleSheet("""
            QMenu {
                background-color: #2a2a3a;
                color: #cdd6f4;
                border: 1px solid #45475a;
                border-radius: 6px;
                padding: 4px;
            }
            QMenu::item {
                background-color: transparent;
                color: #cdd6f4;
                padding: 6px 20px;
                border-radius: 4px;
                font-family: 'Segoe UI', 'Arial';
                font-size: 11px;
            }
            QMenu::item:selected {
                background-color: #89b4fa;
                color: #1e1e2e;
            }
            QMenu::item:disabled {
                color: #6c7086;
            }
            QMenu::separator {
                height: 1px;
                background-color: #45475a;
                margin: 4px 8px;
            }
        """)
        
        connect_action = QAction("Start Connection", self)
        connect_action.triggered.connect(lambda: self.connection_started.emit(self))
        menu.addAction(connect_action)
        
        menu.addSeparator()
        
        edit_action = QAction("Edit Node", self)
        edit_action.triggered.connect(lambda: self.node_updated.emit(self.node))
        menu.addAction(edit_action)

        delete_action = QAction("Delete Node", self)
        delete_action.triggered.connect(self.delete_node)
        menu.addAction(delete_action)
        
        print("Showing node context menu...")
        menu.exec(event.screenPos())
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            print("Right click detected on node")
            event.accept()
        else:
            super().mousePressEvent(event)
    
    def delete_node(self):
        self.node_deleted.emit(self.node)
    
    def itemChange(self, change, value):
        if change == QGraphicsObject.GraphicsItemChange.ItemPositionChange and self.scene():
            self.node.position = value
            self.positionChanged.emit()
        return super().itemChange(change, value)