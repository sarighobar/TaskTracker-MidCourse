# User Stories

## Feature 1: Tags and Labels (Category Tracking)
1. **As a developer**, I want to add tags (e.g., "bug", "frontend") to a task when creating it, so that I can categorize and group my work.
   - **Acceptance Criteria**: The `POST /api/tasks/` payload accepts a `tags` string. The backend parses, trims whitespace, filters empty strings, and stores them as a clean, comma-separated string.
   - **AI Assumption Corrected**: The AI assumed we should allow blank tag inputs. I rejected this and added a Pydantic `@field_validator` in `app/main.py` to strip duplicate commas and outer whitespace (e.g., converting `" ui , , bug "` to `"ui,bug"`).

2. **As a team lead**, I want to filter the board by a specific status, so that I can see only the tasks related to a specific stage of development.
   - **Acceptance Criteria**: Sending a `GET /api/tasks/?status=InProgress` request returns only the tasks in that status state.
   - **AI Assumption Corrected**: The AI assumed we needed to return all tasks in one block and filter only on the UI. I corrected it to add an optional `status` query parameter on the backend to enforce correct workspace state requests.

## Feature 2: Search and Combined Filters
3. **As a project manager**, I want to search for tasks using a search bar on the Kanban board, so that I can find a specific task without scrolling through columns.
   - **Acceptance Criteria**: Entering a search term matches the term case-insensitively across the task title to update the displayed cards dynamically.
   - **AI Assumption Corrected**: The AI initially suggested building heavy, server-side database lookups for standard single-user search. I refactored this into a highly responsive, lightweight frontend search filter that scans titles instantly, keeping backend operations lean.

4. **As a Kanban user**, I want to view my cards organized with clear column separation and see assignee assignments at a glance, so that I can manage my team's workload effectively.
   - **Acceptance Criteria**: Columns are separated visually with a distinct gap layout, and every task card cleanly displays its assignee's name along with a custom initials avatar.
   - **AI Assumption Corrected**: The AI's initial UI layout bunched columns together without visual breathing room and lacked an assignee field on the card view. I refined the HTML grid spacing and injected dynamic JS string methods to generate clean, circular initials-badges for assignees on every card.