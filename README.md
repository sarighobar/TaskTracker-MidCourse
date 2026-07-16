# Task Tracker API

A lightweight, enterprise-ready task-tracking workspace with a FastAPI backend and a Kanban-style frontend. The system allows users to create, view, filter, update, and delete tasks, while strictly validating workflow progressions across task statuses in the backend.

---

## Features

* **Strict Workflow Validation**: Enforces valid status transitions (e.g., `ToDo` $\rightarrow$ `InProgress` $\rightarrow$ `Done`) directly in the database logic.
* **Unified Text Search**: Live search matching keywords case-insensitively across both task titles and descriptions.
* **Tags & Category Labels**: Supports organizing tasks with tag chips, including built-in backend validation to trim whitespace and clean up empty comma inputs.
* **Direct UI Hosting**: The FastAPI app hosts the Single-Page Application (SPA) directly from the root URL.
* **Robust Test Coverage**: Verified with a clean `pytest` integration test suite.

---

## Folder Structure

```text
TaskTracker/
│
├── app/                     # FastAPI Backend Implementation
│   ├── business_rules.py    # Transition matrices & safety rules
│   ├── database.py          # SQLAlchemy SQLite connection setup
│   ├── main.py              # Application routers and frontend delivery
│   ├── models.py            # SQLite declarative database schemas
│   └── schemas.py           # Pydantic payloads & validators
│
├── docs/midcourse/          # Project documentation deliverables
│   ├── mini-adr.md          # Architectural decisions
│   ├── prompt-log.md        # AI Loop prompt logs
│   ├── user-stories.md      # Features and acceptance criteria
│   └── verification.md      # Testing and break test evidence
│
├── frontend/
│   └── index.html           # Kanban Drag-and-Drop Board UI
│
└── tests/
    └── test_tasks.py        # Automated test suite

    -- Use this command to reload/luanch the FE app:

    python -m uvicorn app.main:app --reload

    http://127.0.0.1:8000
    http://127.0.0.1:8000/docs