# Reflection

## Overview
The TaskTracker project focused on building a robust, decoupled task management application utilizing a FastAPI backend and an interactive HTML5 frontend interface. Developing this mid-course project was an insightful experience that challenged my understanding of RESTful API design, data validation, and state management.

## AI Tools Used and Purpose
Throughout this sprint, I primarily utilized AI assistants as my pair programmers. I used AI to assist with generating the initial boilerplate for FastAPI routing, scaffolding the Pydantic data models, and drafting the foundational HTML/CSS layout for the frontend Kanban board. It was also utilized to help generate the initial syntax for testing fixtures in our `pytest` suite.

## When AI Helped
The AI was incredibly helpful in accelerating the setup of my Pydantic schema validation and the core HTTP endpoints. Instead of manually typing out all the standard CRUD operations, the AI quickly provided a functional baseline for `GET`, `POST`, `PUT`, `PATCH`, and `DELETE` routes. This allowed me to focus on the higher-level architecture rather than the repetitive boilerplate. It also effectively helped me debug cross-origin resource sharing (CORS) configurations when connecting the decoupled frontend to the backend service.

## When AI Slowed Me Down
There was a distinct moment where relying on the AI slowed down my momentum. When I asked it to help implement the tags feature, the AI immediately suggested a highly complex relational database architecture using a Many-to-Many junction table. For a simple single-user prototype, this was massive over-engineering. I spent too much time trying to comprehend and implement this heavy structure before realizing it was entirely unnecessary for the project's scope. Additionally, the AI initially assumed that blank tag inputs were acceptable, which conflicted with my data integrity goals.

## How My Review Changed the Result
Because the AI's suggestions were over-engineered and missed edge cases, my manual review fundamentally changed the final implementation. I explicitly rejected the complex junction table architecture in favor of a simplified string filter approach. I corrected the system assumption by implementing a strict Pydantic `@field_validator` that enforces data sanitization by trimming whitespace, stripping duplicate commas, and entirely rejecting empty string inputs. Furthermore, I refined the backend search query structure. The AI initially limited the search function to just the title column, but I manually modified the backend query logic to ensure it searches across both the title and description fields to prevent missing relevant items.