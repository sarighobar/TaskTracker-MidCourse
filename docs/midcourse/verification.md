# Verification

## Baseline
- Before the final refactor, the app loaded the UI page but task creation failed because the frontend was calling a mismatched endpoint and the backend did not yet support the board’s update/filter behavior.

## Backend test results
- Command executed: `python -m pytest -q`
- Result: 11 passed, 2 warnings
- Key tests covered:
  - task creation with tags
  - tag whitespace normalization
  - search by title and tag
  - root page delivery
  - task status updates
  - priority and overdue filtering

## Manual browser checks
- Opened `http://127.0.0.1:8000/` and confirmed the Task Tracker workspace loaded.
- Created a task through the UI and verified it appeared in the board after refresh.
- Used the search, priority, and overdue filters to confirm the task list changed as expected.

## Behavior contract before and after
- Before: the UI could not reliably save tasks through the API and the backend lacked support for status updates and overdue filtering.
- After: the UI can create, list, filter, and update tasks through the FastAPI backend.

## Break test evidence
- A break test was performed by sending an unsupported or empty search term. The list returned no matches while the board structure remained intact.
- A second break test was performed by updating a task to Done and confirming the API returned the updated status value.