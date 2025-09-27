import os
from PySide6.QtWidgets import QFileDialog, QApplication
from PySide6.QtCore import QTimer
from .rag_controller import RAGController
from .actions_controller import ActionsController
from .ai_worker import AIWorker
from adapter.ai_model import AIModel

class AppController:
    def __init__(self):
        self.current_model = "tinyllama"
        
        # Initialize AI Model
        self.ai_model = AIModel(self.current_model)
        
        self.rag_controller = RAGController()
        self.actions_controller = ActionsController()
        
        # Keep track of active worker
        self.current_worker = None
        
    def change_model(self, model_name):
        self.current_model = model_name
        
        # Update AI Model
        self.ai_model.change_model(model_name)
        
        # Update RAG controller
        self.rag_controller.set_model(model_name)
        
        print(f"Model changed to: {model_name}")
    
    def handle_chat_message(self, message):
        window = QApplication.instance().activeWindow()
        
        # Show loading indicator immediately
        window.chat_widget.show_ai_thinking()
        
        # Create and start worker thread
        prompt = f"You are a helpful AI assistant. Respond naturally to: {message}"
        self.current_worker = AIWorker(self.ai_model, prompt, "chat")
        
        # Connect signals
        self.current_worker.response_ready.connect(self._on_chat_response_ready)
        self.current_worker.error_occurred.connect(self._on_ai_error)
        
        # Start background processing
        self.current_worker.start()
    
    def handle_rag_message(self, message):
        # For now, keep RAG synchronous - you can make it async later
        response = self.rag_controller.process_query(message)
        window = QApplication.instance().activeWindow()
        window.chat_widget.add_ai_message(response)
    
    def handle_action_message(self, message):
        # Actions are usually quick, keep synchronous
        response = self.actions_controller.process_command(message)
        window = QApplication.instance().activeWindow()
        window.chat_widget.add_ai_message(response)
    
    def _on_chat_response_ready(self, response):
        """Called when AI response is ready"""
        window = QApplication.instance().activeWindow()
        window.chat_widget.hide_ai_thinking()
        window.chat_widget.add_ai_message(response)
        
        # Clean up worker
        if self.current_worker:
            self.current_worker.deleteLater()
            self.current_worker = None
    
    def _on_ai_error(self, error_message):
        """Called when AI encounters an error"""
        window = QApplication.instance().activeWindow()
        window.chat_widget.hide_ai_thinking()
        window.chat_widget.add_ai_message(f"Error: {error_message}")
        
        # Clean up worker
        if self.current_worker:
            self.current_worker.deleteLater()
            self.current_worker = None
    
    def upload_document(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Upload Document", "", "Text Files (*.txt *.md *.pdf)"
        )
        if file_path:
            self.rag_controller.add_document(file_path)
            window = QApplication.instance().activeWindow()
            window.chat_widget.add_system_message(f"Document uploaded: {os.path.basename(file_path)}")
    
    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Upload Image", "", "Image Files (*.png *.jpg *.jpeg *.gif)"
        )
        if file_path:
            window = QApplication.instance().activeWindow()
            window.chat_widget.add_system_message(f"Image uploaded: {os.path.basename(file_path)}")
    
    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Upload File", "", "All Files (*)"
        )
        if file_path:
            window = QApplication.instance().activeWindow()
            window.chat_widget.add_system_message(f"File uploaded: {os.path.basename(file_path)}")
