import ollama
import datetime
import random
import re
# with gemma3:4b
class FixedAIAgent:
    def __init__(self):
        print("🤖 Fixed AI Agent Starting...")
    
    def get_time(self):
        """Get current time"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def calculate(self, expression):
        """Safe calculator"""
        try:
            allowed = "0123456789+-*/.() "
            cleaned = ''.join(c for c in str(expression) if c in allowed)
            if cleaned and any(op in cleaned for op in "+-*/"):
                result = eval(cleaned)
                return f"{result}"
            return "Invalid math expression"
        except:
            return "Cannot calculate"
    
    def get_weather(self):
        """Get weather"""
        conditions = ["sunny", "cloudy", "rainy", "partly cloudy", "windy"]
        temp = random.randint(15, 35)
        condition = random.choice(conditions)
        return f"{condition}, {temp}°C"
    
    def save_note(self, text):
        """Save note"""
        try:
            timestamp = self.get_time()
            note = f"[{timestamp}] {text}"
            with open("notes.txt", "a", encoding="utf-8") as f:
                f.write(note + "\n")
            return f"Saved: {text}"
        except:
            return "Could not save note"
    
    def read_notes(self):
        """Read notes"""
        try:
            with open("notes.txt", "r", encoding="utf-8") as f:
                notes = f.read().strip()
                return notes if notes else "No notes found"
        except:
            return "No notes file found"
    
    def flip_coin(self):
        """Flip coin"""
        return random.choice(["Heads", "Tails"])
    
    def roll_dice(self, sides=6):
        """Roll dice"""
        try:
            sides = int(sides) if sides else 6
            return str(random.randint(1, sides))
        except:
            return "6"  # Default fallback
    
    def simple_tool_decision(self, user_input):
        """Simple, reliable tool decision"""
        user_lower = user_input.lower().strip()
        
        # Very simple decision prompt
        decision_prompt = f"""
User said: "{user_input}"

Reply with ONLY ONE of these options:
- TIME (if they want time/date)
- MATH (if they want calculations)  
- WEATHER (if they want weather)
- SAVE_NOTE (if they want to save something)
- READ_NOTES (if they want to see notes)
- COIN (if they want coin flip)
- DICE (if they want dice roll)
- CHAT (for normal conversation)

Just the single word, nothing else:
"""
        
        try:
            response = ollama.generate(
                # model='tinyllama',
                model='gemma3:4b',
                prompt=decision_prompt,
                options={'temperature': 0.1, 'max_tokens': 10}
            )
            
            decision = response['response'].strip().upper()
            print(f"🤔 AI chose: {decision}")
            
            # Extract any numbers or text for parameters
            numbers = re.findall(r'\d+', user_input)
            math_expr = re.search(r'[\d\+\-\*\/\.\(\)\s]+', user_input)
            
            if "TIME" in decision:
                return "TIME", None
            elif "MATH" in decision or any(op in user_input for op in ['+', '-', '*', '/', 'calculate']):
                if math_expr:
                    return "MATH", math_expr.group().strip()
                return "MATH", user_input
            elif "WEATHER" in decision:
                return "WEATHER", None
            elif "SAVE" in decision:
                # Extract text after common save phrases
                save_text = user_input
                for phrase in ['save note', 'save', 'note', 'remember']:
                    if phrase in user_lower:
                        save_text = user_input.split(phrase, 1)[-1].strip()
                        break
                return "SAVE_NOTE", save_text
            elif "READ" in decision or "notes" in user_lower:
                return "READ_NOTES", None
            elif "COIN" in decision:
                return "COIN", None
            elif "DICE" in decision:
                sides = numbers[0] if numbers else 6
                return "DICE", sides
            else:
                return "CHAT", None
                
        except Exception as e:
            print(f"❌ Decision error: {e}")
            # Fallback to keyword detection
            if any(word in user_lower for word in ['time', 'date', 'when']):
                return "TIME", None
            elif any(word in user_lower for word in ['calculate', 'math', '+', '-', '*', '/']):
                return "MATH", user_input
            elif any(word in user_lower for word in ['weather', 'temperature']):
                return "WEATHER", None
            elif any(word in user_lower for word in ['save', 'note', 'remember']):
                return "SAVE_NOTE", user_input
            elif any(word in user_lower for word in ['notes', 'show', 'read']):
                return "READ_NOTES", None
            elif any(word in user_lower for word in ['coin', 'flip']):
                return "COIN", None
            elif any(word in user_lower for word in ['dice', 'roll']):
                return "DICE", 6
            else:
                return "CHAT", None
    
    def execute_tool(self, tool_type, param):
        """Execute the selected tool"""
        try:
            if tool_type == "TIME":
                return f"⏰ Current time: {self.get_time()}"
            elif tool_type == "MATH":
                result = self.calculate(param)
                return f"🧮 Calculation result: {result}"
            elif tool_type == "WEATHER":
                result = self.get_weather()
                return f"🌤️ Weather: {result}"
            elif tool_type == "SAVE_NOTE":
                result = self.save_note(param)
                return f"📝 {result}"
            elif tool_type == "READ_NOTES":
                result = self.read_notes()
                return f"📖 Notes:\n{result}"
            elif tool_type == "COIN":
                result = self.flip_coin()
                return f"🪙 Coin flip: {result}"
            elif tool_type == "DICE":
                result = self.roll_dice(param)
                return f"🎲 Dice roll: {result}"
            else:
                return None
        except Exception as e:
            return f"❌ Tool error: {e}"
    
    def generate_response(self, user_input, tool_result):
        """Generate final response"""
        if tool_result:
            # Simple response with tool result
            response_prompt = f"""
User asked: "{user_input}"
Tool result: {tool_result}

Give a brief, helpful response that includes this information:
"""
        else:
            # Normal chat
            response_prompt = f"""
User said: "{user_input}"

Respond naturally and helpfully:
"""
        
        try:
            response = ollama.generate(
                # model='tinyllama',
                model='gemma3:4b',
                prompt=response_prompt,
                options={'temperature': 0.6, 'max_tokens': 150}
            )
            
            return response['response'].strip()
            
        except Exception as e:
            return f"I had an error: {e}"
    
    def run(self):
        """Main loop"""
        print("\n🤖 Simple AI Agent Ready!")
        print("Ask me about: time, math, weather, notes, coin flip, dice, or just chat!")
        print("Type 'quit' to exit\n")
        
        while True:
            try:
                user_input = input("💬 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("🤖 Agent: Goodbye! 👋")
                    break
                
                if not user_input:
                    continue
                
                # Step 1: Decide what to do
                tool_type, param = self.simple_tool_decision(user_input)
                
                # Step 2: Execute tool if needed
                tool_result = None
                if tool_type != "CHAT":
                    tool_result = self.execute_tool(tool_type, param)
                    print(f"🛠️ {tool_result}")
                
                # Step 3: Generate response
                final_response = self.generate_response(user_input, tool_result)
                print(f"🤖 Agent: {final_response}\n")
                
            except KeyboardInterrupt:
                print("\n🤖 Agent: Goodbye! 👋")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue

if __name__ == "__main__":
    agent = FixedAIAgent()
    agent.run()
