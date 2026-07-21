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
4. Open `http://127.0.0.1:8000` in your browser — the backend serves `Frontend/index.html` directly at `/`, so no separate frontend server is needed.

### Frontend (optional, standalone)
If you'd rather serve the frontend separately (e.g. for frontend-only development):
1. Navigate to the `Frontend/` directory (capital `F`).
2. Serve the folder using Live Server (VS Code) or by running: `python -m http.server 8080`
3. Access the dashboard at `http://localhost:8080`.
4. Note: the backend must still be running (`uvicorn app.main:app --reload`) for API calls to succeed, since `Frontend/index.html` calls `/api/tasks/` on the same origin it's served from.

### Testing
- Ensure you are in the project root.
- Run the full test suite: `pytest -v`

## Documentation
Project documentation — user stories, mini-ADR, prompt log, verification report, and reflection — lives in `docs/midcourse/`.
