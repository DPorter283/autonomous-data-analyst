from langchain_core.messages import HumanMessage
from src.agents.analyst_agent import app

def run_chat():
    print("💬 Starting Autonomous Analyst Chat (Type 'quit' to exit)")
    print("-" * 50)
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            print("👋 Goodbye!")
            break
            
        # 1. Create the initial state (The user's message)
        initial_state = {"messages": [HumanMessage(content=user_input)]}
        
        # 2. Run the Graph!
        # The graph will process the state through the nodes we defined.
        result = app.invoke(initial_state)
        
        # 3. Extract the last message (The AI's response)
        ai_response = result["messages"][-1].content
        
        print(f"AI: {ai_response}")
        print("-" * 50)

if __name__ == "__main__":
    run_chat()
