from PyQt6.QtWidgets import QDockWidget
from PyQt6.QtCore import Qt
from tools.tools_manager import ToolsManager

class ToolsIntegration:
    def __init__(self, main_window):
        self.main_window = main_window
        self.tools_manager = None
        self.tools_dock = None

    def setup_tools_integration(self):
        self.tools_manager = ToolsManager(self.main_window)
        
        self.tools_dock = QDockWidget("External Tools", self.main_window)
        self.tools_dock.setWidget(self.tools_manager)

        self.tools_dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea | 
            Qt.DockWidgetArea.RightDockWidgetArea
        )

        self.main_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.tools_dock)
        
        #self.add_tools_menu()

    def add_tools_menu(self):
        menubar = self.main_window.menuBar()
        
        tools_menu = menubar.addMenu('Tools')
        
        toggle_action = tools_menu.addAction('Show/Hide Tools Panel')
        toggle_action.triggered.connect(self.toggle_tools_panel)
        
        tools_menu.addSeparator()
        
        exif_action = tools_menu.addAction('ExifTool')
        exif_action.triggered.connect(lambda: self.quick_launch_tool('exiftool'))
        
        nmap_action = tools_menu.addAction('Nmap')
        nmap_action.triggered.connect(lambda: self.quick_launch_tool('nmap'))
        
        whois_action = tools_menu.addAction('Whois')
        whois_action.triggered.connect(lambda: self.quick_launch_tool('whois'))

    def toggle_tools_panel(self):
        if self.tools_dock.isVisible():
            self.tools_dock.hide()
        else:
            self.tools_dock.show()

    def quick_launch_tool(self, tool_name):
        if self.tools_dock.isHidden():
            self.tools_dock.show()
        
        self.tools_manager.select_tool(tool_name)