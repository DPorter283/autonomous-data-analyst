import operator
from typing import Annotated, TypedDict

from langchain_aws import ChatBedrock
from langchain_core.messages import SystemMessage
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from src.tools.sql import query_dummy_database

from src.core.config import settings

# --- 1. Define the State (The Brain's Memory) ---
class AgentState(TypedDict):
    """
    The state defines what data is passed between nodes in the graph.
    'messages': A list of chat history. 
    'operator.add' tells LangGraph to APPEND new messages, not overwrite.
    """
    messages: Annotated[list[BaseMessage], operator.add]

# --- 2. Initialize the Model (The LLM) ---
# We use ChatBedrock to wrap AWS Bedrock in a standard LangChain interface
llm = ChatBedrock(
    model_id=settings.model_id,
    region_name=settings.aws_region,
    # Temperature 0 = Strict/Factual (Good for SQL generation later)
    model_kwargs={"temperature": 0} 
    
    
)

# Define the list of tools
tools = [query_dummy_database]
    
# Bind the tools to the model
# This modifies the LLM so it KNOWS these functions exist
    
llm_with_tools = llm.bind_tools(tools)

# --- 3. Define Nodes (The Actions) ---
def call_model(state: AgentState):
    """
    The main node. It takes the current conversation history (state),
    sends it to the LLM, and returns the LLM's response.
    """
    print("🤖 Agent is thinking...")
    
    # Get the message history from the state
    messages = state["messages"]
    
    # We prepend a System Message to enforce the persona
    # In a real app, this would be part of the initial state, but this works for now.
    system_prompt = SystemMessage(content=""" You are a Senior Data Analyst at a Fortune 500 company.
    You are an expert in SQL, AWS Redshift, and Business Intelligence.                               
    You speak efficiently and focus on data accuracy.
    If you don't know the answer, say "I need to check the database." """
        
    )
    
    # We combine the system prompt + conversation history
    # Note: We don't save the system prompt to the state here, just send it to the model.
    #response = llm.invoke([system_prompt] + messages)
    response = llm_with_tools.invoke([system_prompt]+ messages)
    
    
    # Return the update (LangGraph will append this to the state)
    return {"messages": [response]}

# --- 4. Build the Graph (The Workflow) ---
workflow = StateGraph(AgentState)

# Add the node we defined above
# Update 2: The Agent (Thinking)
workflow.add_node("agent", call_model)

# Set the entry point: Start -> Agent
# Update 2: LangGraph provides a prebult node that runs the tools automatically

tool_node = ToolNode(tools)
workflow.add_node("tools", tool_node)

# Entry Point
workflow.add_edge(START, "agent")

# The Conditional Edge
# After the agent thinks, we check: "Did it ask for a tool"

workflow.add_conditional_edges(
    "agent",
    tools_condition, #This function checks if the LLM output contains tool_calls
    {
        "tools": "tools", #if yes, go to "tools" node
        END: END
        
    }
)

# The Loop Back
# After the tool runs, give the data back to the agent so it can answer the user
workflow.add_edge("tools", END)

# Compile the graph into a runnable application
app = workflow.compile()
