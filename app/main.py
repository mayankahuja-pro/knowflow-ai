
from fastapi import FastAPI

app = FastAPI(
    title="KnowFlow AI",
    description="Enterprise AI Knowledge and Decision Assistant",
    version="0.1.0",
)


@app.get("/")
def home():
    return {
        "message": "Welcome to KnowFlow AI",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "knowflow-ai",
    }
