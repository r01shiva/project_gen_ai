import subprocess
import json

def ai_assistant():
    print("🤖 Your Personal AI Assistant (TinyLlama)")
    print("Type 'quit' to exit\n")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Assistant: Goodbye! 👋")
            break

        try:
            result = subprocess.run(
                ["ollama", "run", "tinyllama"],
                input=user_input.encode(),
                capture_output=True
            )
            print(f"Assistant: {result.stdout.decode().strip()}\n")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    ai_assistant()
