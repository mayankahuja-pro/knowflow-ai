from sqlalchemy import Column, Integer, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.database import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    # 1536 dimensions corresponds to OpenAI's 'text-embedding-3-small' default model
    embedding = Column(Vector(1536), nullable=True)
    chunk_metadata = Column(JSON, nullable=True)

    document = relationship("Document", backref="chunks")