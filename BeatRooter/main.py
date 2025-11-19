import sys
from PyQt6.QtWidgets import QApplication
from ui.welcome_window import WelcomeWindow
from ui.main_window import DigitalDetectiveBoard

def main():
    app = QApplication(sys.argv)
    
    welcome = WelcomeWindow()
    main_window = None
    
    def on_project_selected(project_type, category, template_json):
        nonlocal main_window
        main_window = DigitalDetectiveBoard(project_type, category, template_json)
        main_window.show()
    
    welcome.project_selected.connect(on_project_selected)
    welcome.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
