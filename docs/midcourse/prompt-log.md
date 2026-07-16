# Prompt Log

This log documents how we applied the **AI Interaction Loop (Ask -> Inspect -> Run -> Test -> Refine)** during our sprint.

## Feature 1: Tags and Labels Validation
* **Weak Prompt (Before)**: *"Add tags to the app."*
* **Stronger Prompt (After)**: *"Add an optional tags field to the Task model as a comma-separated string. Update the TaskCreate and TaskUpdate schemas in `app/schemas.py` to include tags. Add a Pydantic field validator that strips extra spaces, removes empty tags, and returns them as a clean comma-separated string. Return a 422 if validation fails."*
* **AI Response Summary**: The AI generated the schema changes and suggested using a list model, which we converted back to a simplified string parser.
* **Human Decision & Refinement**: We rejected the complex array-based models suggested by the AI. We instead implemented the Pydantic `@field_validator` that splits by commas, strips white spaces, and filters out blank values. We verified this behavior using `pytest`.

## Feature 2: Search and Filter API Query
* **Prompt**: *"Modify the GET /tasks endpoint in `app/main.py` to accept optional 'search' and 'tag' query parameters. If search is provided, filter tasks matching the title or description case-insensitively using SQLAlchemy's .ilike(). If tag is provided, filter tasks by matching the tag column. Return the filtered list as TaskResponse schema elements."*
* **AI Response Summary**: The AI correctly built the SQLAlchemy query filtering chain using `query.filter()`.
* **Human Decision & Refinement**: We accepted the pattern, ran the app, tested empty query results (which correctly returned `200 []`), and verified that passing both parameters narrowed down our results correctly.

## Feature 3: Frontend Integration and CORS
* **Prompt**: *"Generate an updated `frontend/index.html` file that communicates with our FastAPI backend. It must support drag-and-drop status updates with transition validation, priority-based sorting (High -> Medium -> Low), render tags as color-coded pills on cards, and include a compact search bar at the top that live-filters the Kanban board using GET /tasks?search=..."*
* **AI Response Summary**: The AI drafted a clean, modern HTML5 Kanban layout with drag-and-drop event handlers and API fetch loops.
* **Human Decision & Refinement**: Upon inspecting the AI code, we noticed that when an invalid drag-and-drop transition occurred (e.g., dragging straight from ToDo to Done), the UI didn't refresh itself automatically. We refined the JS `handleDrop` script to call `fetchTasks()` immediately after a rejection to sync the visual layout with the backend's state contract.