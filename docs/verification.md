# Verification

## Baseline
- Before the final refactor, the app served the UI but task creation and task update/filter behavior were inconsistent with what the board expected.

## Backend test results
- Command executed: python -m pytest -q
- Result: 11 passed, 2 warnings
- Covered behavior includes task creation with tags, tag normalization, title/tag search, root-page delivery, status updates, and priority/overdue filtering.

## Manual browser checks
- Opened http://127.0.0.1:8000/ and confirmed the Kanban workspace loaded.
- Created a task through the form and confirmed the new task was persisted.
- Used the search, priority, and overdue filters to confirm the board changed as expected.

## Behavior contract before and after
- Before: the UI and backend were not aligned for task updates and filtering.
- After: the UI can create, list, filter, and update tasks through the FastAPI backend.

## Break test evidence
- Break test 1: a search term that should match nothing returned an empty list without breaking the board layout.
- Break test 2: updating a task to Done returned the new status value through the API.
