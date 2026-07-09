# Task Tracker Enterprise Workspace

## How to Run the Backend (API)
1. Ensure Python 3.12+ is installed.
2. Install dependencies: `pip install fastapi uvicorn sqlalchemy`
3. Start the Uvicorn server:
   ```bash
   uvicorn app.main:app --reload