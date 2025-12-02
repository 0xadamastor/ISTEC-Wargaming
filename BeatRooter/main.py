# main.py - ATUALIZADO
import sys
import os
from PyQt6.QtWidgets import QApplication, QMessageBox
from ui.welcome_window import WelcomeWindow
from ui.main_window import DigitalDetectiveBoard
from ui.sandbox.sandbox_main_window import SandboxMainWindow
from ui.file_icon_manager import FileIconManager

def main():
    # Registrar ícones
    icon_manager = FileIconManager()
    if icon_manager.is_admin():
        success = icon_manager.register_file_associations()
        if success:
            print("Ícones registrados com sucesso!")
        else:
            print("Aviso: Não foi possível registrar os ícones automaticamente.")
    else:
        print("Aviso: Execute como administrador para registrar ícones de arquivo.")
    
    app = QApplication(sys.argv)
    
    welcome = WelcomeWindow()
    main_window = None
    
    def on_project_selected(project_type, category, template_json):
        nonlocal main_window
        
        if project_type == 'sandbox':
            main_window = SandboxMainWindow(project_type, category, template_json)
        else:
            main_window = DigitalDetectiveBoard(project_type, category, template_json)
        
        main_window.show()
    
    welcome.project_selected.connect(on_project_selected)
    welcome.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()