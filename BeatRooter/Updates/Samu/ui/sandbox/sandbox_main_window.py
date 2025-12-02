import sys
import os
from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, 
    QToolBar, QStatusBar, QFileDialog, QMessageBox,
    QSplitter, QApplication, QDockWidget, QDialog
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence

from core.sandbox.sandbox_manager import SandboxManager
from ui.sandbox.sandbox_canvas_widget import SandboxCanvasWidget
from ui.sandbox.sandbox_toolbox import SandboxToolbox
from ui.sandbox.sandbox_detail_panel import SandboxDetailPanel
from core.storage_manager import StorageManager
from core.theme_manager import ThemeManager
from models.object_model import ObjectCategory, ObjectType
from tools.docker_integration import DockerAutomationManager

class SandboxMainWindow(QMainWindow):
    def __init__(self, project_type=None, category=None, template_data=None):
        super().__init__()
        self.sandbox_manager = SandboxManager()
        self.storage_manager = StorageManager()
        self.current_theme = 'cyber_modern'
        self.object_widgets = {}
        
        self.project_type = project_type
        self.category = category
        self.template_data = template_data
        
        self.setup_ui()
        self.apply_theme(self.current_theme)
        self.setup_connections()

        self.docker_manager = DockerAutomationManager(self)
        
        self.statusBar().showMessage(f"Ready - {self.get_project_title()}")
        self.sandbox_manager.save_state("Initial state")

    def get_project_title(self):
        if self.project_type and self.category:
            category_name = self.category.replace('_', ' ').title()
            return f"Sandbox - {category_name}"
        return "BeatRooter Sandbox"

    def setup_ui(self):
        self.setWindowTitle("BeatRooter Sandbox")
        self.setGeometry(100, 100, 1400, 900)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Toolbox
        category_enum = self.map_category_to_enum(self.category)
        self.toolbox = SandboxToolbox(self.sandbox_manager, category_enum)
    
        if self.category:
            category_enum = self.map_category_to_enum(self.category)
            self.toolbox.update_category(category_enum)

        splitter.addWidget(self.toolbox)
        
        # Canvas
        self.canvas_widget = SandboxCanvasWidget(self.sandbox_manager)
        splitter.addWidget(self.canvas_widget)
        
        # Detail panel
        self.detail_panel = SandboxDetailPanel(self)
        splitter.addWidget(self.detail_panel)
        
        splitter.setSizes([280, 600, 350])
        main_layout.addWidget(splitter)

        self.create_menu_bar()
        self.create_toolbar()
        self.setStatusBar(QStatusBar())
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        new_action = QAction('New Sandbox', self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_sandbox)
        file_menu.addAction(new_action)
        
        open_action = QAction('Open Sandbox...', self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_sandbox)
        file_menu.addAction(open_action)
        
        save_action = QAction('Save Sandbox', self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_sandbox)
        file_menu.addAction(save_action)
        
        save_as_action = QAction('Save Sandbox As...', self)
        save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        save_as_action.triggered.connect(self.save_sandbox_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()

        self.undo_action = QAction('Undo', self)
        self.undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        self.undo_action.triggered.connect(self.undo)
        self.undo_action.setEnabled(False)
        file_menu.addAction(self.undo_action)
        
        self.redo_action = QAction('Redo', self)
        self.redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        self.redo_action.triggered.connect(self.redo)
        self.redo_action.setEnabled(False)
        file_menu.addAction(self.redo_action)
        
        file_menu.addSeparator()
        
        export_menu = file_menu.addMenu('Export')
        
        export_png_action = QAction('PNG Image', self)
        export_png_action.triggered.connect(self.export_png)
        export_menu.addAction(export_png_action)
        
        export_json_action = QAction('JSON Data', self)
        export_json_action.triggered.connect(self.export_json)
        export_menu.addAction(export_json_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        theme_menu = view_menu.addMenu('Theme')
        
        cyber_theme_action = QAction('Cyber Modern', self)
        cyber_theme_action.triggered.connect(lambda: self.apply_theme('cyber_modern'))
        theme_menu.addAction(cyber_theme_action)
        
        hacker_theme_action = QAction('Hacker Dark', self)
        hacker_theme_action.triggered.connect(lambda: self.apply_theme('hacker_dark'))
        theme_menu.addAction(hacker_theme_action)
        
        # Object menu
        object_menu = menubar.addMenu('Object')
        
        arrange_menu = object_menu.addMenu('Arrange')
        
        group_action = QAction('Group Selected', self)
        group_action.triggered.connect(self.group_selected_objects)
        arrange_menu.addAction(group_action)
        
        ungroup_action = QAction('Ungroup Selected', self)
        ungroup_action.triggered.connect(self.ungroup_selected_objects)
        arrange_menu.addAction(ungroup_action)
        
        object_menu.addSeparator()
        
        align_menu = object_menu.addMenu('Align')
        
        align_left_action = QAction('Align Left', self)
        align_left_action.triggered.connect(lambda: self.align_objects('left'))
        align_menu.addAction(align_left_action)
        
        align_center_action = QAction('Align Center', self)
        align_center_action.triggered.connect(lambda: self.align_objects('center'))
        align_menu.addAction(align_center_action)
        
        align_right_action = QAction('Align Right', self)
        align_right_action.triggered.connect(lambda: self.align_objects('right'))
        align_menu.addAction(align_right_action)
        
        # Docker menu
        docker_menu = menubar.addMenu('Docker')
        
        up_docker_action = QAction('Up Project in Env', self)
        up_docker_action.triggered.connect(self.show_docker_automation)
        docker_menu.addAction(up_docker_action)
    
    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        new_action = QAction('New', self)
        new_action.triggered.connect(self.new_sandbox)
        toolbar.addAction(new_action)
        
        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_sandbox)
        toolbar.addAction(open_action)
        
        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_sandbox)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()

        undo_toolbar_action = QAction('Undo', self)
        undo_toolbar_action.triggered.connect(self.undo)
        undo_toolbar_action.setEnabled(False)
        toolbar.addAction(undo_toolbar_action)
        
        redo_toolbar_action = QAction('Redo', self)
        redo_toolbar_action.triggered.connect(self.redo)
        redo_toolbar_action.setEnabled(False)
        toolbar.addAction(redo_toolbar_action)
        
        toolbar.addSeparator()
        
        zoom_in_action = QAction('Zoom In', self)
        zoom_in_action.triggered.connect(self.zoom_in)
        toolbar.addAction(zoom_in_action)
        
        zoom_out_action = QAction('Zoom Out', self)
        zoom_out_action.triggered.connect(self.zoom_out)
        toolbar.addAction(zoom_out_action)
        
        reset_zoom_action = QAction('Reset Zoom', self)
        reset_zoom_action.triggered.connect(self.reset_zoom)
        toolbar.addAction(reset_zoom_action)

    def show_docker_automation(self):
        sandbox_data = self._get_sandbox_data_for_docker()
        if not sandbox_data or not sandbox_data.get('objects'):
            QMessageBox.warning(self, "Aviso", 
                            "Nenhum sandbox carregado ou vazio.\n\n"
                            "Por favor, carregue um sandbox com uma aplicação web primeiro.")
            return
        
        print(f"Sandbox carregado com {len(sandbox_data.get('objects', []))} objetos")
        
        from tools.docker_automation import DockerAutomationDialog
        dialog = DockerAutomationDialog(sandbox_data, self)
        dialog.exec()

    def _get_sandbox_data_for_docker(self):
        try:
            environment = self.sandbox_manager.environment
            sandbox_data = {
                'metadata': environment.metadata,
                'objects': [obj.to_dict() for obj in environment.objects.values()]
            }
            return sandbox_data
        except:
            return None

    def map_category_to_enum(self, category_str):
        mapping = {
            'operating_systems': ObjectCategory.OPERATING_SYSTEM,
            'network_devices': ObjectCategory.NETWORK,
            'web_technologies': ObjectCategory.WEB,
            'organization': ObjectCategory.ORGANIZATION,
            'network_topology': ObjectCategory.NETWORK,
            'web_architecture': ObjectCategory.WEB,
            'operative_system': ObjectCategory.OPERATING_SYSTEM
        }
        return mapping.get(category_str, None)

    def setup_connections(self):
        self.toolbox.object_created.connect(self.create_object)
        self.canvas_widget.object_created.connect(self.create_object_visual)
        self.canvas_widget.connection_requested.connect(self.create_connection)
        self.canvas_widget.parent_child_requested.connect(self.set_parent_child)
        
        self.detail_panel.object_data_updated.connect(self.on_object_updated)
        self.detail_panel.object_deleted.connect(self.on_object_deleted)

    def create_object(self, obj_type, obj_name=None):
        from PyQt6.QtCore import QPointF
        from models.object_model import ObjectType
        
        view_center = self.canvas_widget.mapToScene(
            self.canvas_widget.viewport().rect().center()
        )

        try:
            if isinstance(obj_type, str):
                obj_type = ObjectType(obj_type)
            
            obj = self.sandbox_manager.add_object(obj_type, view_center, obj_name)
            self.create_object_visual(obj)
            
            self.statusBar().showMessage(f"Created {obj_type.value} object")
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to create object: {e}")

    def create_object_visual(self, obj):
        from ui.sandbox.sandbox_object_widget import SandboxObjectWidget
        
        obj_widget = SandboxObjectWidget(obj)
        self.canvas_widget.add_object_widget(obj_widget)
        
        obj_widget.object_updated.connect(self.on_object_selected)
        obj_widget.connection_started.connect(self.start_connection)
        obj_widget.parent_child_started.connect(self.start_parent_child)
        obj_widget.object_deleted.connect(self.on_object_deleted)
        
        self.object_widgets[obj.id] = obj_widget
        
        self.statusBar().showMessage(f"Created {obj.object_type.value} object visual")

    def on_object_selected(self, obj):
        self.detail_panel.display_object(obj)
        self.statusBar().showMessage(f"Selected {obj.object_type.value} object: {obj.name}")

    def on_object_updated(self, obj):
        if obj.id in self.object_widgets:
            self.object_widgets[obj.id].update_display()
        
        self.sandbox_manager.save_state(f"Update {obj.object_type.value} object")
        self.update_undo_redo_buttons()
        
        self.statusBar().showMessage(f"Updated {obj.object_type.value} object")

    def on_object_deleted(self, obj):
        reply = QMessageBox.question(self, 'Delete Object', 
                                f'Are you sure you want to delete this {obj.object_type.value} object?',
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.canvas_widget.remove_connections_for_object(obj.id)
            
            self.sandbox_manager.remove_object(obj.id)

            if obj.id in self.object_widgets:
                obj_widget = self.object_widgets[obj.id]
                self.canvas_widget.scene.removeItem(obj_widget)
                del self.object_widgets[obj.id]
            
            if self.detail_panel.current_object and self.detail_panel.current_object.id == obj.id:
                self.detail_panel.clear_panel()
            
            self.update_undo_redo_buttons()
            
            self.statusBar().showMessage(f"Deleted {obj.object_type.value} object")

    def _remove_object_connections_visual(self, obj_id: str):
        connections_to_remove = []
        
        for connection_id, connection_item in self.canvas_widget.connection_items.items():
            if obj_id in connection_id:
                connections_to_remove.append(connection_id)
        
        for connection_id in connections_to_remove:
            self.canvas_widget.remove_connection_item(connection_id)

    def clear_all_connections(self):
        for connection_id in list(self.connection_items.keys()):
            self.remove_connection_item(connection_id)

    def start_connection(self, source_widget):
        self.connection_source = source_widget
        self.statusBar().showMessage("Connection mode: Click target object or ESC to cancel")

    def start_parent_child(self, parent_widget):
        self.parent_child_source = parent_widget
        self.statusBar().showMessage("Parent-Child mode: Click child object or ESC to cancel")

    def create_connection(self, source_id, target_id):
        try:
            connection_id = self.sandbox_manager.add_connection(source_id, target_id)
            self.canvas_widget.draw_connection(source_id, target_id, connection_id)
            
            self.update_undo_redo_buttons()
            self.statusBar().showMessage(f"Connected {source_id} to {target_id}")
        except Exception as e:
            self.statusBar().showMessage(f"Connection failed: {e}")

    def set_parent_child(self, parent_id, child_id):
        try:
            self.sandbox_manager.set_parent(child_id, parent_id)
            
            if parent_id in self.object_widgets and child_id in self.object_widgets:
                parent_widget = self.object_widgets[parent_id]
                child_widget = self.object_widgets[child_id]
                self.canvas_widget.update_parent_child_visual(parent_widget, child_widget)
            
            self.update_undo_redo_buttons()
            self.statusBar().showMessage(f"Set {child_id} as child of {parent_id}")
        except Exception as e:
            self.statusBar().showMessage(f"Parent-child relationship failed: {e}")

    def undo(self):
        if self.sandbox_manager.undo():
            self.refresh_canvas_from_environment()
            self.update_undo_redo_buttons()
            self.statusBar().showMessage("Undo: " + self.sandbox_manager.history[self.sandbox_manager.history_position]['description'])
    
    def redo(self):
        if self.sandbox_manager.redo():
            self.refresh_canvas_from_environment()
            self.update_undo_redo_buttons()
            self.statusBar().showMessage("Redo: " + self.sandbox_manager.history[self.sandbox_manager.history_position]['description'])
    
    def update_undo_redo_buttons(self):
        self.undo_action.setEnabled(self.sandbox_manager.can_undo())
        self.redo_action.setEnabled(self.sandbox_manager.can_redo())
        
        for action in self.findChildren(QAction):
            if action.text() == 'Undo':
                action.setEnabled(self.sandbox_manager.can_undo())
            elif action.text() == 'Redo':
                action.setEnabled(self.sandbox_manager.can_redo())

    def refresh_canvas_from_environment(self):
        self.canvas_widget.scene.clear()
        self.object_widgets.clear()
        
        for obj in self.sandbox_manager.environment.objects.values():
            self.create_object_visual(obj)
        
        for obj in self.sandbox_manager.environment.objects.values():
            for connection_id in obj.connections:
                if '_' in connection_id:
                    source_id, target_id = connection_id.replace('conn_', '').split('_', 1)
                    self.canvas_widget.draw_connection(source_id, target_id, connection_id)
        
        if (self.detail_panel.current_object and 
            self.detail_panel.current_object.id not in self.sandbox_manager.environment.objects):
            self.detail_panel.clear_panel()

    def new_sandbox(self):
        if self.has_unsaved_changes():
            reply = QMessageBox.question(self, 'New Sandbox', 
                                    'You have unsaved changes. Are you sure you want to start a new sandbox?',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.No:
                return
        
        from ui.sandbox.sandbox_category_dialog import SandboxCategoryDialog
        category_dialog = SandboxCategoryDialog(self)
        
        if category_dialog.exec() == QDialog.DialogCode.Accepted:
            selected_category = category_dialog.selected_category
            
            self.sandbox_manager.clear_environment()
            self.canvas_widget.scene.clear()
            self.object_widgets.clear()
            self.detail_panel.clear_panel()

            if selected_category != 'all_categories':
                category_enum = self.map_category_to_enum(selected_category)
                self.toolbox.update_category(category_enum)
            else:
                self.toolbox.update_category(None)
            
            self.statusBar().showMessage(f"New {selected_category.replace('_', ' ')} sandbox created")

    def start_connection(self, source_widget):
        self.canvas_widget.start_connection(source_widget)

    def start_parent_child(self, parent_widget):
        self.canvas_widget.start_parent_child(parent_widget)

    def create_connection(self, source_id, target_id):
        try:
            connection_id = self.sandbox_manager.add_connection(source_id, target_id)
            self.canvas_widget.draw_connection(source_id, target_id, connection_id)
            
            self.update_undo_redo_buttons()
            self.statusBar().showMessage(f"Connected {source_id} to {target_id}")
        except Exception as e:
            self.statusBar().showMessage(f"Connection failed: {e}")

    def set_parent_child(self, parent_id, child_id):
        try:
            self.sandbox_manager.set_parent(child_id, parent_id)
            
            if parent_id in self.object_widgets and child_id in self.object_widgets:
                parent_widget = self.object_widgets[parent_id]
                child_widget = self.object_widgets[child_id]
                self.canvas_widget.update_parent_child_visual(parent_widget, child_widget)
            
            self.update_undo_redo_buttons()
            self.statusBar().showMessage(f"Set {child_id} as child of {parent_id}")
        except Exception as e:
            self.statusBar().showMessage(f"Parent-child relationship failed: {e}")

    def has_unsaved_changes(self):
        return len(self.sandbox_manager.environment.objects) > 0

    def save_sandbox(self):
        if self.storage_manager.current_file:
            success = self.save_environment_to_file(self.storage_manager.current_file)
            if success:
                self.statusBar().showMessage("Sandbox saved")
            else:
                self.statusBar().showMessage("Save failed")
        else:
            self.save_sandbox_as()

    def save_sandbox_as(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, 'Save Sandbox', '', 
            'BeatRooter Sandbox Files (*.brs);;JSON Files (*.json);;All Files (*)'
        )
        
        if filename:
            if not filename.endswith('.brs') and not filename.endswith('.json'):
                filename += '.brs'
            
            success = self.save_environment_to_file(filename)
            if success:
                self.storage_manager.current_file = filename
                self.statusBar().showMessage(f"Sandbox saved as: {filename}")
            else:
                self.statusBar().showMessage("Save failed")

    def save_environment_to_file(self, filename):
        try:
            import json
            from datetime import datetime
            
            self.sandbox_manager.environment.metadata['modified'] = datetime.now().isoformat()
            if not self.sandbox_manager.environment.metadata.get('created'):
                self.sandbox_manager.environment.metadata['created'] = datetime.now().isoformat()
            
            data = self.sandbox_manager.environment.to_dict()
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save sandbox: {e}")
            return False

    def open_sandbox(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, 'Open Sandbox', '', 
            'BeatRooter Sandbox Files (*.brs);;JSON Files (*.json);;All Files (*)'
        )
        
        if filename:
            try:
                self.load_environment_from_file(filename)
                self.statusBar().showMessage(f"Opened sandbox: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open file: {e}")

    def load_environment_from_file(self, filename):
        try:
            import json
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            from models.object_model import SandboxEnvironment
            environment = SandboxEnvironment.from_dict(data)
            
            self.sandbox_manager.environment = environment
            self.storage_manager.current_file = filename
            
            self.refresh_canvas_from_environment()
            
        except Exception as e:
            raise Exception(f"Failed to load environment: {e}")

    def export_png(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, 'Export as PNG', '', 'PNG Images (*.png)'
        )
        
        if filename:
            success = self.storage_manager.export_png(
                None,
                filename,
                self.canvas_widget.scene
            )
            if success:
                self.statusBar().showMessage(f"Exported PNG: {filename}")
            else:
                self.statusBar().showMessage("PNG export failed")

    def export_json(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, 'Export as JSON', '', 'JSON Files (*.json)'
        )
        
        if filename:
            success = self.save_environment_to_file(filename)
            if success:
                self.statusBar().showMessage(f"Exported JSON: {filename}")
            else:
                self.statusBar().showMessage("JSON export failed")

    def apply_theme(self, theme_name):
        self.current_theme = theme_name
        style_sheet = ThemeManager.get_theme(theme_name)
        self.setStyleSheet(style_sheet)
        self.statusBar().showMessage(f"Applied {theme_name} theme")

    def zoom_in(self):
        self.canvas_widget.scale(1.2, 1.2)
    
    def zoom_out(self):
        self.canvas_widget.scale(0.8, 0.8)
    
    def reset_zoom(self):
        self.canvas_widget.resetTransform()

    def group_selected_objects(self):
        selected_objects = [item for item in self.canvas_widget.scene.selectedItems() 
                          if hasattr(item, 'object')]
        
        if len(selected_objects) < 2:
            QMessageBox.information(self, "Group Objects", "Please select at least 2 objects to group")
            return
        
        self.statusBar().showMessage(f"Grouped {len(selected_objects)} objects")

    def ungroup_selected_objects(self):
        selected_objects = [item for item in self.canvas_widget.scene.selectedItems() 
                          if hasattr(item, 'object')]
        
        if not selected_objects:
            QMessageBox.information(self, "Ungroup Objects", "Please select a group to ungroup")
            return
        
        self.statusBar().showMessage("Ungrouped objects")

    def align_objects(self, alignment):
        selected_objects = [item for item in self.canvas_widget.scene.selectedItems() 
                          if hasattr(item, 'object')]
        
        if len(selected_objects) < 2:
            QMessageBox.information(self, "Align Objects", "Please select at least 2 objects to align")
            return
        
        self.statusBar().showMessage(f"Aligned objects to {alignment}")

    def closeEvent(self, event):
        if self.has_unsaved_changes():
            reply = QMessageBox.question(self, 'Unsaved Changes', 
                                      'You have unsaved changes. Are you sure you want to quit?',
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return
        
        event.accept()