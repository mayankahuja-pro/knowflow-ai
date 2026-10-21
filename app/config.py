from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "KnowFlow AI"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    LLM_PROVIDER: str = "gemini"
    GEMINI_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()