# User Stories & Feature Specifications

## Feature 1: Task Categorization with Tags

### US-1.1: Add Tags During Task Creation
* **As a** TaskTracker user,
* **I want to** attach comma-separated tags when creating a new task,
* **So that** I can categorize my work items immediately at creation time.

**Acceptance Criteria:**
* The task creation modal includes an optional "Tags" input field.
* Tags entered as comma-separated values (e.g., `work, urgent`) are trimmed and saved cleanly to the database.
* Empty tags or extra spaces (e.g., `work, , urgent `) are automatically sanitized into `work,urgent`.

---

### US-1.2: Filter Tasks by Tag
* **As a** TaskTracker user,
* **I want to** filter my task dashboard by selecting or requesting a specific tag,
* **So that** I can focus exclusively on tasks belonging to a single category.

**Acceptance Criteria:**
* `GET /tasks?tag=work` returns only tasks containing `work` in their tag list.
* Tag matching is case-insensitive (e.g., filtering for `Work` matches `work`).
* Unmatched tasks are excluded from the response array.

---

### US-1.3: Update Task Tags
* **As a** TaskTracker user,
* **I want to** edit or clear tags on an existing task,
* **So that** task metadata stays up to date as priorities and categories change.

**Acceptance Criteria:**
* `PATCH /tasks/{id}` accepts a updated `tags` string parameter.
* Updating unrelated fields (like `status`) preserves existing tags if `tags` is omitted in the payload.
* Sending an empty string (`""`) for `tags` successfully clears all tags from the task.

---

### US-1.4: Visual Tag Display on Task Cards
* **As a** TaskTracker user,
* **I want to** see tags rendered as distinct visual chips on each task card,
* **So that** I can visually identify categories at a glance without opening task details.

**Acceptance Criteria:**
* Each tag in a comma-separated list is rendered as an individual visual chip element (`.chip`).
* Tasks with no tags omit the chip container cleanly without rendering blank elements.

> 💡 **AI Assumption Corrected (Feature 1):** 
> **AI Assumption:** The AI initially assumed tags should be stored in a separate relational table with a Many-to-Many foreign key relationship (`TaskTag` junction table).
> **Correction:** I corrected the AI to store tags as a simple, trimmed comma-separated string directly in the `Task` schema table (`tags` column). This kept the SQLite database lightweight and avoided unnecessary JOIN complexity for our local TaskTracker app.

---

## Feature 2: Real-time Search & Combined Filtering

### US-2.1: Full-Text Keyword Search
* **As a** TaskTracker user,
* **I want to** search tasks using keywords in a search bar,
* **So that** I can rapidly locate specific tasks by searching their titles or descriptions.

**Acceptance Criteria:**
* `GET /tasks?search=keyword` performs a substring search across both task `title` and `description` fields.
* Search matches are case-insensitive.
* Returns an empty list (`[]`) with a `200 OK` status code if no matching tasks are found.

---

### US-2.2: Multi-Criteria Combined Filtering
* **As a** TaskTracker user,
* **I want to** combine search terms with status, priority, and tag filters simultaneously,
* **So that** I can pinpoint exact tasks in a large backlog.

**Acceptance Criteria:**
* The `GET /tasks` endpoint accepts `status`, `priority`, `tag`, and `search` query parameters together.
* The backend applies SQL `AND` conditions across all active query filters.
* Re-fetching data updates the UI dynamically when any filter control changes.

---

### US-2.3: Graceful Search & Filter Empty States
* **As a** TaskTracker user,
* **I want to** see a clear visual notice when my search or filter criteria return no results,
* **So that** I know my search worked correctly and there are simply no matching tasks.

**Acceptance Criteria:**
* The UI displays a friendly empty-state message (e.g., "No tasks match your current search/filters") when the API returns an empty array.
* Clearing the search bar or resetting filters restores the full task list immediately.

---

### US-2.4: Strict Filter Input Validation
* **As an** API consumer,
* **I want** the backend to validate query filter parameters and return explicit error messages for invalid values,
* **So that** invalid requests fail early with actionable error responses.

**Acceptance Criteria:**
* Passing invalid `status` or `priority` values (e.g., `?status=invalid_status`) returns a `400 Bad Request` or `422 Unprocessable Entity`.
* The error payload explains why the value was rejected.

> 💡 **AI Assumption Corrected (Feature 2):** 
> **AI Assumption:** The AI assumed the `search` query parameter should only scan the `title` column of the task table.
> **Correction:** I instructed the AI to extend search filtering to evaluate both `title` AND `description` using an SQL `OR` condition, ensuring users could find tasks based on context written inside task descriptions.