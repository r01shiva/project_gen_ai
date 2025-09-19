import ollama
import random

def story_generator():
    print("📚 Interactive Story Generator")
    
    # Story elements
    genres = ["mystery", "adventure", "sci-fi", "fantasy", "comedy"]
    characters = ["detective", "wizard", "robot", "pirate", "scientist"]
    settings = ["haunted castle", "space station", "underwater city", "forest", "mountain"]
    
    while True:
        print("\n🎲 Generating random story elements...")
        
        genre = random.choice(genres)
        character = random.choice(characters)
        setting = random.choice(settings)
        
        print(f"Genre: {genre}")
        print(f"Main Character: {character}")
        print(f"Setting: {setting}")
        
        # Let user add custom element
        custom_element = input("Add a custom element (or press Enter to skip): ")
        
        # Build story prompt
        prompt = f"""
        Write a short story (200-300 words) with these elements:
        - Genre: {genre}
        - Main character: {character}
        - Setting: {setting}
        """
        
        if custom_element:
            prompt += f"- Special element: {custom_element}"
        
        prompt += "\n\nMake it engaging and complete with a beginning, middle, and end."
        
        try:
            print("\n✍️ Generating your story...\n")
            
            response = ollama.generate(
                model='tinyllama',
                prompt=prompt,
                options={
                    'temperature': 0.8,  # More creative
                    # 'max_tokens': 300 # it is for open ai not for ollama
                    'num_predict': 30 
                }
            )
            
            print("📖 Your Story:")
            print("-" * 40)
            print(response['response'])
            print("-" * 40)
            
        except Exception as e:
            print(f"Error: {e}")
        
        again = input("\n🔄 Generate another story? (y/n): ")
        if again.lower() != 'y':
            break

if __name__ == "__main__":
    story_generator()
