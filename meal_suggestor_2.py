import ollama
import random

def food_recommender():
    print("🍽️ Smart Food Recommender")
    
    while True:
        # Simulate weather data
        temperature = random.randint(15, 40)  # Celsius
        humidity = random.randint(30, 90)     # Percentage
        
        print(f"\n🌡️ Temperature: {temperature}°C")
        print(f"💧 Humidity: {humidity}%")
        
        # Create context-aware prompt
        prompt = f"""
        Weather conditions:
        - Temperature: {temperature}°C
        - Humidity: {humidity}%
        
        Suggest 3 appropriate food items for this weather. 
        Give brief reasons why each food is suitable.
        """
        
        try:
            response = ollama.generate(
                model='tinyllama',
                prompt=prompt
            )
            print(f"\n🍴 Food Suggestions:\n{response['response']}")
            
        except Exception as e:
            print(f"Error: {e}")
        
        # Ask if user wants another suggestion
        again = input("\n🔄 Get another suggestion? (y/n): ")
        if again.lower() != 'y':
            break

if __name__ == "__main__":
    food_recommender()
