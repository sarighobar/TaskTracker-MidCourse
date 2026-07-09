Goal
In this project, I implemented two primary features to enhance the TaskTracker API:

Status Filtering: Added the ability to filter tasks by their current status (e.g., To Do, Done) via query parameters.

Search/Title Filtering: Implemented a case-insensitive search functionality that allows users to filter tasks by matching keywords within either the title or the tags field.

The "Small Loop" Experience
Adopting the "Backend -> Test -> Frontend" loop significantly improved my development speed and code quality. By writing tests before finishing the implementation (such as test_tags_validation), I was able to identify that my tags were being saved with incorrect whitespace. I also caught the AttributeError caused by my initial folder structure early, which prevented these issues from compounding into larger, harder-to-debug problems later in the process.

Challenges
The most significant challenge was resolving import errors related to Python module resolution. My initial directory structure used folders for models and schemas instead of files, which prevented the application from finding the Task class. Standardizing the structure by moving these into dedicated .py files within the app/ directory and ensuring the correct use of absolute imports resolved these conflicts and stabilized the test environment.