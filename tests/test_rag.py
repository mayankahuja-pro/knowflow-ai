from app.services.rag_service import chunk_text

def test_chunk_text():
    sample_text = "Enterprise AI knowledge management and decision science platforms require robust chunking algorithms. " * 50
    chunks = chunk_text(sample_text, chunk_size=30, overlap=5)
    
    assert len(chunks) > 1
    assert isinstance(chunks[0], str)
    assert len(chunks[0]) > 0