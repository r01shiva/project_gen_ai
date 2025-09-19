import ollama

def ai_assistant():
    print("🤖 Your Personal AI Assistant (TinyLlama)")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Assistant: Goodbye! 👋")
            break
            
        try:
            response = ollama.generate(
                model='tinyllama',
                prompt=user_input
            )
            print(f"Assistant: {response['response']}\n")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    ai_assistant()