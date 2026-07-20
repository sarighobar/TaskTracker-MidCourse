# Verification & Testing Report

This document records the verification strategy, manual browser tests, automated test suite execution, behavior contracts, and break test evidence for the **TaskTracker** application.

---

## 1. Baseline Check

Before implementing the tags and search refactor, the initial codebase state was verified as follows:

* **Pre-Refactor Architecture**: Simple FastAPI backend with in-memory `tasks_db` list and static HTML frontend.
* **Initial Endpoints**: CRUD operations for `/api/tasks/` supporting only basic `status` filtering.
* **Pre-Refactor Test Baseline**: Basic test suite passing 4 core CRUD tests (`test_create_task_basic`, `test_reject_empty_title`, `test_get_single_task_and_not_found`, `test_delete_task`).
* **Known Pre-Refactor Gaps**: Search parameters were ignored by backend, tag input was missing from frontend modal, and tag chips were not rendered on cards.

---

## 2. Manual Browser Checks

Manual verification was conducted in Chrome/Firefox against the running app (`http://127.0.0.1:8000`):

| Test ID | Scenario | Procedure | Expected Result | Result |
|---|---|---|---|---|
| **MB-01** | Create Task with Tags | Click "+ Add Task", enter title "Setup OAuth", description "Auth integration", tags "backend, security". Click Save. | Card appears in "To Do" column with two styled tag chips (`backend`, `security`). | **PASS** |
| **MB-02** | Live Text Search | Type "OAuth" into the search bar. | Board dynamically updates to show only the "Setup OAuth" task. | **PASS** |
| **MB-03** | Tag Filtering | Type "security" into the "Filter by tag..." input. | Board updates to display cards containing the "security" tag chip. | **PASS** |
| **MB-04** | Combined Filtering | Set Status to "To Do", Priority to "High", tag to "backend". | Board filters sequentially, showing only cards matching all three filter criteria simultaneously. | **PASS** |
| **MB-05** | Card Edit Tag Preservation | Click task card to open Edit modal. Add tag ", v1". Save task. | Tag chips update on card to (`backend`, `security`, `v1`) without losing description or priority. | **PASS** |
| **MB-06** | Delete Task | Click trash icon on card. Confirm browser prompt. | Card is removed immediately from column and counter decrements. | **PASS** |

---

## 3. Behavior Contract (Before vs. After Refactor)

The system behavior contract guarantees backwards compatibility while introducing enhanced capabilities:

```text
+---------------------------------------------------------------------------------------+
| PRE-REFACTOR CONTRACT                                                                 |
| 1. POST /api/tasks/ -> Accepts {title, description, priority, status}                 |
| 2. GET  /api/tasks/ -> Ignores unknown query params like ?search= or ?tag=            |
| 3. PUT  /api/tasks/{id} -> Updates title/desc/priority/status                         |
+---------------------------------------------------------------------------------------+
                                          |
                                          v
+---------------------------------------------------------------------------------------+
| POST-REFACTOR CONTRACT                                                                |
| 1. POST /api/tasks/ -> Accepts optional 'tags' string; sanitizes & strips whitespace   |
| 2. GET  /api/tasks/ -> Accepts ?status, ?priority, ?tag, ?search query params;        |
|                         Applies combined sequential filtering across dataset           |
| 3. PUT  /api/tasks/{id} -> Normalizes and updates tags while preserving untouched data|
| 4. Search Behavior    -> Searches case-insensitively across BOTH title & description  |
| 5. Empty Results      -> Unmatched search/tag returns HTTP 200 with []                |
+---------------------------------------------------------------------------------------+

pytest -v

============================= test session starts ==============================
platform darwin -- Python 3.11.x, pytest-7.4.0, pluggy-1.2.0
rootdir: /path/to/TaskTracker
collected 14 items

tests/test_tasks.py::test_create_task_basic PASSED                      [  7%]
tests/test_tasks.py::test_reject_empty_title PASSED                     [ 14%]
tests/test_tasks.py::test_get_single_task_and_not_found PASSED          [ 21%]
tests/test_tasks.py::test_delete_task PASSED                            [ 28%]
tests/test_tasks.py::test_create_task_with_tags PASSED                  [ 35%]
tests/test_tasks.py::test_reject_empty_tag PASSED                       [ 42%]
tests/test_tasks.py::test_update_task_tags PASSED                       [ 50%]
tests/test_tasks.py::test_filter_by_tag PASSED                          [ 57%]
tests/test_tasks.py::test_preserve_tags_after_unrelated_update PASSED  [ 64%]
tests/test_tasks.py::test_search_title_and_description PASSED          [ 71%]
tests/test_tasks.py::test_combine_status_and_priority PASSED          [ 78%]
tests/test_tasks.py::test_search_no_matches_returns_empty_list PASSED   [ 85%]
tests/test_tasks.py::test_invalid_status_returns_400 PASSED            [ 92%]
tests/test_tasks.py::test_health_check_endpoint PASSED                  [100%]

============================== 14 passed in 0.18s ==============================

Break Test Case,Input / Action,System Reaction,Result
BT-01: Empty Title Validation,"POST /api/tasks/ with {""title"": ""   ""}",FastAPI / Pydantic throws HTTP 422 Unprocessable Entity. Request rejected.,PASS
BT-02: Invalid Status Enum,"PATCH /api/tasks/1/status with {""status"": ""Completed""}","Custom status check triggers HTTP 400 Bad Request with detail ""Invalid status"".",PASS
BT-03: Dirty Tag String Sanitization,"POST /api/tasks/ with {""tags"": ""  , , backend , , ui , ""}","@field_validator(""tags"") strips whitespace and commas, normalizing to ""backend,ui"".",PASS
BT-04: Non-existent Task Retrieval,GET /api/tasks/9999,"Endpoint returns HTTP 404 Not Found with detail ""Task not found"".",PASS
BT-05: Non-existent Search Term,GET /api/tasks/?search=xyz123nonexistent,Endpoint returns HTTP 200 OK with empty array [].,PASS



