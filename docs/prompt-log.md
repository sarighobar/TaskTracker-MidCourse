# AI Prompt Log

## Feature 1: Tags / Labels
* **Weak Prompt (Initial Idea):** "Make tags for my application."
* **Strong Refactored Prompt:** "In `app/schemas/task.py`, create Pydantic schemas for `TaskCreate`, `TaskUpdate`, and `TaskResponse`. For the `tags` field, allow it to accept a string or null, but strip leading/trailing spaces if provided. Ensure the response schema includes the `id` and `status` fields."
* **AI Return Summary:** The AI returned a fully functional Pydantic validator snippet utilizing python strings split and list-comprehensions to normalize spaces.
* **Human Decision:** Accepted completely. It prevents broken empty tags or trailing space errors elegantly.

## Feature 2: Search + Combined Filters
* **Prompt Used:** "In `app/routers/task.py`, create the FastAPI APIRouter handling CRUD operations for our Tasks. Crucially, for `GET /tasks`, implement an optional `search` query parameter. If `search` is provided, use SQLAlchemy to filter tasks whose `title`, `description`, or `tags` contain that search string (case-insensitive partial matching)."
* **AI Return Summary:** Provided a route using `.ilike()` statements combined with the OR bitwise pipe operator (`|`).
* **Human Decision:** Accepted. Case-insensitive checking across all fields simultaneously meets our single search bar constraints perfectly.