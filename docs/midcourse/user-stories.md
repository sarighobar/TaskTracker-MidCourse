# User Stories

## Feature 1: Tags and Labels (Category Tracking)
1. **As a developer**, I want to add tags (e.g., "bug", "frontend") to a task when creating it, so that I can categorize and group my work.
   - **Acceptance Criteria**: The `POST /tasks` payload accepts a `tags` string. The backend parses, trims whitespace, filters empty strings, and stores them as a clean, comma-separated string.
   - **AI Assumption Corrected**: The AI assumed we should allow blank tag inputs. I rejected this and added a Pydantic `@field_validator` to strip duplicate commas and outer whitespace (e.g., converting `" ui , , bug "` to `"ui,bug"`).

2. **As a team lead**, I want to filter the board by a specific tag using a query parameter, so that I can see only the tasks related to a specific feature or domain.
   - **Acceptance Criteria**: Sending a `GET /tasks?tag=bug` request returns only the tasks where "bug" is present in the database `tags` column.
   - **AI Assumption Corrected**: The AI assumed we needed a complex relational many-to-many junction table, but I corrected it to use a clean SQLite `LIKE` filter on a comma-separated string column for simplicity.

## Feature 2: Search and Combined Filters
3. **As a project manager**, I want to search for tasks using a search bar, so that I can find a specific task without scrolling through columns.
   - **Acceptance Criteria**: Sending a `GET /tasks?search=database` matches the term "database" case-insensitively across both the task `title` and `description` columns.
   - **AI Assumption Corrected**: The AI's initial search query only filtered by task title. I refined this to search both `title` and `description` to prevent missing relevant items.

4. **As a Kanban user**, I want my search filters and tag filters to combine dynamically, so that I can narrow down my search to highly specific tasks.
   - **Acceptance Criteria**: Performing `GET /tasks?search=auth&tag=security` successfully applies both database query constraints.
   - **AI Assumption Corrected**: The AI wrote separate endpoints for searching vs. tag filtering. I refactored them into a single, unified `GET /tasks` endpoint with multiple optional query parameters.