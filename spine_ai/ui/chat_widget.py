from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QPushButton, QScrollArea, QProgressBar, QLabel
)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QTextCursor, QFont

class ChatWidget(QWidget):
    message_sent = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.current_mode = "chat"
        self.thinking_timer = QTimer()
        self.thinking_dots = 0
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setMinimumHeight(400)
        
        # Progress indicator (hidden by default)
        self.progress_widget = QWidget()
        progress_layout = QHBoxLayout(self.progress_widget)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate progress
        self.progress_bar.hide()
        
        self.thinking_label = QLabel("🤖 AI is thinking...")
        self.thinking_label.hide()
        
        progress_layout.addWidget(self.thinking_label)
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addStretch()
        
        # Input area
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        
        # Text input
        self.message_input = QTextEdit()
        self.message_input.setMaximumHeight(100)
        self.message_input.setPlaceholderText("Type your message here...")
        
        # Send button
        send_layout = QHBoxLayout()
        self.send_button = QPushButton("Send ⬆️")
        self.send_button.setMaximumWidth(100)
        self.send_button.clicked.connect(self._send_message)
        
        send_layout.addStretch()
        send_layout.addWidget(self.send_button)
        
        input_layout.addWidget(self.message_input)
        input_layout.addLayout(send_layout)
        
        # Add all widgets to main layout
        layout.addWidget(self.chat_display, 3)
        layout.addWidget(self.progress_widget)
        layout.addWidget(input_widget, 1)
        
        # Connect enter key
        self.message_input.installEventFilter(self)
        
        # Setup thinking animation
        self.thinking_timer.timeout.connect(self._animate_thinking)
    
    def eventFilter(self, obj, event):
        if obj == self.message_input and event.type() == event.Type.KeyPress:
            if event.key() == Qt.Key_Return and not event.modifiers() & Qt.ShiftModifier:
                self._send_message()
                return True
        return super().eventFilter(obj, event)
    
    def _send_message(self):
        message = self.message_input.toPlainText().strip()
        if message and self.send_button.isEnabled():
            self.add_user_message(message)
            self.message_input.clear()
            
            # Disable send button while processing
            self.send_button.setEnabled(False)
            
            self.message_sent.emit(message)
    
    def show_ai_thinking(self):
        """Show progress indicator and disable input"""
        self.thinking_label.show()
        self.progress_bar.show()
        self.thinking_dots = 0
        self.thinking_timer.start(500)  # Update every 500ms
        
        # Keep send button disabled
        self.send_button.setEnabled(False)
    
    def hide_ai_thinking(self):
        """Hide progress indicator and re-enable input"""
        self.thinking_label.hide()
        self.progress_bar.hide()
        self.thinking_timer.stop()
        
        # Re-enable send button
        self.send_button.setEnabled(True)
    
    def _animate_thinking(self):
        """Animate the thinking indicator"""
        dots = "." * (self.thinking_dots % 4)
        self.thinking_label.setText(f"🤖 AI is thinking{dots}")
        self.thinking_dots += 1
    
    def add_user_message(self, message):
        self.chat_display.append(f"<div style='margin: 10px 0;'><b>You:</b> {message}</div>")
        self._scroll_to_bottom()
    
    def add_ai_message(self, message):
        mode_prefix = {
            "chat": "🤖 AI",
            "rag": "📚 RAG",
            "actions": "⚡ Actions"
        }
        prefix = mode_prefix.get(self.current_mode, "🤖 AI")
        
        self.chat_display.append(f"<div style='margin: 10px 0; background-color: #f0f0f0; padding: 10px; border-radius: 5px;'><b>{prefix}:</b> {message}</div>")
        self._scroll_to_bottom()
    
    def add_system_message(self, message):
        self.chat_display.append(f"<div style='margin: 5px 0; color: #666; font-style: italic;'>System: {message}</div>")
        self._scroll_to_bottom()
    
    def set_mode(self, mode):
        self.current_mode = mode
        mode_names = {"chat": "Normal Chat", "rag": "RAG Search", "actions": "Actions"}
        self.add_system_message(f"Switched to {mode_names.get(mode, mode)} mode")
    
    def search_messages(self, query):
        # Simple search implementation
        content = self.chat_display.toPlainText()
        if query.lower() in content.lower():
            self.add_system_message(f"Found '{query}' in chat history")
        else:
            self.add_system_message(f"'{query}' not found in chat history")
    
    def _scroll_to_bottom(self):
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.chat_display.setTextCursor(cursor)
