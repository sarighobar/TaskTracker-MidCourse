# AI Prompt Log & Pair Programming Record

This log records key interactions with AI tools during the development of the **TaskTracker** application. In accordance with project guidelines, it documents at least 3 meaningful prompts per feature, highlighting human review, corrections, and architectural decisions.

---

## Feature 1: Tags / Labels

### Prompt 1.1: Data Schema & Tag Validation
* **Date**: June 2026
* **Tool**: ChatGPT / Claude AI
* **User Prompt**:
  > "How should I implement a tags feature in my FastAPI and Pydantic task model? Provide the Pydantic schema and validation for handling comma-separated tags."
* **AI Output Summary**:
  > Suggested creating a relational `Tag` model with a Many-to-Many junction table. For Pydantic, it provided a basic list validator that allowed blank strings inside tag lists.
* **Human Review & Critique**:
  > The junction table was massive over-engineering for an in-memory prototype. Additionally, accepting blank strings (e.g. `"tag1, , tag2"`) breaks data hygiene.
* **Action Taken**:
  > Rejected the relational database approach. Instructed AI to simplify to a single comma-separated string field (`tags: Optional[str] = ""`) and wrote a custom `@field_validator("tags")` that strips whitespace and filters out empty values.

---

### Prompt 1.2: UI Tag Input & Card Badge Rendering
* **Date**: June 2026
* **Tool**: ChatGPT / Claude AI
* **User Prompt**:
  > "Provide HTML/CSS and vanilla JS code to add a tags input to a modal and render tag chips on Kanban cards."
* **AI Output Summary**:
  > Generated basic CSS `.tag-chip` styling and JavaScript card rendering logic using `task.tags.split(',')`.
* **Human Review & Critique**:
  > The JS code assumed `task.tags` was always a valid string. When a task had no tags (`null` or `""`), `.split(',')` threw a `TypeError` in the browser console.
* **Action Taken**:
  > Refactored the card rendering JS to check if `task.tags` exists before splitting, and applied `.trim()` to each tag element to ensure clean badge display.

---

### Prompt 1.3: Tag Filtering Endpoint & Automated Tests
* **Date**: July 2026
* **Tool**: ChatGPT / Claude AI
* **User Prompt**:
  > "Write a FastAPI endpoint parameter to filter tasks by tag and write pytest unit tests covering create with tags, empty tag normalization, tag update, tag filter, and preserving tags after status update."
* **AI Output Summary**:
  > Provided `tag: Optional[str] = None` query parameter logic in FastAPI and drafted 3 basic pytest functions.
* **Human Review & Critique**:
  > The initial pytest draft omitted the `test_preserve_tags_after_unrelated_update` test and didn't test normalization of trailing spaces during creation.
* **Action Taken**:
  > Expanded the test suite in `tests/test_tasks.py` to cover all 5 tag test cases requested by the brief.

---

## Feature 2: Search + Combined Filters

### Prompt 2.1: Multi-Column Search Query Logic
* **Date**: June 2026
* **Tool**: ChatGPT / Claude AI
* **User Prompt**:
  > "How do I implement a search parameter in FastAPI that searches across both task titles and task descriptions?"
* **AI Output Summary**:
  > Provided a list comprehension in FastAPI: `[t for t in tasks if search in t["title"]]`.
* **Human Review & Critique**:
  > The AI's code only checked the `title` field (ignoring `description`) and was case-sensitive, meaning searching "auth" would miss "Auth".
* **Action Taken**:
  > Modified the logic in `app/main.py` to convert query strings to lowercase and check both `title` and `description` (`search_lower in t["title"].lower() or search_lower in t["description"].lower()`).

---

### Prompt 2.2: Combining Multiple Query Parameters
* **Date**: July 2026
* **Tool**: ChatGPT / Claude AI
* **User Prompt**:
  > "How can I combine search, status, priority, and tag filters into a single GET /api/tasks/ endpoint in FastAPI?"
* **AI Output Summary**:
  > Suggested using separate route endpoints like `/api/tasks/status/{status}` and `/api/tasks/search/{query}`.
* **Human Review & Critique**:
  > Creating separate endpoints makes combining filters (e.g. `status=ToDo` AND `priority=High` AND `search=bug`) impossible in a clean RESTful manner.
* **Action Taken**:
  > Defined optional query parameters on a single `GET /api/tasks/` route: `status`, `priority`, `tag`, and `search`. Chain-filtered the results array sequentially for all active parameters.

---

### Prompt 2.3: Comprehensive Search and Filter Unit Tests
* **Date**: July 2026
* **Tool**: ChatGPT / Claude AI
* **User Prompt**:
  > "Write pytest cases for multi-column search, combining status and priority, empty result list on no match (HTTP 200 with []), and invalid filter inputs returning HTTP 400."
* **AI Output Summary**:
  > Generated test functions using `TestClient(app)`.
* **Human Review & Critique**:
  > The generated test for invalid filter inputs expected a 422 error on a status patch instead of verifying the custom 400 error handling in `main.py`.
* **Action Taken**:
  > Adjusted assertions to match the actual API contract (`assert res.status_code == 400` and `assert res.json()["detail"] == "Invalid status"`).