from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont

class SidebarWidget(QWidget):
    mode_changed = Signal(str)
    
    def __init__(self):
        super().__init__()
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("AI Assistant")
        title.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setPointSize(14)
        title.setFont(font)
        layout.addWidget(title)
        
        # Mode buttons
        self.mode_buttons = []
        modes = [
            ("💬", "Normal Chat", "chat"),
            ("🔍", "RAG Search", "rag"),
            ("⚡", "Actions", "actions")
        ]
        
        for icon, text, mode in modes:
            btn = QPushButton(f"{icon} {text}")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, m=mode: self._on_mode_clicked(m))
            self.mode_buttons.append((btn, mode))
            layout.addWidget(btn)
        
        # Set default mode
        self.mode_buttons[0][0].setChecked(True)
        
        layout.addStretch()
    
    def _on_mode_clicked(self, mode):
        # Update button states
        for btn, btn_mode in self.mode_buttons:
            btn.setChecked(btn_mode == mode)
        
        self.mode_changed.emit(mode)
