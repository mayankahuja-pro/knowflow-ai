from pydantic import BaseModel
from typing import List

class QuestionRequest(BaseModel):
    question: str

class Citation(BaseModel):
    document_id: int
    filename: str
    chunk_index: int
    content_snippet: str

class AnswerResponse(BaseModel):
    answer: str
    citations: List[Citation]