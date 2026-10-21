from openai import OpenAI
from app.config import settings

_client = None

def get_openai_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client

def generate_embedding(text: str) -> list[float]:
    client = get_openai_client()
    response = client.embeddings.create(
        model=settings.EMBEDDING_MODEL_NAME,
        input=text
    )
    return response.data[0].embedding