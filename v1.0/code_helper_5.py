import ollama

def code_helper():
    print("💻 AI Code Helper")
    print("Ask for help with Python code, algorithms, or debugging!")
    print("Type 'quit' to exit\n")
    
    while True:
        user_question = input("Your coding question: ")
        
        if user_question.lower() in ['quit', 'exit']:
            break
            
        # Enhanced prompt for better code responses
        prompt = f"""
        As a Python programming assistant, help with this question:
        {user_question}
        
        Please provide:
        1. A clear explanation
        2. Working code example (if applicable)
        3. Any important notes or best practices
        """
        
        try:
            response = ollama.generate(
                model='tinyllama',
                prompt=prompt,
                options={
                    'temperature': 0.3,  # Less creative, more factual
                    'num_ctx': 2048      # Context window
                }
            )
            
            print(f"\n🤖 AI Helper:\n{response['response']}\n")
            print("-" * 50)
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    code_helper()
