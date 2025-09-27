import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from ui.main_window import MainWindow
from controller.app_controller import AppController

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Spine AI")
    app.setOrganizationName("AI Tools")
    
    # Set application style
    app.setStyle('Fusion')
    
    controller = AppController()
    window = MainWindow(controller)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
