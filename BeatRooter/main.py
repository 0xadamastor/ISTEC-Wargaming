import sys
import os
import json
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

from ui.main_window import DigitalDetectiveBoard

def main():
    app = QApplication(sys.argv)

    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = DigitalDetectiveBoard()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()