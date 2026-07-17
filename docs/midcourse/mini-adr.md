# Mini Architecture Decision Record (ADR)

## Decision
For the Mid-Course Feature Extension Sprint, we successfully implemented two scoped features:
1. **Tags/Labels**: Allowing tasks to store comma-separated, trimmed, non-empty tags validated by the backend.
2. **Search + Combined Filters**: Enabling responsive text-based search across both task titles and descriptions.

## Why This Approach Fits
We utilized lightweight filtering combined with **Pydantic** schema constraints to handle search validation and tag lookups efficiently. By storing tags as a clean, standardized comma-separated string attribute, we avoided complex join tables while meeting all validation criteria for a single-user prototype.

## Alternatives Considered
* **Separate Tag Association Table (Many-to-Many Relational Schema)**: Suggested by the AI assistant. We rejected this because a relational junction table would add unnecessary schema migrations, query joins, and code complexity that is out of scope for this sprint.
* **Full-text Search Indexes (SQLite FTS5)**: Suggested by the AI to optimize search. We rejected this because our task database is compact, and standard substring matching operators are highly performant, simpler to implement, and easier to test reliably.

## What Was Accepted and Rejected
* **Accepted**: Pydantic `@field_validator` hooks to automatically sanitize, strip spaces, and format comma-separated tags on the backend payload before state persistence.
* **Rejected**: Introducing heavy third-party front-end state management or complex UI frameworks. We opted for clean vanilla JavaScript and utility-first Tailwind CSS to update the DOM elements directly, maximizing speed and maintainability.