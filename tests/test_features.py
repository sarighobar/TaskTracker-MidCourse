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