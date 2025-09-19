import requests
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
            # stream=True because Ollama sends multiple JSON objects
            with requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "tinyllama", "prompt": user_input},
                stream=True
            ) as r:
                response_text = ""
                for line in r.iter_lines():
                    if line:
                        data = json.loads(line.decode("utf-8"))
                        if "response" in data:
                            print(data["response"], end="", flush=True)
                            response_text += data["response"]
                        if data.get("done", False):
                            break
                print("\n")  # new line after full response

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    ai_assistant()
