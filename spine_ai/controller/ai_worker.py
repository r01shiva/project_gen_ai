from PySide6.QtCore import QThread, Signal

class AIWorker(QThread):
    response_ready = Signal(str)
    error_occurred = Signal(str)
    
    def __init__(self, ai_model, prompt, message_type="chat"):
        super().__init__()
        self.ai_model = ai_model
        self.prompt = prompt
        self.message_type = message_type
    
    def run(self):
        try:
            # Generate AI response in background thread
            response = self.ai_model.generate(
                prompt=self.prompt,
                temperature=0.7,
                max_tokens=200
            )
            self.response_ready.emit(response)
        except Exception as e:
            self.error_occurred.emit(str(e))
