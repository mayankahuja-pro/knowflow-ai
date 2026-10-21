from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.get("/")
def root():
    return {
        "message": "Welcome to KnowFlow AI API",
        "docs": "/docs",
        "status": "active"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}