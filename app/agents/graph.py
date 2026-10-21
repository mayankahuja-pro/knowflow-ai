from langgraph.graph import StateGraph, END
from app.agents.state import AgentState
from app.agents.nodes import router_node, rag_tool_node

def create_knowflow_agent():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("router", router_node)
    workflow.add_node("rag_tool", rag_tool_node)
    
    # Define edges and flow
    workflow.set_entry_point("router")
    workflow.add_edge("router", "rag_tool")
    workflow.add_edge("rag_tool", END)
    
    return workflow.compile()

# Initialize compiled graph instance
agent_app = create_knowflow_agent()