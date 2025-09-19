import ollama

def chain_of_thought_solver():
    print("🧠 Chain-of-Thought Problem Solver")
    
    problem = input("Enter a complex problem: ")
    
    cot_prompt = f"""
    Solve this problem step-by-step using chain-of-thought reasoning:
    
    Problem: {problem}
    
    Stop after giving the final answer.
    Format:
    1. Understanding
    2. Step 1
    3. Step 2
    4. Therefore, the answer is: ...
    
    Think through each step carefully and show your reasoning.
    """
    #  Please follow this format:
    # 1. First, let me understand what the problem is asking...
    # 2. Then, I'll break it down into smaller steps...
    # 3. Step 1: [reasoning]
    # 4. Step 2: [reasoning]
    # 5. Therefore, the answer is...
    
    response = ollama.generate(model='tinyllama', prompt=cot_prompt,
    options={
        "temperature": 0.7,
        "max_tokens": 150
        # "stop": ["Therefore, the answer is:"]
    }
                               )
    print(f"\n🔍 Chain-of-Thought Solution:\n{response['response']}")



# if __name__ == "__main__":
#     chain_of_thought_solver()
    
def self_improving_writer():
    print("📝 Self-Improving Content Generator")
    
    topic = input("What topic should I write about? ")
    
    # Step 1: Initial draft
    initial_prompt = f"Write a short article about {topic} (200-300 words)."
    
    draft = ollama.generate(model='tinyllama', prompt=initial_prompt)
    print(f"\n📄 Initial Draft:\n{draft['response']}\n")
    
    # Step 2: Self-critique
    critique_prompt = f"""
    Analyze this article about {topic} and identify 3 specific areas for improvement:
    
    Article: {draft['response']}
    
    Please critique in this format:
    1. Weakness 1: [specific issue]
    2. Weakness 2: [specific issue] 
    3. Weakness 3: [specific issue]
    
    Be specific and constructive in your feedback.
    """
    
    critique = ollama.generate(model='tinyllama', prompt=critique_prompt)
    print(f"🔍 Self-Critique:\n{critique['response']}\n")
    
    # Step 3: Improved version
    improve_prompt = f"""
    Rewrite this article about {topic}, addressing these specific critiques:
    
    Original Article: {draft['response']}
    
    Critiques to Address: {critique['response']}
    
    Create an improved version that fixes these issues while maintaining the core message.
    """
    
    improved = ollama.generate(model='tinyllama', prompt=improve_prompt)
    print(f"✨ Improved Article:\n{improved['response']}")

if __name__ == "__main__":
    self_improving_writer()

