
from sqlalchemy.orm import Session
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import generate_embedding
from app.services.llm_service import generate_chat_completion


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> list[str]:
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)

    return chunks


def process_and_store_document_chunks(
    db: Session,
    document_id: int,
    text: str
):
    chunks = chunk_text(text)

    for idx, chunk_content in enumerate(chunks):
        embedding_vector = generate_embedding(chunk_content)

        db_chunk = DocumentChunk(
            document_id=document_id,
            chunk_index=idx,
            content=chunk_content,
            embedding=embedding_vector
        )

        db.add(db_chunk)

    db.commit()


def search_similar_chunks(
    db: Session,
    query: str,
    top_k: int = 4,
    owner_id: int | None = None
) -> list[DocumentChunk]:
    query_vector = generate_embedding(query)

    stmt = db.query(DocumentChunk).join(DocumentChunk.document)

    if owner_id is not None:
        stmt = stmt.filter(Document.owner_id == owner_id)

    stmt = stmt.order_by(
        DocumentChunk.embedding.cosine_distance(query_vector)
    )

    results = stmt.limit(top_k).all()
    return results


def answer_question_with_rag(
    db: Session,
    question: str,
    owner_id: int | None = None
) -> dict:
    # 1. Retrieve the most relevant chunks
    similar_chunks = search_similar_chunks(
        db,
        question,
        top_k=4,
        owner_id=owner_id
    )

    if not similar_chunks:
        return {
            "answer": (
                "I could not find any relevant documents in your "
                "knowledge base to answer this question. "
                "Please upload relevant documents first."
            ),
            "citations": []
        }

    # 2. Construct context and citations
    context_parts = []
    citations = []

    for chunk in similar_chunks:
        context_parts.append(
            f"--- Document ID: {chunk.document_id} "
            f"({chunk.document.filename}) ---\n"
            f"{chunk.content}"
        )

        citations.append({
            "document_id": chunk.document_id,
            "filename": chunk.document.filename,
            "chunk_index": chunk.chunk_index,
            "content_snippet": chunk.content[:150] + "..."
        })

    context_text = "\n\n".join(context_parts)

    # 3. Build the RAG prompt
    prompt = f"""You are KnowFlow AI, an enterprise knowledge
and decision assistant.

Answer the user's question using ONLY the provided context.
If the answer cannot be found in the context, clearly state
that you do not have enough information in the uploaded
documents. Never invent facts.

Context:
{context_text}

User Question: {question}

Answer professionally with clear explanations and refer to
the source document names when citing information."""

    # 4. Generate the answer
    answer = generate_chat_completion(prompt)

    return {
        "answer": answer,
        "citations": citations
    }
