# Prompt Log

This log documents how we applied the **AI Interaction Loop (Ask -> Inspect -> Run -> Test -> Refine)** during our sprint.

## Feature 1: Tags and Labels Validation
* **Weak Prompt (Before)**: *"Add tags to the app."*
* **Stronger Prompt (After)**: *"Add an optional tags field to the Task Pydantic model as a comma-separated string in `app/main.py`. Add a field validator that strips extra spaces, removes empty tags, and returns them as a clean comma-separated string. Ensure it returns a validation error if empty values are passed improperly."*
* **AI Response Summary**: The AI generated the schema changes and suggested using a list model, which we converted back to a simplified string parser.
* **Human Decision & Refinement**: We rejected the complex array-based models suggested by the AI. We instead implemented a clean Pydantic `@field_validator` that splits by commas, strips whitespaces, and filters out blank values. We verified this behavior using our `pytest` test suite.

## Feature 2: Search and Filter API Query
* **Prompt**: *"Modify the GET `/api/tasks/` endpoint in `app/main.py` to accept an optional 'status' query parameter. If provided, filter tasks matching that status precisely. Ensure the endpoint safely returns an empty list `[]` if no matching tasks exist."*
* **AI Response Summary**: The AI provided a standard query filtering list comprehension pattern matching the selected state.
* **Human Decision & Refinement**: We accepted the pattern, updated the endpoint, and verified that passing the query parameter narrowed down our results correctly while maintaining compatibility with the existing frontend lifecycle.

## Feature 3: Frontend Integration and CORS
* **Prompt**: *"Generate an updated `Frontend/index.html` file that communicates with our FastAPI backend. It must support drag-and-drop status updates with a backwards-movement workflow restriction (rejecting In Progress to To Do), display a clean light UI layout inspired by Jira typography, add an assignee field, and include a compact filter bar at the top."*
* **AI Response Summary**: The AI drafted a clean, modern HTML5 Kanban layout with drag-and-drop event handlers, visual assignee initials badges, and API fetch loops.
* **Human Decision & Refinement**: Upon inspecting the code, we adjusted the layout's grid gaps to ensure clean column separation. We also verified that when an invalid drag-and-drop transition occurred, a clear alert message was triggered on the screen without corrupting the backend state.