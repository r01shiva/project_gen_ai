from PySide6.QtCore import QObject

class ThemeManager(QObject):
    def __init__(self):
        super().__init__()
        self.is_dark_theme = True
    
    def apply_dark_theme(self, widget):
        self.is_dark_theme = True
        dark_stylesheet = """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        QPushButton {
            background-color: #404040;
            border: 1px solid #555555;
            padding: 5px;
            border-radius: 3px;
            color: #ffffff;
        }
        QPushButton:hover {
            background-color: #505050;
        }
        QPushButton:checked {
            background-color: #0078d4;
        }
        QTextEdit {
            background-color: #1e1e1e;
            border: 1px solid #555555;
            color: #ffffff;
        }
        QLineEdit {
            background-color: #1e1e1e;
            border: 1px solid #555555;
            padding: 5px;
            color: #ffffff;
        }
        QComboBox {
            background-color: #404040;
            border: 1px solid #555555;
            padding: 5px;
            color: #ffffff;
        }
        QLabel {
            color: #ffffff;
        }
        """
        widget.setStyleSheet(dark_stylesheet)
    
    def apply_light_theme(self, widget):
        self.is_dark_theme = False
        light_stylesheet = """
        QMainWindow {
            background-color: #ffffff;
            color: #000000;
        }
        QWidget {
            background-color: #ffffff;
            color: #000000;
        }
        QPushButton {
            background-color: #f0f0f0;
            border: 1px solid #cccccc;
            padding: 5px;
            border-radius: 3px;
            color: #000000;
        }
        QPushButton:hover {
            background-color: #e0e0e0;
        }
        QPushButton:checked {
            background-color: #0078d4;
            color: #ffffff;
        }
        QTextEdit {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            color: #000000;
        }
        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            padding: 5px;
            color: #000000;
        }
        QComboBox {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            padding: 5px;
            color: #000000;
        }
        QLabel {
            color: #000000;
        }
        """
        widget.setStyleSheet(light_stylesheet)
