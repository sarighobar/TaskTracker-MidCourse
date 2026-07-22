$content = @'
# Verification & Testing Report

This document records the verification strategy, manual browser tests, automated test suite execution, behavior contracts, and break test evidence for the **TaskTracker** application.

---

## 1. Baseline Check

Before implementing the tags and search refactor, the initial codebase state was verified as follows:

* **Pre-Refactor Architecture**: Simple FastAPI backend with in-memory `tasks_db` list and static HTML frontend.
* **Initial Endpoints**: CRUD operations for `/api/tasks/` supporting only basic `status` filtering.
* **Pre-Refactor Test Baseline**: Basic test suite passing 4 core CRUD tests (`test_create_task_basic`, `test_reject_empty_title`, `test_get_single_task_and_not_found`, `test_delete_task`).
* **Known Pre-Refactor Gaps**: Search parameters were ignored by backend, tag input was missing from frontend modal, tag chips were not rendered on cards, and invalid `status`/`priority` filter values were silently ignored rather than rejected.

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
| **MB-07** | Invalid Filter Value | Manually navigate to `/api/tasks/?status=NotAStatus`. | API returns `400 Bad Request` instead of an empty board with no explanation. | **PASS** |

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
| 6. Invalid Filters    -> ?status= or ?priority= with an unrecognized value returns    |
|                         HTTP 400 with an explicit detail message                       |
| 7. Status Transitions -> PATCH /{id}/status enforces the transition matrix in         |
|                         business_rules.py (e.g. ToDo -> Done directly is rejected)      |
+---------------------------------------------------------------------------------------+
```

---

## 4. Full Test Suite Result

Command run: `pytest -v`

```text
pytest -v
============================================================================================= test session starts ==============================================================================================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\sghobar\AppData\Local\Programs\Python\Python312\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\sghobar\OneDrive - S.M.L.C. (Societe Moderne Libanaise pour le Commerce S.A.L.)\Desktop\TaskTracker
plugins: anyio-4.14.1, cov-7.1.0
collected 21 items

tests/test_tasks.py::test_create_task_basic PASSED                                                                                                                                                        [  4%]
tests/test_tasks.py::test_reject_empty_title PASSED                                                                                                                                                       [  9%]
tests/test_tasks.py::test_get_single_task_and_not_found PASSED                                                                                                                                            [ 14%]
tests/test_tasks.py::test_delete_task PASSED                                                                                                                                                              [ 19%]
tests/test_tasks.py::test_create_task_with_tags PASSED                                                                                                                                                    [ 23%]
tests/test_tasks.py::test_reject_empty_tag PASSED                                                                                                                                                         [ 28%]
tests/test_tasks.py::test_update_task_tags PASSED                                                                                                                                                         [ 33%]
tests/test_tasks.py::test_filter_by_tag PASSED                                                                                                                                                            [ 38%]
tests/test_tasks.py::test_preserve_tags_after_unrelated_update PASSED                                                                                                                                     [ 42%]
tests/test_tasks.py::test_search_title_and_description PASSED                                                                                                                                             [ 47%]
tests/test_tasks.py::test_combine_status_and_priority PASSED                                                                                                                                              [ 52%]
tests/test_tasks.py::test_search_no_matches_returns_empty_list PASSED                                                                                                                                     [ 57%]
tests/test_tasks.py::test_invalid_status_filter_returns_400 PASSED                                                                                                                                        [ 61%]
tests/test_tasks.py::test_invalid_priority_filter_returns_400 PASSED                                                                                                                                      [ 66%]
tests/test_tasks.py::test_invalid_status_transition_via_patch PASSED                                                                                                                                      [ 71%]
tests/test_tasks.py::test_patch_status_rejects_skipped_transition PASSED                                                                                                                                  [ 76%]
tests/test_tasks.py::test_health_check_endpoint PASSED                                                                                                                                                    [ 80%]
tests/test_tasks.py::test_same_status_is_valid PASSED                                                                                                                                                     [ 85%]
tests/test_tasks.py::test_allowed_status_transitions PASSED                                                                                                                                               [ 90%]
tests/test_tasks.py::test_invalid_current_status_raises_400 PASSED                                                                                                                                        [ 95%]
tests/test_tasks.py::test_disallowed_transition_raises_400 PASSED                                                                                                                                         [100%]

=============================================================================================== warnings summary ===============================================================================================
..\..\..\AppData\Local\Programs\Python\Python312\Lib\site-packages\fastapi\testclient.py:1
  C:\Users\sghobar\AppData\Local\Programs\Python\Python312\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

app\database.py:12
  C:\Users\sghobar\OneDrive - S.M.L.C. (Societe Moderne Libanaise pour le Commerce S.A.L.)\Desktop\TaskTracker\app\database.py:12: MovedIn20Warning: The ``declarative_base()`` function is now available as sqlalchemy.orm.declarative_base(). (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)
    Base = declarative_base()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================================================================================== 21 passed, 2 warnings in 0.41s ========================================================================================
```

---

## 5. Break Test Evidence

Genuine break-test cycles: each test was confirmed passing, the underlying code was deliberately broken, the test was re-run to confirm it caught the break, the code was restored, and the test was re-run a final time to confirm it passed again.

### BT-01: Tag sanitization (`test_reject_empty_tag`)

**File changed:** `app/routers.py`, inside `create_task()`

**Line changed:**
```python
# Original:
tags_list = [t.strip() for t in raw_tags.split(",") if t.strip()]
# Broken (removes the empty-string filter):
tags_list = [t.strip() for t in raw_tags.split(",")]
```

**Step 1 - Confirm passing (before break):**
```text
pytest -v -k test_reject_empty_tag
===================================================================================== test session starts =====================================================================================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\sghobar\AppData\Local\Programs\Python\Python312\python.exe
collected 21 items / 20 deselected / 1 selected

