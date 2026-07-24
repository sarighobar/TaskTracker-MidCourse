# Enterprise Task Tracker

This project is a Kanban-based task management system developed for the mid-course project.

## Features
1. **Kanban Workflow**: Drag-and-drop status transitions between To Do, In Progress, and Done.
2. **Persistence Layer**: Integrated backend API and database for reliable data storage.
3. **Tags / Labels**: Comma-separated tags on tasks, with tag chips on cards and tag filtering.
4. **Search + Combined Filters**: Text search across title/description, combinable with status, priority, and tag filters.

## How to Run

### Backend (also serves the frontend)
1. Navigate to the project root.
2. Install requirements: `pip install -r requirements.txt`
3. Start the server: `uvicorn app.main:app --reload`
4. Open `http://127.0.0.1:8000` in your browser — the backend serves `frontend/index.html` directly at `/`, so no separate frontend server is needed.

### Frontend (optional, standalone)
If you'd rather serve the frontend separately (e.g. for frontend-only development):
1. Navigate to the `frontend/` directory.
2. Serve the folder using Live Server (VS Code) or by running: `python -m http.server 8080`
3. Access the dashboard at `http://localhost:8080`.
4. Note: the backend must still be running (`uvicorn app.main:app --reload`) for API calls to succeed, since `frontend/index.html` calls `/api/tasks/` on the same origin it's served from.

### Testing
- Ensure you are in the project root.
- Run the full test suite: `pytest -v`

### Docker Support
1. Build the image: `docker build -t tasktracker .`
2. Run the container: `docker run -d -p 8000:8000 --name tasktracker-test tasktracker`
3. Verify health: `curl http://127.0.0.1:8000/health`

## Documentation
Project documentation — user stories, mini-ADR, prompt log, verification report, and reflection — lives in `docs/`.

---

## Final Project
Branch reviewed: final-project

### What this submission demonstrates
Existing Task Tracker app still runs inside the intended course scope.
CI runs the pytest suite on push and/or pull request.
Docker image builds and runs with /health returning 200.
AI review, security, and ownership evidence is in docs/.

### How to run locally
`uvicorn app.main:app --reload`

### How to run tests
`pytest -v`

### How to run with Docker
`docker build -t tasktracker .`
`docker run -d -p 8000:8000 --name tasktracker-test tasktracker`
`curl http://127.0.0.1:8000/health`

### Evidence files
- docs/release-evidence.md
- docs/final-ai-review.md
- docs/ai-playbook.md

### AI assistance summary
AI helped draft or review: CI workflow, Dockerfile container hardening, documentation claim-vs-reality logs, and test structure.
I verified the work by: Full pytest execution, manual Kanban board testing in the browser, and checking container runtime logs in GitHub Actions.
One AI suggestion I rejected or corrected: AI suggested adding full JWT user authentication, which I rejected to stay strictly within project scope and prevent scope creep.