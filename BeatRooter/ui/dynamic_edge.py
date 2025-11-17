from PyQt6.QtWidgets import QGraphicsPathItem
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QPainterPath, QPen, QColor, QPainter, QBrush
import math

class DynamicEdge(QGraphicsPathItem):
    def __init__(self, source_node, target_node, edge_data=None):
        super().__init__()
        self.source_node = source_node
        self.target_node = target_node
        self.edge_data = edge_data or {}
        
        self.setZValue(-1)
        self.setAcceptHoverEvents(True)
        
        self.normal_color = QColor(100, 150, 255)
        self.hover_color = QColor(255, 200, 50)
        self.selected_color = QColor(255, 100, 100)
        
        self.current_color = self.normal_color
        self.line_width = 3
        
        self.source_node.positionChanged.connect(self.update_path)
        self.target_node.positionChanged.connect(self.update_path)
        
        self.update_path()
        
    def update_path(self):
        if not self.source_node or not self.target_node:
            return
            
        source_rect = self.source_node.boundingRect()
        target_rect = self.target_node.boundingRect()

        source_scene_pos = self.source_node.scenePos()
        target_scene_pos = self.target_node.scenePos()
        
        start_point = QPointF(
            source_scene_pos.x() + source_rect.width()/2,
            source_scene_pos.y()
        )
        
        end_point = QPointF(
            target_scene_pos.x() - target_rect.width()/2,
            target_scene_pos.y()
        )
        
        path = QPainterPath()
        path.moveTo(start_point)
        
        dx = end_point.x() - start_point.x()
        dy = end_point.y() - start_point.y()

        control_offset = abs(dx) * 0.5
        
        ctrl1 = QPointF(start_point.x() + control_offset, start_point.y())
        ctrl2 = QPointF(end_point.x() - control_offset, end_point.y())
        
        path.cubicTo(ctrl1, ctrl2, end_point)
        
        self.setPath(path)
        self.update()
    
    def hoverEnterEvent(self, event):
        self.current_color = self.hover_color
        self.line_width = 4
        self.update()
        super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event):
        self.current_color = self.normal_color
        self.line_width = 3
        self.update()
        super().hoverLeaveEvent(event)
    
    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        pen = QPen(self.current_color)
        pen.setWidth(self.line_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        
        self.setPen(pen)
        super().paint(painter, option, widget)