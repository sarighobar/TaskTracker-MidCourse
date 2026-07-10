# Mini ADR

## Decision
We implemented two scoped features that were already implied by the existing Kanban UI:
- task status updates through a PUT endpoint, and
- richer task listing filters for priority and overdue items.

## Why this approach
The UI already expected these capabilities, so the fastest reliable path was to add backend support and keep the frontend contract simple. This kept the change set focused and avoided a larger architectural rewrite.

## Alternatives considered
- A larger board state-management layer was rejected as too complex for the mid-course scope.
- A separate analytics service for overdue logic was rejected because it would add unnecessary overhead for a single-page app.

## Accepted and rejected changes
The AI suggestions for adding broad search support were accepted, but larger refactors such as introducing a full task service layer or database migration tooling were rejected as out of scope.
