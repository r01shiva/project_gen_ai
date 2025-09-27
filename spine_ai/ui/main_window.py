from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, 
    QSplitter, QPushButton, QLineEdit, QComboBox, QLabel
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon

from .sidebar_widget import SidebarWidget
from .chat_widget import ChatWidget
from .theme_manager import ThemeManager
from adapter.ai_model import AIModel

class MainWindow(QMainWindow):
    model_changed = Signal(str)
    
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.theme_manager = ThemeManager()
        self.current_mode = "chat"  # chat, rag, actions
        self.ai_model = AIModel()
        
        self.setWindowTitle("Spine AI")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        self._setup_ui()
        self._connect_signals()
        self._apply_theme()
    
    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left sidebar
        self.sidebar = SidebarWidget()
        self.sidebar.setMaximumWidth(250)
        splitter.addWidget(self.sidebar)
        
        # Right content area
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Top bar with model selector and theme toggle
        top_bar = self._create_top_bar()
        right_layout.addWidget(top_bar)
        
        # Chat area
        self.chat_widget = ChatWidget()
        right_layout.addWidget(self.chat_widget)
        
        # Bottom search bar
        bottom_bar = self._create_bottom_bar()
        right_layout.addWidget(bottom_bar)
        
        splitter.addWidget(right_widget)
        splitter.setSizes([250, 1150])
        
        main_layout.addWidget(splitter)
    
    def _create_top_bar(self):
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_widget.setMaximumHeight(50)
        
        # Model selector
        model_label = QLabel("Model:")
        self.model_combo = QComboBox()
        model_list = self.ai_model.list_models() 
        self.model_combo.addItems(["tinyllama", "gemma3:4b"])
        self.model_combo.setMinimumWidth(150)
        
        # Theme toggle
        self.theme_toggle = QPushButton("🌙")
        self.theme_toggle.setMaximumWidth(40)
        self.theme_toggle.setMaximumHeight(30)
        self.theme_toggle.clicked.connect(self._toggle_theme)
        
        # Upload buttons
        upload_layout = QHBoxLayout()
        upload_buttons = [
            ("📄", "Upload Document", self._upload_document),
            ("🖼️", "Upload Image", self._upload_image),
            ("📁", "Upload File", self._upload_file)
        ]
        
        for icon, tooltip, handler in upload_buttons:
            btn = QPushButton(icon)
            btn.setToolTip(tooltip)
            btn.setMaximumWidth(40)
            btn.setMaximumHeight(30)
            btn.clicked.connect(handler)
            upload_layout.addWidget(btn)
        
        top_layout.addWidget(model_label)
        top_layout.addWidget(self.model_combo)
        top_layout.addStretch()
        top_layout.addLayout(upload_layout)
        top_layout.addWidget(self.theme_toggle)
        
        return top_widget
    
    def _create_bottom_bar(self):
        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout(bottom_widget)
        bottom_widget.setMaximumHeight(40)
        
        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search in chat history...")
        
        search_btn = QPushButton("🔍")
        search_btn.setMaximumWidth(40)
        search_btn.clicked.connect(self._search_chat)
        
        bottom_layout.addWidget(self.search_input)
        bottom_layout.addWidget(search_btn)
        
        return bottom_widget
    
    def _connect_signals(self):
        # Sidebar signals
        self.sidebar.mode_changed.connect(self._on_mode_changed)
        
        # Model change signal
        self.model_combo.currentTextChanged.connect(self._on_model_changed)
        
        # Chat widget signals
        self.chat_widget.message_sent.connect(self._on_message_sent)
    
    def _toggle_theme(self):
        if self.theme_manager.is_dark_theme:
            self.theme_manager.apply_light_theme(self)
            self.theme_toggle.setText("🌙")
        else:
            self.theme_manager.apply_dark_theme(self)
            self.theme_toggle.setText("☀️")
    
    def _apply_theme(self):
        self.theme_manager.apply_dark_theme(self)
        self.theme_toggle.setText("☀️")
    
    def _on_mode_changed(self, mode):
        self.current_mode = mode
        self.chat_widget.set_mode(mode)
        print(f"Mode changed to: {mode}")
    
    def _on_model_changed(self, model):
        self.controller.change_model(model)
        self.chat_widget.add_system_message(f"Model changed to: {model}")
    
    def _on_message_sent(self, message):
        if self.current_mode == "chat":
            self.controller.handle_chat_message(message)
        elif self.current_mode == "rag":
            self.controller.handle_rag_message(message)
        elif self.current_mode == "actions":
            self.controller.handle_action_message(message)
    
    def _upload_document(self):
        self.controller.upload_document()
    
    def _upload_image(self):
        self.controller.upload_image()
    
    def _upload_file(self):
        self.controller.upload_file()
    
    def _search_chat(self):
        query = self.search_input.text().strip()
        if query:
            self.chat_widget.search_messages(query)
