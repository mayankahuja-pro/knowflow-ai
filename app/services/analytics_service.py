import pandas as pd
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.document import Document
from app.services.llm_service import generate_chat_completion

def analyze_csv_document(db: Session, document_id: int, owner_id: int | None = None) -> dict:
    stmt = db.query(Document).filter(Document.id == document_id)
    if owner_id is not None:
        stmt = stmt.filter(Document.owner_id == owner_id)
    doc = stmt.first()
    
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found or unauthorized."
        )
    if doc.file_type != ".csv":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Analytics is currently supported only for CSV documents."
        )
        
    try:
        df = pd.read_csv(doc.file_path)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to read CSV file: {str(e)}"
        )
        
    summary = df.describe(include="all").fillna("").to_dict()
    
    prompt = f"""You are an Enterprise Decision Science Analyst at Accenture. Analyze the following summary statistics of a business dataset ({doc.filename}) and provide 3 key executive business insights:

Summary Statistics:
{summary}

Provide professional, data-backed business recommendations."""

    insights = generate_chat_completion(prompt)
    
    return {
        "summary_stats": {str(k): str(v) for k, v in summary.items()},
        "insights": insights
    }