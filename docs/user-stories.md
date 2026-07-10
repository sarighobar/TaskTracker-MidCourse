# User Stories

## Feature 1: Status updates and workflow control
1. As a project lead, I want to move a task from To Do to Done, so that progress is visible on the board.
   - Acceptance criteria: the API accepts a partial update, stores the new status, and returns the updated task.
   - AI assumption corrected: the frontend was assumed to be read-only, but it also needed a writable update route.

2. As a team member, I want to filter tasks by workflow status, so that I can focus on the right column.
   - Acceptance criteria: GET /tasks/ with the status query returns only matching tasks.
   - AI assumption corrected: status filtering was not available in the router and had to be added explicitly.

## Feature 2: Search, priority, and overdue filtering
3. As a product owner, I want to search tasks by keyword, so that I can find relevant work quickly.
   - Acceptance criteria: search matches task title and tags case-insensitively and returns the matching subset.
   - AI assumption corrected: search was expanded beyond title-only matching.

4. As a manager, I want to filter tasks by priority and overdue date, so that urgent work can be identified quickly.
   - Acceptance criteria: GET /tasks/ accepts priority_filter and overdue_only parameters and returns the correct subset.
   - AI assumption corrected: the backend needed explicit support for the UI filters rather than only a simple search box.

5. As a user, I want task creation to persist tags and due dates, so that context and deadlines stay together.
   - Acceptance criteria: create requests accept tags and due_date values and persist them.
   - AI assumption corrected: tags were treated as cosmetic, but they needed to be part of the data contract.
