This project implements a Task Tracker application composed of a FastAPI backend and a Kanban-style frontend. The system allows users to create, view, filter, update, and delete tasks, while also supporting workflow progression across task statuses. In addition, the project includes search and filtering capabilities for priority and overdue items. Documentation has been prepared in the docs/midcourse directory, covering user stories, design decisions, prompt history, verification evidence, and reflection. The application was tested using pytest, and the core user workflows were validated through browser-based manual checks.

# TaskTracker API
A lightweight task-tracking workspace with a FastAPI backend and a Kanban-style frontend.

## Features
- Status filtering for task workflow stages such as To Do, In Progress, and Done
- Search across task titles and tags with case-insensitive matching
- Tag normalization that trims whitespace in comma-separated values
- Frontend integration so the UI can create, list, filter, update, and delete tasks

## Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Start the app with: `python -m uvicorn app.main:app --host 127.0.0.1 --port 8000`
4. Open: `http://127.0.0.1:8000/`

## Testing
Run the full suite with:
`python -m pytest -q`

## Documentation
Project notes and planning artifacts are in the [docs](docs) folder.

## Repository
GitHub repository: https://github.com/sarighobar/TaskTracker-MidCourse
