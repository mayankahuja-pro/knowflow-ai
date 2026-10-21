from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.chat import QuestionRequest, AnswerResponse
from app.services.auth_service import get_current_user
from app.services.agent_service import run_agent_workflow

router = APIRouter(prefix="/chat", tags=["RAG Chat & Agent"])

@router.post("/ask", response_model=AnswerResponse)
def ask_question(
    payload: QuestionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    owner_filter = None if current_user.is_superuser else current_user.id
    result = run_agent_workflow(db, payload.question, owner_id=owner_filter)
    return result