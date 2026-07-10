# Prompt Log

## Feature 1: Task status update workflow
- Weak prompt: "Make tasks updateable."
- Stronger prompt: "Add a FastAPI PUT endpoint for tasks that accepts a partial task payload and updates only the provided fields, then return the updated task."
- AI response summary: The AI proposed a basic update route and suggested using a partial schema.
- Human decision: Accepted the route structure, but I refined it to use a dedicated TaskUpdate schema and kept the change narrow.

## Feature 2: Search, priority, and overdue filtering
- Prompt: "Extend GET /tasks/ so it supports search, priority_filter, and overdue_only parameters and filters tasks in the database accordingly."
- AI response summary: The AI returned SQLAlchemy query logic that handled the parameters cleanly.
- Human decision: Accepted with one change: I made overdue filtering compare due_date against today using a date object rather than a string comparison.

## Feature 3: Frontend compatibility
- Prompt: "Make the frontend page work when it is served from the FastAPI app instead of relying on a separate local file open."
- AI response summary: The AI suggested serving the index.html from the root endpoint and switching the browser API URL to the current host.
- Human decision: Accepted and kept the fix minimal to preserve the existing UI behavior.