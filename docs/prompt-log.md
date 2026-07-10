# Prompt Log

## Feature 1: Status updates
- Weak prompt: “Make tasks updateable.”
- Stronger prompt: “Add a FastAPI PUT endpoint for tasks that accepts a partial task payload and updates only the provided fields, then return the updated task.”
- AI response summary: The model proposed a basic update route and a partial payload schema.
- Human decision: Accepted the route structure, but refined it to use a dedicated TaskUpdate schema and kept the changes narrow.

- Prompt: “Add a query parameter so the API can filter tasks by status.”
- AI response summary: The model suggested an SQLAlchemy filter on the status column.
- Human decision: Accepted and kept the implementation consistent with the existing router pattern.

- Prompt: “Make the frontend reflect status changes after a task is moved.”
- AI response summary: The model suggested reloading the board after a successful update.
- Human decision: Accepted and preserved the simple UX flow.

## Feature 2: Search, priority, and overdue filters
- Prompt: “Extend GET /tasks/ so it supports search, priority_filter, and overdue_only parameters.”
- AI response summary: The model returned SQLAlchemy query logic for all three filters.
- Human decision: Accepted with one refinement: overdue filtering compares due_date against the current date using a proper date object.

- Prompt: “Support filtering by tag or title in the task list.”
- AI response summary: The model suggested combining title and tag matching in a case-insensitive search.
- Human decision: Accepted and kept the matching logic simple.

- Prompt: “Make the board work correctly when the page is served from FastAPI.”
- AI response summary: The model suggested serving the index HTML and pointing the browser to the same host.
- Human decision: Accepted and kept the fix minimal to preserve the current UI.
