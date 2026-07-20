# User Stories & Feature Specifications

This document defines the functional requirements and user expectations for the two selected features: **Tags / Labels** and **Search + Combined Filters**. Each feature includes 4 distinct user stories with acceptance criteria and AI review corrections.

---

## Feature 1: Tags / Labels

### User Story 1.1: Add Tags During Task Creation
* **As a** project manager,
* **I want to** add comma-separated tags when creating a task,
* **So that** I can categorize tasks by department or domain (e.g., `frontend`, `urgent`).

#### Acceptance Criteria
1. The creation modal includes an input field for tags.
2. Comma-separated strings are automatically sanitized by trimming extra spaces.
3. Empty tag entries (e.g., `, ,`) are filtered out before saving.

#### AI Assistance & Review
* **Initial AI Suggestion**: AI suggested a relational database schema with a separate `Tags` table and a `TaskTags` junction table.
* **Human Correction**: Rejected the junction table as over-engineering for this lightweight prototype. Instructed AI to store tags as a normalized CSV string in the Pydantic schema with a custom `@field_validator`.

---

### User Story 1.2: Display Tag Chips on Cards
* **As a** developer,
* **I want to** see tag badges (chips) displayed on each task card in the Kanban board,
* **So that** I can quickly spot task categories at a glance.

#### Acceptance Criteria
1. Each tag in the saved task's string renders as an individual styled badge on the card.
2. Cards without tags render normally without breaking layout or throwing JavaScript errors.

#### AI Assistance & Review
* **Initial AI Suggestion**: AI generated JS code that called `.split(',')` without checking if `task.tags` was null or undefined.
* **Human Correction**: Added null checks and trimmed whitespace around tag chips during rendering to prevent blank badges.

---

### User Story 1.3: Update Task Tags
* **As a** project manager,
* **I want to** edit existing tags when updating a task in the modal,
* **So that** I can re-categorize tasks as priorities shift.

#### Acceptance Criteria
1. Opening the Edit modal populates the tag input with current task tags.
2. Saving changes updates the task's tags without wiping out existing fields like status or description.

#### AI Assistance & Review
* **Initial AI Suggestion**: AI attempted to overwrite the entire task object without preserving unmodified fields.
* **Human Correction**: Corrected the `PUT` handler logic to merge payload updates and maintain normalized tag formatting.

---

### User Story 1.4: Filter Tasks by Tag
* **As a** team member,
* **I want to** filter the Kanban board by typing a specific tag,
* **So that** I can focus exclusively on tasks assigned to my area (e.g., `backend`).

#### Acceptance Criteria
1. The UI provides a "Filter by tag..." input field.
2. Typing a tag updates the displayed cards to show only tasks containing that tag (case-insensitive).
3. The API endpoint handles `GET /api/tasks/?tag=<tag_name>`.

#### AI Assistance & Review
* **Initial AI Suggestion**: AI implemented tag filtering on the frontend only, ignoring backend query parameters.
* **Human Correction**: Updated `app/main.py` to accept `tag: Optional[str] = None` and perform tag matching on the backend.

---

## Feature 2: Search + Combined Filters

### User Story 2.1: Text Search Across Title and Description
* **As a** developer,
* **I want to** search for keywords using a search bar,
* **So that** I can find relevant tasks whether the keyword appears in the title or the description.

#### Acceptance Criteria
1. Searching matches text in both the `title` and `description` fields case-insensitively.
2. Partial keyword matches return matching tasks.
3. If no match is found, the API returns HTTP 200 with an empty list `[]`.

#### AI Assistance & Review
* **Initial AI Suggestion**: AI limited search logic strictly to the `title` field (`t["title"]`).
* **Human Correction**: Expanded backend logic in `app/main.py` to check both `title` and `description` fields.

---

### User Story 2.2: Combined Filtering by Status and Priority
* **As a** team lead,
* **I want to** filter tasks simultaneously by status and priority (e.g., `ToDo` + `High`),
* **So that** I can prioritize critical pending work.

#### Acceptance Criteria
1. Selecting a status dropdown option and a priority dropdown option combines both filters.
2. Only tasks satisfying **both** conditions are returned by `GET /api/tasks/?status=ToDo&priority=High`.

#### AI Assistance & Review
* **Initial AI Suggestion**: AI created separate endpoint routes for each filter combination (`/api/tasks/status/{s}` and `/api/tasks/priority/{p}`).
* **Human Correction**: Replaced separate routes with unified query parameters in a single `GET /api/tasks/` endpoint.

---

### User Story 2.3: Combined Search and Tag Filtering
* **As a** developer,
* **I want to** combine text search with a tag filter,
* **So that** I can narrow down specific backend bugs without seeing frontend tasks.

#### Acceptance Criteria
1. Passing both `search` and `tag` query parameters filters tasks matching both criteria.
2. Sending invalid filter values responds gracefully without server crashes.

#### AI Assistance & Review
* **Initial AI Suggestion**: AI executed frontend search after dropping active backend filters.
* **Human Correction**: Refactored frontend `fetchTasks()` to build a unified `URLSearchParams` object containing all active filter fields.

---

### User Story 2.4: Real-time UI Board Refresh on Filter Input
* **As a** user,
* **I want to** see the board update dynamically as I type into search or filter inputs,
* **So that** I get immediate visual feedback without manual page reloads.

#### Acceptance Criteria
1. Input event listeners triggers fetch updates dynamically (`oninput="fetchTasks()"`).
2. Board column counters dynamically update to reflect filtered task counts.

#### AI Assistance & Review
* **Initial AI Suggestion**: AI suggested adding a dedicated "Submit Search" button.
* **Human Correction**: Used inline `oninput` handlers for a smoother user experience.