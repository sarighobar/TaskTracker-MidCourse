import pytest

def test_create_task(client):
    response = client.post("/tasks/", json={"title": "Test Task", "status": "To Do", "priority": "High"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"

def test_delete_task(client):
    # Create a task to delete
    response = client.post("/tasks/", json={"title": "To Delete", "status": "To Do", "priority": "Low"})
    task_id = response.json()["id"]
    
    # Delete it
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200
    
    # Verify it's gone
    get_response = client.get("/tasks/")
    assert len(get_response.json()) == 0

def test_filter_by_status(client):
    """Verify that filtering by status returns only relevant tasks."""
    client.post("/tasks/", json={"title": "Work", "status": "To Do", "priority": "High"})
    client.post("/tasks/", json={"title": "Relax", "status": "Done", "priority": "Low"})
    
    # Filter for Done
    response = client.get("/tasks/?status=Done")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    assert data[0]["status"] == "Done"
    assert data[0]["title"] == "Relax"

def test_get_all_tasks_no_filter(client):
    """Verify that without a filter, all tasks are returned."""
    client.post("/tasks/", json={"title": "Task A", "status": "To Do", "priority": "High"})
    client.post("/tasks/", json={"title": "Task B", "status": "Done", "priority": "Low"})
    
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 2