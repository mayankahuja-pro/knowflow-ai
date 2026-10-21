import os
import shutil
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
import pandas as pd
from pypdf import PdfReader
from app.models.document import Document

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".csv"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def validate_and_save_file(file: UploadFile) -> tuple[str, str, int]:
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{ext}'. Allowed types: PDF, TXT, CSV."
        )
    
    # Read file content to check size
    contents = file.file.read()
    file_size = len(contents)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the 10MB limit."
        )
    
    # Save file locally
    file_path = os.path.join(UPLOAD_DIR, f"{os.urandom(8).hex()}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Reset file pointer for future reading if needed
    file.file.seek(0)
    return file_path, ext, file_size

def extract_text_from_file(file_path: str, file_type: str) -> str:
    text = ""
    try:
        if file_type == ".pdf":
            reader = PdfReader(file_path)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        elif file_type == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        elif file_type == ".csv":
            df = pd.read_csv(file_path)
            text = df.to_string(index=False)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract text from file: {str(e)}"
        )
    return text

def create_document_record(db: Session, filename: str, file_path: str, file_type: str, file_size: int, owner_id: int) -> Document:
    db_doc = Document(
        filename=filename,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
        owner_id=owner_id
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc