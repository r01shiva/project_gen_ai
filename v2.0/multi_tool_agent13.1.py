import ollama
import datetime
import random
import json
import re

class WorkingAIAgent:
    def __init__(self):
        print("🤖 Starting AI Agent...")
        self.conversation_history = []
        
    def get_current_time(self):
        """Get current time"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def simple_calculator(self, expression):
        """Safe calculator for basic math"""
        try:
            # Remove any non-math characters for safety
            allowed_chars = "0123456789+-*/.() "
            cleaned = ''.join(c for c in expression if c in allowed_chars)
            
            if cleaned:
                result = eval(cleaned)  # Safe since we filtered input
                return f"Result: {result}"
            else:
                return "Error: Invalid math expression"
        except:
            return "Error: Cannot calculate that"
    
    def get_weather(self):
        """Simulate weather data"""
        conditions = ["sunny", "cloudy", "rainy", "partly cloudy", "windy"]
        temp = random.randint(15, 35)
        condition = random.choice(conditions)
        return f"Current weather: {condition}, {temp}°C"
    
    def store_note(self, note):
        """Store a simple note"""
        timestamp = self.get_current_time()
        note_entry = f"[{timestamp}] {note}"
        
        # Store in a simple file
        try:
            with open("agent_notes.txt", "a", encoding="utf-8") as f:
                f.write(note_entry + "\n")
            return f"✅ Note saved: {note}"
        except:
            return "❌ Could not save note"
    
    def read_notes(self):
        """Read stored notes"""
        try:
            with open("agent_notes.txt", "r", encoding="utf-8") as f:
                notes = f.read().strip()
                if notes:
                    return f"📝 Your notes:\n{notes}"
                else:
                    return "📝 No notes found"
        except:
            return "📝 No notes file found"
    
    def decide_and_execute_tools(self, user_input):
        """Simple rule-based tool selection"""
        user_lower = user_input.lower()
        results = []
        
        # Time-related requests
        if any(word in user_lower for word in ["time", "date", "when", "now"]):
            time_result = self.get_current_time()
            results.append(f"🕐 Current time: {time_result}")
        
        # Math requests  
        if any(word in user_lower for word in ["calculate", "math", "+", "-", "*", "/", "="]):
            # Extract math expression
            math_pattern = r'[\d\+\-\*\/\.\(\)\s]+'
            matches = re.findall(math_pattern, user_input)
            if matches:
                for match in matches:
                    if any(op in match for op in ["+", "-", "*", "/"]):
                        calc_result = self.simple_calculator(match.strip())
                        results.append(f"🔢 {calc_result}")
        
        # Weather requests
        if any(word in user_lower for word in ["weather", "temperature", "climate"]):
            weather_result = self.get_weather()
            results.append(f"🌤️ {weather_result}")
        
        # Note-taking requests
        if "save note" in user_lower or "add note" in user_lower:
            # Extract note content after "save note" or "add note"
            note_patterns = [r"save note[:\s]+(.+)", r"add note[:\s]+(.+)"]
            note_text = ""
            for pattern in note_patterns:
                match = re.search(pattern, user_lower)
                if match:
                    note_text = match.group(1).strip()
                    break
            
            if note_text:
                save_result = self.store_note(note_text)
                results.append(save_result)
            else:
                results.append("❓ What note would you like to save?")
        
        # Read notes requests
        if any(phrase in user_lower for phrase in ["show notes", "read notes", "my notes", "list notes"]):
            notes_result = self.read_notes()
            results.append(notes_result)
        
        return results
    
    def chat_with_ollama(self, user_input, tool_results=None):
        """Get response from TinyLlama"""
        try:
            # Prepare the prompt with tool results if available
            if tool_results:
                context = f"""
User asked: {user_input}

I used tools and got these results:
{chr(10).join(tool_results)}

Based on the user's question and these tool results, provide a helpful response.
"""
            else:
                context = user_input
            
            response = ollama.generate(
                model='tinyllama',
                prompt=context,
                options={
                    'temperature': 0.7,
                    'max_tokens': 300
                }
            )
            
            return response['response']
            
        except Exception as e:
            return f"❌ AI Error: {e}"
    
    def run(self):
        """Main agent loop"""
        print("\n🤖 Multi-Tool AI Agent Ready!")
        print("\nI can help you with:")
        print("• ⏰ Time and date ('What time is it?')")
        print("• 🔢 Math calculations ('Calculate 25 * 4 + 10')")
        print("• 🌤️ Weather info ('What's the weather?')")
        print("• 📝 Notes ('Save note: Buy groceries', 'Show my notes')")
        print("• 💬 General conversation")
        print("\nType 'quit' to exit\n")
        
        while True:
            user_input = input("💬 You: ")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("🤖 Agent: Goodbye! 👋")
                break
            
            print("🤖 Agent: Let me help you with that...")
            
            # Step 1: Check if tools are needed and execute them
            tool_results = self.decide_and_execute_tools(user_input)
            
            # Step 2: Get AI response, incorporating tool results if any
            if tool_results:
                print("\n🛠️ Tool Results:")
                for result in tool_results:
                    print(f"   {result}")
                
                ai_response = self.chat_with_ollama(user_input, tool_results)
                print(f"\n🤖 Agent: {ai_response}")
            else:
                # No tools needed, just normal conversation
                ai_response = self.chat_with_ollama(user_input)
                print(f"🤖 Agent: {ai_response}")
            
            print("-" * 50)

if __name__ == "__main__":
    agent = WorkingAIAgent()
    agent.run()
