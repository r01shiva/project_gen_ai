import ollama

def study_buddy():
    print("📚 AI Study Buddy")
    print("I can explain concepts, create quizzes, and help you learn!")
    print("Type 'quit' to exit\n")
    
    subjects = {
        '1': 'Mathematics',
        '2': 'Programming',
        '3': 'Science', 
        '4': 'History',
        '5': 'Other'
    }
    
    while True:
        print("\nWhat would you like to study?")
        for key, subject in subjects.items():
            print(f"{key}. {subject}")
        
        choice = input("\nChoose (1-5): ")
        
        if choice in subjects:
            subject = subjects[choice]
            
            if subject == 'Other':
                subject = input("What subject? ")
            
            print(f"\n📖 Great! Let's study {subject}")
            print("Options:")
            print("1. Explain a concept")
            print("2. Create practice questions")
            print("3. Summarize a topic")
            
            option = input("Choose (1-3): ")
            
            if option == '1':
                concept = input(f"What {subject} concept do you want explained? ")
                prompt = f"Explain {concept} in {subject} in simple terms with examples. Make it easy to understand for a beginner."
                
            elif option == '2':
                topic = input(f"What {subject} topic for practice questions? ")
                prompt = f"Create 3 practice questions about {topic} in {subject}. Include the answers at the end."
                
            elif option == '3':
                topic = input(f"What {subject} topic to summarize? ")
                prompt = f"Provide a clear, structured summary of {topic} in {subject}. Include key points and important details."
            
            else:
                print("Invalid option!")
                continue
            
            try:
                print(f"\n🤖 Processing...\n")
                
                response = ollama.generate(
                    model='tinyllama',
                    prompt=prompt,
                    options={'temperature': 0.4}  # Balanced creativity/accuracy
                )
                
                print("📝 Study Material:")
                print("=" * 50)
                print(response['response'])
                print("=" * 50)
                
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice.lower() == 'quit':
            break
        else:
            print("Invalid choice!")
        
        continue_study = input("\n📚 Continue studying? (y/n): ")
        if continue_study.lower() != 'y':
            break

if __name__ == "__main__":
    study_buddy()

