# Release Evidence

## Baseline

- **Branch:** final-project
- **Date:** 2026-07-24
- **Local app run command:** `uvicorn app.main:app --reload`
- **/health result:**

curl.exe http://127.0.0.1:8000/health
{"status":"ok"}

- **Frontend check:** Opened `http://127.0.0.1:8000` in the browser. The Kanban board loads with existing tasks visible across the To Do / In Progress / Done columns (tag chips render correctly, e.g. `FE`, `bug`). Clicking "+ Add New Task" opens the create-task modal and successfully adds a new task to the board.
- **Test command:** `pytest -v`
- **Test result:**

===================================================================================== test session starts =====================================================================================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\sghobar\AppData\Local\Programs\Python\Python312\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\sghobar\OneDrive - S.M.L.C. (Societe Moderne Libanaise pour le Commerce S.A.L.)\Desktop\TaskTracker
plugins: anyio-4.14.1, cov-7.1.0
collected 21 items

tests/test_tasks.py::test_create_task_basic PASSED [ 4%]
tests/test_tasks.py::test_reject_empty_title PASSED [ 9%]
tests/test_tasks.py::test_get_single_task_and_not_found PASSED [ 14%]
tests/test_tasks.py::test_delete_task PASSED [ 19%]
tests/test_tasks.py::test_create_task_with_tags PASSED [ 23%]
tests/test_tasks.py::test_reject_empty_tag PASSED [ 28%]
tests/test_tasks.py::test_update_task_tags PASSED [ 33%]
tests/test_tasks.py::test_filter_by_tag PASSED [ 38%]
tests/test_tasks.py::test_preserve_tags_after_unrelated_update PASSED [ 42%]
tests/test_tasks.py::test_search_title_and_description PASSED [ 47%]
tests/test_tasks.py::test_combine_status_and_priority PASSED [ 52%]
tests/test_tasks.py::test_search_no_matches_returns_empty_list PASSED [ 57%]
tests/test_tasks.py::test_invalid_status_filter_returns_400 PASSED [ 61%]
tests/test_tasks.py::test_invalid_priority_filter_returns_400 PASSED [ 66%]
tests/test_tasks.py::test_invalid_status_transition_via_patch PASSED [ 71%]
tests/test_tasks.py::test_patch_status_rejects_skipped_transition PASSED [ 76%]
tests/test_tasks.py::test_health_check_endpoint PASSED [ 80%]
tests/test_tasks.py::test_same_status_is_valid PASSED [ 85%]
tests/test_tasks.py::test_allowed_status_transitions PASSED [ 90%]
tests/test_tasks.py::test_invalid_current_status_raises_400 PASSED [ 95%]
tests/test_tasks.py::test_disallowed_transition_raises_400 PASSED [100%]

=============================================================================== 21 passed, 2 warnings in 0.42s ================================================================================

- **Notes on this baseline:** `Frontend/` was renamed to `frontend/` (lowercase) for consistency with the required repository structure and to avoid case-sensitivity issues in CI/Docker (Linux is case-sensitive; Windows is not). `app/main.py`'s `FileResponse("Frontend/index.html")` was updated to `FileResponse("frontend/index.html")` to match. This is a documentation-supported path correction, not a new feature -- re-running the full test suite and the manual frontend check above confirms nothing broke as a result.

## CI evidence
- Workflow file:
- Latest run link or note:
- Test command used by CI:
- Shortcut check: no continue-on-error / no || true / pytest is not skipped.

## Docker evidence
- Build command:
- Run command:
- /health check:
- Non-root check, if implemented:
- No-baked-secrets check:

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
