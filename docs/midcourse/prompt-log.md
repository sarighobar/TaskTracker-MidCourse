# AI Prompt Log & Workflow Evidence

This document tracks key AI interactions during the implementation of **Task Categorization (Tags)** and **Search & Combined Filtering**.

---

## Weak Prompt vs. Strong Prompt Refactoring

To demonstrate effective AI prompting techniques, an initial weak/unconstrained prompt was refactored into a structured, highly effective prompt.

### 🔴 Original (Weak Prompt)
> "Add search and filtering to my tasks api."

* **Why it failed / produced poor results:**
  * Unclear scope: Didn't specify which fields to search (title, description, or both).
  * Lacked constraints: Didn't specify the framework (FastAPI/SQLAlchemy) or query parameter structure.
  * Result: The AI attempted to rewrite the entire router, created unnecessary endpoint paths (`/api/tasks/search`), and broke existing pagination/response schema.

### 🟢 Rewritten (Strong Prompt)
> "Modify the existing `GET /api/tasks/` endpoint in FastAPI using SQLAlchemy. Extend the endpoint query parameters to accept optional `status`, `priority`, `tag`, and `search` arguments.
> - If `search` is provided, perform a case-insensitive substring search across BOTH `models.Task.title` AND `models.Task.description` using an SQL OR condition.
> - Combine all active filters using SQL AND logic.
> - Return a `200 OK` with an empty array `[]` if no tasks match.
> - Do not change the existing task response schema."

* **Why it succeeded:**
  * Clear scope: Defined exact fields, logic (`OR` vs `AND`), and target endpoint.
  * Explicit constraints: Specified FastAPI, SQLAlchemy `.ilike()`, status code `200`, and response array structure.
  * Preserved integrity: Ensured existing response contracts were untouched.

---

## Feature 1: Task Categorization with Tags

### Prompt 1.1: Backend Data Model & Normalization Logic
* **Prompt:**
  > "I need to add a `tags` field to my Task model in FastAPI with SQLAlchemy and SQLite. Store tags as a comma-separated string on the Task table. Write a helper function in Pydantic/routers that takes raw tag input like `' frontend, bug, , urgent '`, strips whitespace, removes empty values, and normalizes it to `'frontend,bug,urgent'`."
* **AI Output:**
  * Suggested adding `tags = Column(String, nullable=True, default="")` to `models.py`.
  * Provided a string cleaning snippet using python list comprehension: `",".join([t.strip() for t in raw.split(",") if t.strip()])`.
* **Decision & Action:**
  * **ACCEPTED:** The string cleaning logic was clean, idiomatic, and handled edge cases like multiple empty commas (`" , , "`).
  * **EDITED:** Ensured `default=""` was set on the model so database queries return empty strings instead of `None` for un-tagged tasks.

---

### Prompt 1.2: Tag Filtering in Router
* **Prompt:**
  > "Update the `GET /api/tasks/` endpoint in `app/routers.py` to accept an optional `tag: Optional[str] = None` query parameter. Use SQLAlchemy `.ilike()` to match tasks whose `tags` column contains the tag parameter."
* **AI Output:**
  ```python
  if tag:
      tag_lower = f"%{tag.lower()}%"
      query = query.filter(models.Task.tags.ilike(tag_lower))
  ```
* **Decision & Action:**
  * **ACCEPTED:** The `.ilike()` substring match handled case-insensitivity correctly and needed no edits.

---

### Prompt 1.3: Tag Storage Architecture
* **Prompt:**
  > "What's the best way to model tags for a task in a relational database, given I want to support filtering tasks by a single tag?"
* **AI Output:**
  * The AI recommended a normalized Many-to-Many schema: a `Tag` table, a `TaskTag` junction table, and SQLAlchemy `relationship()` mappings, arguing it would prevent duplicate/misspelled tag strings and support future tag-management features.
* **Decision & Action:**
  * **REJECTED:** For a single-user prototype with a small, static dataset, a junction table added migration overhead, join complexity, and extra CRUD endpoints (create/rename/delete tag) that were out of scope for this sprint.
  * **ACTION TAKEN:** Kept tags as a single normalized comma-separated string column on `Task`, validated by the trimming/dedup logic from Prompt 1.1, and filtered with `.ilike()` substring matching (Prompt 1.2) instead of a join. This decision is also recorded in `mini-adr.md`.

---

## Feature 2: Search & Combined Filtering

### Prompt 2.1: Weak → Strong Prompt Rewrite
* See the **Weak Prompt vs. Strong Prompt Refactoring** section above — this rewrite was the first prompt used to scope Feature 2 and is the one that produced the working `GET /api/tasks/` implementation with `status`, `priority`, `tag`, and `search` combined with `AND` logic.

---

### Prompt 2.2: Combining Filters with AND Logic
* **Prompt:**
  > "Given the `GET /api/tasks/` endpoint with `status`, `priority`, `tag`, and `search` as optional query parameters, confirm that when multiple parameters are supplied together, SQLAlchemy applies them as a combined AND condition rather than OR, and show the query-building pattern."
* **AI Output:**
  * Confirmed that chaining multiple `.filter()` calls on a SQLAlchemy `Query` object combines conditions with `AND` by default, and demonstrated the incremental `query = query.filter(...)` pattern used in `routers.py`.
* **Decision & Action:**
  * **ACCEPTED:** This confirmed the existing incremental-filter pattern was correct and required no structural changes — each `if` block reassigns `query` with an additional `AND`-ed filter.

---

### Prompt 2.3: Validating Filter Input Values
* **Prompt:**
  > "In FastAPI, if a client passes `?status=NotARealStatus` to `GET /api/tasks/`, my current code just filters and silently returns an empty list. I want it to instead return `400 Bad Request` with a message naming the invalid value, for both `status` and `priority`. Show the validation check to add at the top of the route, before the query is built."
* **AI Output:**
  * Suggested defining `VALID_STATUSES` and `VALID_PRIORITIES` sets and raising `HTTPException(status_code=400, detail=...)` early in `get_tasks()` if the supplied value isn't a member of the corresponding set.
* **Decision & Action:**
  * **ACCEPTED:** Added the validation exactly as suggested. This closed a gap identified during manual review (US-2.4 in `user-stories.md` had described this behavior, but the backend didn't actually enforce it) and is covered by `test_invalid_status_filter_returns_400` and `test_invalid_priority_filter_returns_400` in `test_tasks.py`.
