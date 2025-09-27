import ollama

class AIModel:
    def __init__(self, model_name='tinyllama'):
        self.model_name = model_name

    def generate(self, prompt, temperature=0.7, num_ctx=1024, max_tokens=150, stop=None, top_p=0.9):
        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': temperature,
                    'num_ctx': num_ctx,
                    'max_tokens': max_tokens,
                    'stop': stop,
                    'top_p': top_p
                }
            )
            return response['response']
        except Exception as e:
            return f"Error: {e}"
    
    def change_model(self, model_name):
        """Change the current model"""
        self.model_name = model_name
        print(f"AI Model changed to: {model_name}")
    
    def get_current_model(self):
        """Get the current model name"""
        return self.model_name
        
    def list_models(self):
        """List available models correctly"""
        try:
            models_response = ollama.list()
            # Inspect the response structure
            # Example response: {'models': [{'name': 'tinyllama'}, {'name': 'gemma:2b'}]}
            models = models_response.get('models', [])
            # Extract model names
            return [model.get('name', 'Unknown') for model in models]
        except Exception as e:
            return f"Error: {e}"

