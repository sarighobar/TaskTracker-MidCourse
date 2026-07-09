TaskTracker API
A robust backend service for tracking tasks, featuring status filtering, keyword searching, and data validation.

Features
Status Filtering: Filter tasks by their current status (e.g., To Do, In Progress).

Search Functionality: Perform case-insensitive searches across both title and tags fields.

Data Sanitization: Automatically cleans and strips whitespace from task tags.

Installation
Clone the repository: git clone <https://github.com/sarighobar/TaskTracker-MidCourse>

Navigate to the project folder: cd TaskTracker

Install dependencies: pip install -r requirements.txt

Running the API
Start the FastAPI server:
uvicorn app.main:app --reload

Testing
Run the test suite to verify all features:
pytest