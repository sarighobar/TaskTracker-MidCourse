# Mini Architecture Decision Record (ADR)

## Decision
For the Mid-Course Feature Extension Sprint, we successfully implemented two scoped features:
1. **Tags/Labels**: Allowing tasks to store comma-separated, trimmed, non-empty tags validated by the backend.
2. **Search + Combined Filters**: Enabling responsive text-based search across both task titles and descriptions.

## Why This Approach Fits
We utilized lightweight, manual string-cleaning logic directly in `app/routers.py` to handle tag normalization and combined SQLAlchemy `.filter()` calls to handle search/status/priority/tag validation efficiently. By storing tags as a clean, standardized comma-separated string attribute, we avoided complex join tables while meeting all validation criteria for a single-user prototype.

## Alternatives Considered
* **Separate Tag Association Table (Many-to-Many Relational Schema)**: Suggested by the AI assistant. We rejected this because a relational junction table would add unnecessary schema migrations, query joins, and code complexity that is out of scope for this sprint.
* **Full-text Search Indexes (SQLite FTS5)**: Suggested by the AI to optimize search. We rejected this because our task database is compact, and standard substring matching operators are highly performant, simpler to implement, and easier to test reliably.

## What Was Accepted and Rejected
* **Accepted**: A plain Python helper pattern — `",".join([t.strip() for t in raw.split(",") if t.strip()])` — applied in both `create_task` and `update_task` in `app/routers.py` to trim, deduplicate blanks, and normalize comma-separated tags before persistence. We also accepted adding explicit `VALID_STATUSES`/`VALID_PRIORITIES` checks to `GET /api/tasks/` so invalid filter values return `400 Bad Request` instead of silently returning an empty list.
* **Rejected**: Introducing a front-end framework, build step, or CSS utility library. We opted for a single static `Frontend/index.html` file with plain inline CSS and vanilla JavaScript `fetch()` calls, since the project scope didn't call for build tooling.
