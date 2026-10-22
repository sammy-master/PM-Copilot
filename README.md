# PM Copilot — B.Tech Final Year Project

> An AI-powered assistant for Product Managers using Generative AI, LLMs, and RAG.

## Project Structure

```
pm-copilot/
├── frontend/      # Next.js + TypeScript + Tailwind CSS
└── backend/       # Python + FastAPI
```

## Quick Start

### 1. Clone & Setup Environment

```bash
# Backend
cd backend
cp .env.example .env        # Fill in your values
pip install -r requirements.txt

# Frontend
cd frontend
cp .env.local.example .env.local    # Fill in your Clerk keys
npm install
```

### 2. Start Ollama (Local LLM)

```bash
# Install from https://ollama.com
ollama pull llama3.2
ollama serve
```

### 3. Run Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 4. Run Frontend

```bash
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

## AI Concepts Demonstrated

| Concept | Where |
|---|---|
| LLM Integration | PRD, User Story, Roadmap generators |
| Prompt Engineering | `/backend/app/prompts/` |
| RAG | Document upload + Q&A |
| Embeddings | `sentence-transformers` |
| Vector Database | ChromaDB |
| Semantic Search | Document retrieval |
| Streaming | Chat interface |
| Provider Pattern | Ollama / OpenAI / Gemini switching |

## Tech Stack

**Frontend:** Next.js · TypeScript · Tailwind CSS · shadcn/ui  
**Backend:** Python · FastAPI · SQLAlchemy  
**Database:** PostgreSQL · ChromaDB  
**AI:** Ollama (LLaMA 3.2) · LangChain · Sentence Transformers  
**Auth:** Clerk  
**Deploy:** Vercel (Frontend) · Railway (Backend)
