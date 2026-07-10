# User Stories

## Feature 1: Task workflow and status updates
1. As a project lead, I want to move a task from To Do to Done, so that I can reflect progress in the board.
   - Acceptance criteria: a task can be updated through the API, the status changes in storage, and the updated value is returned in the response.
   - AI assumption corrected: I initially assumed the frontend would only read tasks, but the board also needs a writable update route.

2. As a team member, I want to filter tasks by their current status, so that I can focus on the work that matters right now.
   - Acceptance criteria: calling GET /tasks/ with a status query returns only tasks matching that status.
   - AI assumption corrected: I corrected the assumption that status filter support already existed in the router.

## Feature 2: Search, priority, and overdue filtering
3. As a product owner, I want to search tasks by keyword, so that I can find relevant work quickly.
   - Acceptance criteria: a search term matches task titles or tags case-insensitively and returns only matching tasks.
   - AI assumption corrected: I corrected the plan to search title-only and expanded it to title and tags.

4. As a manager, I want to filter tasks by priority and overdue date, so that I can identify urgent work.
   - Acceptance criteria: GET /tasks/ accepts priority_filter and overdue_only parameters and returns the expected subset.
   - AI assumption corrected: I corrected the earlier assumption that the UI only needed a simple search bar and not backend support for the board filters.

5. As a user, I want to create tasks with tags and due dates, so that I can keep context and deadlines in one place.
   - Acceptance criteria: task creation accepts tags and due_date fields, and the values are persisted correctly.
   - AI assumption corrected: I corrected the assumption that tags were purely cosmetic and not part of the data contract.