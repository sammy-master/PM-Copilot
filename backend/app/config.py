"""
PM Copilot - Application Configuration
---------------------------------------
Reads all settings from environment variables (.env file).
Pydantic Settings automatically validates types and provides defaults.
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # ---- Application ----
    app_name: str = "PM Copilot"
    app_version: str = "1.0.0"
    debug: bool = True
    frontend_url: str = "http://localhost:3000"

    # ---- Database ----
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/pm_copilot"

    # ---- JWT Auth ----
    secret_key: str = "change-this-secret-key-in-production-use-a-long-random-string"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours

    # ---- AI Provider ----
    ai_provider: str = "ollama"  # "ollama" | "openai" | "gemini"

    # ---- Ollama ----
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"

    # ---- OpenAI ----
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # ---- Gemini ----
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"

    # ---- Embeddings ----
    embedding_provider: str = "sentence_transformers"
    embedding_model: str = "all-MiniLM-L6-v2"
    ollama_embedding_model: str = "nomic-embed-text"

    # ---- ChromaDB ----
    chroma_persist_dir: str = "./chroma"

    # ---- File Uploads ----
    upload_dir: str = "./uploads"
    max_upload_size_mb: int = 10

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore unknown env vars


# Single global instance — import this anywhere in the app
settings = Settings()
