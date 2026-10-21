from typing import TypedDict, List, Dict, Any, Optional

class AgentState(TypedDict):
    question: str
    owner_id: int
    db_session: Any
    messages: List[Dict[str, Any]]
    tool_output: Optional[str]
    citations: List[Dict[str, Any]]
    final_answer: Optional[str]