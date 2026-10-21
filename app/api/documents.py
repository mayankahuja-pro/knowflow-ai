from fastapi import APIRouter, Depends, UploadFile, File, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.document import Document
from app.schemas.document import DocumentResponse
from app.services.auth_service import get_current_user
from app.services.ingestion_service import validate_and_save_file, extract_text_from_file, create_document_record

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    file_path, file_type, file_size = validate_and_save_file(file)
    # Extract text to test parser functionality
    _ = extract_text_from_file(file_path, file_type)
    
    document = create_document_record(
        db=db,
        filename=file.filename,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
        owner_id=current_user.id
    )
    return document

@router.get("/", response_model=List[DocumentResponse])
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.is_superuser:
        return db.query(Document).all()
    return db.query(Document).filter(Document.owner_id == current_user.id).all()