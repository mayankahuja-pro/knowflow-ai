from sqlalchemy.orm import Session
from app.agents.graph import agent_app
from app.services.redis_service import get_cached_answer, set_cached_answer

def run_agent_workflow(db: Session, question: str, owner_id: int | None = None) -> dict:
    # 1. Check Redis cache first
    cached_result = get_cached_answer(question, owner_id)
    if cached_result:
        cached_result["answer"] = "[Cached] " + cached_result["answer"]
        return cached_result

    # 2. Run LangGraph workflow if not cached
    initial_state = {
        "question": question,
        "owner_id": owner_id,
        "db_session": db,
        "messages": [],
        "tool_output": None,
        "citations": [],
        "final_answer": None
    }
    
    final_state = agent_app.invoke(initial_state)
    
    result = {
        "answer": final_state.get("final_answer", "No answer generated."),
        "citations": final_state.get("citations", [])
    }
    
    # 3. Store result in Redis cache (expires in 1 hour)
    set_cached_answer(question, owner_id, result)
    
    return result