from fastapi import FastAPI
from app.config import settings
from app.api import auth, documents, chat, analytics

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(documents.router, prefix=settings.API_V1_STR)
app.include_router(chat.router, prefix=settings.API_V1_STR)
app.include_router(analytics.router, prefix=settings.API_V1_STR)

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