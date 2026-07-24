$agents = @'
# Project AI Guardrails & Agent Guidelines

## Tech Stack
- Backend: Python 3.12, FastAPI, SQLAlchemy, SQLite, Pytest
- Frontend: HTML5, CSS3, JavaScript (Vanilla)
- Infrastructure: Docker, GitHub Actions CI

## Standard Development Commands
- Run locally: uvicorn app.main:app --reload
- Run tests: pytest -v
- Docker build: docker build -t tasktracker .
- Docker run: docker run -d -p 8000:8000 --name tasktracker-test tasktracker

## Mandatory Guardrails for AI Collaboration
1. Read First: Always inspect existing app/ and frontend/ modules before proposing changes.
2. Docs First: Any structural API change must update docs/ before implementation.
3. No Scope Creep: Do not add unrequested features (e.g., auth, third-party databases, webhooks).
4. Secret Isolation: Never commit, print, or transmit real credentials or .env contents.
'@
Set-Content -Path "AGENTS.md" -Value $agents -Encoding utf8