# Enterprise Task Tracker

This project is a Kanban-based task management system developed for the mid-course project.

## Features
1. **Kanban Workflow**: Drag-and-drop status transitions between To Do, In Progress, and Done.
2. **Persistence Layer**: Integrated backend API and database for reliable data storage.

## How to Run

### Backend
1. Navigate to the project root.
2. Install requirements: `pip install -r requirements.txt`
3. Start the server: `uvicorn app.main:app --reload`

### Frontend
1. Navigate to the `frontend/` directory.
2. Serve the site using Live Server (VS Code) or by running: `python -m http.server 8080`
3. Access the dashboard at `http://localhost:8080`.

### Testing
- Ensure you are in the root directory.
- Run the full test suite: `pytest`