from sqlalchemy.orm import Session
from app.agents.state import AgentState
from app.services.rag_service import answer_question_with_rag

def router_node(state: AgentState) -> AgentState:
    """Decides whether to route to RAG tool or direct fallback."""
    # For now, all enterprise questions go through our secure RAG tool
    return state

def rag_tool_node(state: AgentState) -> AgentState:
    question = state["question"]
    owner_id = state.get("owner_id")
    db: Session = state["db_session"]
    
    result = answer_question_with_rag(db, question, owner_id=owner_id)
    
    state["final_answer"] = result["answer"]
    state["citations"] = result["citations"]
    return state