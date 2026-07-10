# Mini ADR

## Decision
We implemented two small but practical features in the Task Tracker app:
- task status updates through a PUT endpoint, and
- richer task listing filters for priority and overdue work.

## Why this approach
The frontend already expected these capabilities, so the fastest reliable path was to add backend support for them and keep the UI contract simple. This kept the change set focused and avoided introducing an unnecessary new architecture.

## Alternatives considered
- A larger state-management layer for the board was rejected as too complex for this project scope.
- A separate analytics service for overdue logic was rejected because it would add unnecessary overhead for a single-page app.

## What was accepted and rejected
The AI suggestions for adding broad search support were accepted, but larger refactors such as introducing a full task service layer or separate database migration tooling were rejected as out of scope for this mid-course deliverable.