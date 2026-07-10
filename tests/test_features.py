import pytest

def test_create_task_with_tags(client):
    """Verify creating a task with valid comma-separated tags works properly"""
    response = client.post("/tasks/", json={
        "title": "Fix Login Page",
        "description": "Auth token bug",
        "tags": "Bug,Frontend",
        "priority": "Medium",
        "status": "To Do"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["tags"] == "Bug,Frontend"


def test_tags_validation_whitespace(client):
    """Verify whitespace around tags is automatically stripped during validation"""
    response = client.post("/tasks/", json={
        "title": "Clean Database",
        "tags": " Backend , Database ",
        "priority": "Medium",
        "status": "To Do"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["tags"] == "Backend,Database"


def test_search_filter_by_title(client):
    """Verify searching tasks by title case-insensitively filters correctly"""
    # 1. Populate test data inside the sandboxed database
    client.post("/tasks/", json={"title": "Apple Ecosystem Task", "priority": "Low", "status": "To Do"})
    client.post("/tasks/", json={"title": "Banana Harvest Task", "priority": "Low", "status": "To Do"})
    
    # 2. Search for the keyword
    response = client.get("/tasks/?search=Apple")
    assert response.status_code == 200
    results = response.json()
    
    # 3. Assert only the matched title comes back
    assert len(results) == 1
    assert results[0]["title"] == "Apple Ecosystem Task"


def test_search_filter_by_tag(client):
    """Verify searching tasks by tags case-insensitively filters correctly"""
    # 1. Populate test data inside the sandboxed database
    client.post("/tasks/", json={"title": "Task A", "tags": "Urgent", "priority": "High", "status": "To Do"})
    client.post("/tasks/", json={"title": "Task B", "tags": "Normal", "priority": "Low", "status": "To Do"})
    
    # 2. Search for the tag
    response = client.get("/tasks/?search=urgent")
    assert response.status_code == 200
    results = response.json()
    
    # 3. Assert only the task matching the tag context comes back
    assert len(results) == 1
    assert results[0]["title"] == "Task A"


def test_root_serves_frontend_page(client):
    """The root endpoint should serve the Task Tracker UI so the browser can load it directly from the API server."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Task Tracker Workspace" in response.text


def test_root_page_exposes_activity_panel(client):
    """The served UI should include the activity sidebar panel by default."""
    response = client.get("/")
    assert response.status_code == 200
    assert 'id="activityLogStream"' in response.text
    assert "Activity Log" in response.text
    assert "hidden xl:flex" not in response.text


def test_update_task_status(client):
    """Tasks should allow their workflow status to be updated through the API."""
    created = client.post("/tasks/", json={"title": "Ship feature", "priority": "High", "status": "To Do"})
    task_id = created.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"status": "Done"})
    assert response.status_code == 200
    assert response.json()["status"] == "Done"


def test_filter_by_priority_and_overdue(client):
    """The task listing should support filtering by priority and overdue tasks used by the UI."""
    client.post("/tasks/", json={"title": "High overdue", "priority": "High", "status": "To Do", "due_date": "2023-01-01"})
    client.post("/tasks/", json={"title": "Medium upcoming", "priority": "Medium", "status": "To Do", "due_date": "2099-01-01"})

    response = client.get("/tasks/?priority_filter=High&overdue_only=true")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["title"] == "High overdue"