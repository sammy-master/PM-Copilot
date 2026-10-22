"""
PM Copilot - FastAPI Application Entry Point
---------------------------------------------
This is where the entire backend starts.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_tables
import app.models.user  # noqa: F401 — ensures User table is created on startup


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs setup code before the server starts, and cleanup after it stops.
    - Creates DB tables on first run (if DB is configured)
    - Creates upload/chroma directories if they don't exist
    """
    # Create directories if they don't exist
    os.makedirs(settings.upload_dir, exist_ok=True)
    os.makedirs(settings.chroma_persist_dir, exist_ok=True)

    # Try to connect to DB — warn if not configured yet (don't crash)
    try:
        await create_tables()
        print("[OK] Database connected and tables created")
    except Exception as e:
        print(f"[WARN] Database not connected: {e}")
        print("[WARN] Set DATABASE_URL in .env to enable database features")

    print(f"[OK] PM Copilot Backend started - AI Provider: {settings.ai_provider.upper()}")
    print(f"[>>] API Docs: http://localhost:8000/docs")

    yield  # Server is running

    print("[STOP] PM Copilot Backend shutting down...")


# Create the FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered assistant for Product Managers",
    lifespan=lifespan,
)

# ---- CORS Middleware ----
# Allows the Next.js frontend (on a different port) to call this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- Health Check ----
@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "PM Copilot API is running",
        "version": settings.app_version,
        "ai_provider": settings.ai_provider,
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}


# ---- Register API Routers ----
from app.api.v1 import auth
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])

# (More routers will be added as we build each feature)
# from app.api.v1 import chat, generate, documents, projects, history
# app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
# app.include_router(generate.router, prefix="/api/v1/generate", tags=["Generate"])
# app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])
# app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
# app.include_router(history.router, prefix="/api/v1/history", tags=["History"])
