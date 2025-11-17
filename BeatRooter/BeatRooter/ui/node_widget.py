from PyQt6.QtWidgets import QGraphicsObject, QMenu, QInputDialog
from PyQt6.QtCore import Qt, QRectF, pyqtSignal, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QFont, QAction, QLinearGradient
from models.node import Node
from core.node_factory import NodeFactory

class NodeWidget(QGraphicsObject):
    node_updated = pyqtSignal(object)
    connection_started = pyqtSignal(object)
    positionChanged = pyqtSignal()
    
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
            if 'geo_location' in self.node.data and self.node.data['geo_location']:
                lines.append(f"{self.node.data['geo_location']}")
            if 'threat_level' in self.node.data and self.node.data['threat_level'] != 'unknown':
                lines.append(f"{self.node.data['threat_level']}")
                
        elif self.node.type == 'domain':
            if 'name' in self.node.data and self.node.data['name']:
                lines.append(self.node.data['name'])
            if 'registrar' in self.node.data and self.node.data['registrar']:
                lines.append(f"{self.node.data['registrar']}")
                
        elif self.node.type == 'user':
            if 'username' in self.node.data and self.node.data['username']:
                lines.append(self.node.data['username'])
            if 'email' in self.node.data and self.node.data['email']:
                lines.append(f"{self.node.data['email']}")
            if 'role' in self.node.data and self.node.data['role']:
                lines.append(f"{self.node.data['role']}")
                
        elif self.node.type == 'credential':
            if 'username' in self.node.data and self.node.data['username']:
                lines.append(self.node.data['username'])
            if 'source' in self.node.data and self.node.data['source']:
                lines.append(f"{self.node.data['source']}")
            if 'compromised' in self.node.data and self.node.data['compromised']:
                lines.append("Compromised")
                
        elif self.node.type == 'attack':
            if 'type' in self.node.data and self.node.data['type']:
                lines.append(self.node.data['type'])
            if 'severity' in self.node.data and self.node.data['severity']:
                lines.append(f"{self.node.data['severity']}")
            if 'technique' in self.node.data and self.node.data['technique']:
                lines.append(f"{self.node.data['technique']}")
                
        elif self.node.type == 'vulnerability':
            if 'cve' in self.node.data and self.node.data['cve']:
                lines.append(self.node.data['cve'])
            if 'severity' in self.node.data and self.node.data['severity']:
                lines.append(f"{self.node.data['severity']}")
            if 'exploited' in self.node.data and self.node.data['exploited']:
                lines.append("Exploited")
                
        elif self.node.type == 'host':
            if 'hostname' in self.node.data and self.node.data['hostname']:
                lines.append(self.node.data['hostname'])
            if 'ip' in self.node.data and self.node.data['ip']:
                lines.append(f"{self.node.data['ip']}")
            if 'os' in self.node.data and self.node.data['os']:
                lines.append(f"{self.node.data['os']}")
                
        elif self.node.type == 'note':
            if 'content' in self.node.data and self.node.data['content']:
                content = self.node.data['content']
                if len(content) > 20:
                    content = content[:20] + "..."
                lines.append(content)
            if 'priority' in self.node.data and self.node.data['priority']:
                lines.append(f"{self.node.data['priority']}")
                
        elif self.node.type == 'screenshot':
            if 'filename' in self.node.data and self.node.data['filename']:
                lines.append(self.node.data['filename'])
            if 'timestamp' in self.node.data and self.node.data['timestamp']:
                lines.append(f"{self.node.data['timestamp']}")
        
        if not lines:
            lines.append(self.node.type)
            
        return lines
    
    def mouseDoubleClickEvent(self, event):
        self.node_updated.emit(self.node)
        super().mouseDoubleClickEvent(event)
    
    def contextMenuEvent(self, event):
        print(f"Node context menu requested for: {self.node.id}")
        
        menu = QMenu()
        
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
        scene = self.scene()
        if scene:
            scene.removeItem(self)
    
    def itemChange(self, change, value):
        if change == QGraphicsObject.GraphicsItemChange.ItemPositionChange and self.scene():
            self.node.position = value
            self.positionChanged.emit()
        return super().itemChange(change, value)