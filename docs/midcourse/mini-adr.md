# Mini Architecture Decision Record (ADR)

## Decision
For the Mid-Course Feature Extension Sprint, we successfully implemented two scoped features:
1. **Tags/Labels**: Allowing tasks to store comma-separated, trimmed, non-empty tags.
2. **Search + Combined Filters**: Enabling text-based search across both task titles and descriptions.

## Why This Approach Fits
We used **SQLAlchemy** query-level filtering (`.ilike()`) in the backend to handle search and tag lookups. This approach keeps the architecture incredibly simple, fast, and light. It stores tags as a comma-separated string column in our SQLite database, avoiding complex join tables while meeting the validation criteria.

## Alternatives Considered
* **Separate Tag Association Table (Many-to-Many Relational Schema)**: Suggested by the AI assistant. We rejected this because a relational junction table would add unnecessary schema migrations, query joins, and code complexity that is out of scope for a single-user prototype.
* **Full-text Search Indexes (SQLite FTS5)**: Suggested by the AI to optimize search. We rejected this because our task database is small, and standard SQL `LIKE` operators are highly performant and easier to test.

## What Was Accepted and Rejected
* **Accepted**: Pydantic `@field_validator` hooks to automatically sanitize, strip spaces, and format comma-separated tags before database insertion.
* **Rejected**: Introducing heavy third-party front-end state management libraries. We opted for vanilla JavaScript to update the DOM elements directly, matching the style of Modules 1-3.