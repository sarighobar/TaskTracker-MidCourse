# Prompt Log

## Feature 1: Tags & Labels

### Prompt 1
> **Prompt:** "Write a Pydantic validator or SQLAlchemy helper function to parse comma-separated tags, strip whitespace around each tag, and strip empty strings."  
> **Outcome:** Implemented normalization logic ensuring input like `" backend , , devops "` cleans to `"backend,devops"`.

### Prompt 2
> **Prompt:** "How do I render tag chips visually inside a CSS flex layout on Kanban card elements in raw HTML/JS?"  
> **Outcome:** Created `.tag-chips` and `.chip` CSS classes and updated dynamic card generation in JavaScript.

### Prompt 3
> **Prompt:** "Write pytest test cases using FastAPI TestClient to test creating tasks with tags, stripping empty tags, filtering by tag, and preserving tags during status updates."  
> **Outcome:** Added full automated test coverage for all tag operations in `tests/test_tasks.py`.

---

## Feature 2: Search & Combined Filters

### Prompt 1
> **Prompt:** "How do I construct a SQLAlchemy query using `.ilike()` and `OR` conditions to search across both title and description fields in FastAPI?"  
> **Outcome:** Updated `get_tasks` endpoint in `routers/tasks.py` to handle case-insensitive multi-column search.

### Prompt 2
> **Prompt:** "How can I combine multiple optional query parameters (`status`, `priority`, `search`, `tag`) in a single FastAPI route?"  
> **Outcome:** Chained conditional query filters dynamically based on non-null parameters.

### Prompt 3
> **Prompt:** "Write automated pytest functions to test searching titles/descriptions, combining status and priority, handling non-matching queries returning HTTP 200 `[]`, and testing invalid input handling."  
> **Outcome:** Added full test suite verifying search and combined filter behaviors in `tests/test_tasks.py`.