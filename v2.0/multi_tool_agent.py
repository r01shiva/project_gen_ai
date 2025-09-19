import ollama
import json
import datetime
import random

class AIAgent:
    def __init__(self):
        self.tools = {
            'get_current_time': self.get_current_time,
            'calculate': self.calculator,
            'weather_info': self.get_weather_info,
            'note_keeper': self.note_keeper
        }
        self.notes = []
    
    def get_current_time(self, format_type="full"):
        """Get current date and time"""
        now = datetime.datetime.now()
        if format_type == "date":
            return now.strftime("%Y-%m-%d")
        elif format_type == "time":
            return now.strftime("%H:%M:%S")
        else:
            return now.strftime("%Y-%m-%d %H:%M:%S")
    
    def calculator(self, expression):
        """Simple calculator (be careful with eval in real applications!)"""
        try:
            # Very basic safety check
            allowed_chars = "0123456789+-*/.() "
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return f"Result: {result}"
            else:
                return "Error: Invalid characters in expression"
        except Exception as e:
            return f"Calculation error: {e}"
    
    def get_weather_info(self, location="local"):
        """Simulate weather information"""
        weather_conditions = ["sunny", "cloudy", "rainy", "partly cloudy", "stormy"]
        temperature = random.randint(15, 35)
        condition = random.choice(weather_conditions)
        return f"Weather in {location}: {condition}, {temperature}°C"
    
    def note_keeper(self, action, note=""):
        """Keep notes - add, list, or clear"""
        if action == "add" and note:
            self.notes.append(f"[{self.get_current_time()}] {note}")
            return f"Note added: {note}"
        elif action == "list":
            if self.notes:
                return "\n".join([f"{i+1}. {note}" for i, note in enumerate(self.notes)])
            else:
                return "No notes found."
        elif action == "clear":
            count = len(self.notes)
            self.notes.clear()
            return f"Cleared {count} notes."
        else:
            return "Usage: note_keeper(action='add/list/clear', note='your note')"
    
    def process_request(self, user_input):
        """Main agent processing logic"""
        
        # First, determine what tools to use
        analysis_prompt = f"""
        Analyze this user request and determine which tools to use: {user_input}
        
        Available tools:
        - get_current_time(format_type="full/date/time"): Get current date/time
        - calculate(expression="math expression"): Perform calculations
        - weather_info(location="place"): Get weather information  
        - note_keeper(action="add/list/clear", note="text"): Manage notes
        
        Respond in JSON format:
        {{
            "tools_needed": [
                {{"tool": "tool_name", "params": {{"param": "value"}}}}
            ],
            "reasoning": "Why these tools are needed"
        }}
        
        If no tools are needed, respond with regular conversation.
        """
        
        analysis = ollama.generate(
            model='tinyllama',
            prompt=analysis_prompt,
            options={'temperature': 0.2}
        )
        
        print(f"🤔 Agent thinking: {analysis['response']}\n")
        
        # Try to extract JSON and execute tools
        try:
            # Simple JSON extraction (in real apps, use proper parsing)
            response_text = analysis['response']
            if '"tools_needed"' in response_text:
                # Execute the tools (simplified for demo)
                tool_results = []
                
                # For demo, let's handle common cases manually
                if "time" in user_input.lower() or "date" in user_input.lower():
                    result = self.get_current_time()
                    tool_results.append(f"Current time: {result}")
                
                if any(op in user_input for op in ['+', '-', '*', '/', 'calculate']):
                    # Extract numbers and operators (very basic)
                    import re
                    math_expr = re.search(r'[\d\+\-\*\/\.\(\)\s]+', user_input)
                    if math_expr:
                        result = self.calculator(math_expr.group())
                        tool_results.append(result)
                
                if "weather" in user_input.lower():
                    result = self.get_weather_info()
                    tool_results.append(result)
                
                if "note" in user_input.lower():
                    if "add" in user_input.lower():
                        note_text = user_input.split("add")[-1].strip()
                        result = self.note_keeper("add", note_text)
                        tool_results.append(result)
                    elif "list" in user_input.lower():
                        result = self.note_keeper("list")
                        tool_results.append(result)
                
                # Generate final response using tool results
                if tool_results:
                    final_prompt = f"""
                    User asked: {user_input}
                    
                    Tool results: {'; '.join(tool_results)}
                    
                    Provide a helpful response incorporating these results:
                    """
                    
                    final_response = ollama.generate(
                        model='tinyllama',
                        prompt=final_prompt,
                        options={'temperature': 0.4}
                    )
                    
                    return final_response['response']
        
        except Exception as e:
            print(f"Tool execution error: {e}")
        
        # Fallback to normal conversation
        normal_prompt = f"Respond helpfully to: {user_input}"
        response = ollama.generate(model='tinyllama', prompt=normal_prompt)
        return response['response']

def agent_demo():
    print("🤖 Multi-Tool AI Agent")
    print("I can help with time, calculations, weather, notes, and general questions!")
    print("\nTry asking:")
    print("- What time is it?")
    print("- Calculate 15 * 8 + 20")
    print("- What's the weather like?")
    print("- Add note: Meeting at 3pm")
    print("- List my notes")
    
    agent = AIAgent()
    
    while True:
        user_input = input("\n💬 You: ")
        if user_input.lower() in ['quit', 'exit']:
            break
        
        response = agent.process_request(user_input)
        print(f"\n🤖 Agent: {response}")

if __name__ == "__main__":
    agent_demo()
