from sqlalchemy.orm import Session
from app.agents.graph import agent_app

def run_agent_workflow(db: Session, question: str, owner_id: int | None = None) -> dict:
    initial_state = {
        "question": question,
        "owner_id": owner_id,
        "db_session": db,
        "messages": [],
        "tool_output": None,
        "citations": [],
        "final_answer": None
    }
    
    # Invoke LangGraph workflow
    final_state = agent_app.invoke(initial_state)
    
    return {
        "answer": final_state.get("final_answer", "No answer generated."),
        "citations": final_state.get("citations", [])
    }