tests/test_tasks.py::test_reject_empty_tag PASSED                                                                                                                                        [100%]

================================================================================= 1 passed, 20 deselected, 2 warnings in 0.21s =================================================================================
```

**Step 2 - Break the code, re-run:**
```text
pytest -v -k test_reject_empty_tag
============================================================================================= test session starts ==============================================================================================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\sghobar\AppData\Local\Programs\Python\Python312\python.exe
collected 21 items / 20 deselected / 1 selected

tests/test_tasks.py::test_reject_empty_tag FAILED                                                                                                                                                         [100%]

=================================================================================================== FAILURES ===================================================================================================
____________________________________________________________________________________________ test_reject_empty_tag _____________________________________________________________________________________________

client = <starlette.testclient.TestClient object at 0x000002DF24B6BCB0>

    def test_reject_empty_tag(client):
        response = client.post("/api/tasks/", json={
            "title": "Clean Database",
            "tags": "   ,  , backend , , "
        })
        assert response.status_code == 201
>       assert response.json()["tags"] == "backend"
E       AssertionError: assert ',,backend,,' == 'backend'
E
E         - backend
E         + ,,backend,,
E         ? ++       ++

tests\test_tasks.py:72: AssertionError
=========================================================================================== short test summary info ============================================================================================
FAILED tests/test_tasks.py::test_reject_empty_tag - AssertionError: assert ',,backend,,' == 'backend'
================================================================================= 1 failed, 20 deselected, 2 warnings in 0.17s =================================================================================
```

**Step 3 - Restore the code, re-run to confirm recovery:**
```text
pytest -v -k test_reject_empty_tag
============================================================================================= test session starts ==============================================================================================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\sghobar\AppData\Local\Programs\Python\Python312\python.exe
collected 21 items / 20 deselected / 1 selected

tests/test_tasks.py::test_reject_empty_tag PASSED                                                                                                                                                         [100%]

================================================================================= 1 passed, 20 deselected, 2 warnings in 0.04s =================================================================================
```

**What this proves:** the test genuinely exercises the tag-sanitization logic. Removing the `if t.strip()` filter let blank tokens from `"   ,  , backend , , "` survive into the stored value, producing `,,backend,,` instead of `backend` -- the exact AssertionError above (`assert ',,backend,,' == 'backend'`) demonstrates the test correctly catching a real regression, not just always passing.

---

### BT-02: Invalid status filter validation (`test_invalid_status_filter_returns_400`)

**File changed:** `app/routers.py`, inside `get_tasks()`

**Lines changed:**
```python
# Original:
if status is not None and status not in VALID_STATUSES:
    raise HTTPException(status_code=400, detail=f"Invalid status: '{status}'")
# Broken (commented out):
# if status is not None and status not in VALID_STATUSES:
#     raise HTTPException(status_code=400, detail=f"Invalid status: '{status}'")
```

**Step 1 - Confirm passing (before break):**
```text
pytest -v -k test_invalid_status_filter_returns_400
============================================================================================= test session starts ==============================================================================================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\sghobar\AppData\Local\Programs\Python\Python312\python.exe
collected 21 items / 20 deselected / 1 selected

tests/test_tasks.py::test_invalid_status_filter_returns_400 PASSED                                                                                                                                        [100%]

================================================================================= 1 passed, 20 deselected, 2 warnings in 0.06s =================================================================================
```

**Step 2 - Break the code, re-run:**
```text
pytest -v -k test_invalid_status_filter_returns_400
============================================================================================= test session starts ==============================================================================================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\sghobar\AppData\Local\Programs\Python\Python312\python.exe
collected 21 items / 20 deselected / 1 selected

tests/test_tasks.py::test_invalid_status_filter_returns_400 FAILED                                                                                                                                        [100%]

=================================================================================================== FAILURES ===================================================================================================
____________________________________________________________________________________ test_invalid_status_filter_returns_400 ____________________________________________________________________________________

client = <starlette.testclient.TestClient object at 0x00000163BD533A10>

    def test_invalid_status_filter_returns_400(client):
        """US-2.4: GET /api/tasks/?status=<invalid> must be rejected, not silently return []."""
        res = client.get("/api/tasks/?status=NotAStatus")
>       assert res.status_code == 400
E       assert 200 == 400
E        +  where 200 = <Response [200 OK]>.status_code

tests\test_tasks.py:155: AssertionError
=========================================================================================== short test summary info ============================================================================================
FAILED tests/test_tasks.py::test_invalid_status_filter_returns_400 - assert 200 == 400
================================================================================= 1 failed, 20 deselected, 2 warnings in 0.13s =================================================================================
```

**Step 3 - Restore the code, re-run to confirm recovery:**
```text
pytest -v -k test_invalid_status_filter_returns_400
============================================================================================= test session starts ==============================================================================================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\sghobar\AppData\Local\Programs\Python\Python312\python.exe
collected 21 items / 20 deselected / 1 selected

tests/test_tasks.py::test_invalid_status_filter_returns_400 PASSED                                                                                                                                        [100%]

================================================================================= 1 passed, 20 deselected, 2 warnings in 0.16s =================================================================================
```

**What this proves:** the test genuinely exercises the status-filter validation. With the validation check commented out, `GET /api/tasks/?status=NotAStatus` silently fell through to a `200 OK` instead of the required `400 Bad Request` -- the exact AssertionError above (`assert 200 == 400`) demonstrates the test correctly catching a real regression, not just always passing.
'@
Set-Content -Path "docs\midcourse\verification.md" -Value $content -Encoding utf8