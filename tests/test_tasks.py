import pytest

def test_create_task_activity_log(client):
    """Test 1: Verify creating a task automatically adds a log entry to the activity stream"""
    response = client.post("/tasks/", json={
        "title": "Activity Log Test",
        "description": "Checking logs",
        "priority": "Medium",
        "status": "To Do"
    })
    assert response.status_code == 201
    
    log_response = client.get("/tasks/global/activity")
    assert log_response.status_code == 200
    logs = log_response.json()
    
    assert len(logs) > 0
    assert logs[0]["action"] == "TASK CREATED"
    assert "Activity Log Test" in logs[0]["details"]


def test_transition_status_activity_log(client):
    """Test 2: Verify shifting columns creates a STAGE TRANSITION log entry"""
    create_resp = client.post("/tasks/", json={
        "title": "Move Me", 
        "priority": "Low", 
        "status": "To Do"
    })
    assert create_resp.status_code == 201
    task = create_resp.json()
    
    response = client.put(f"/tasks/{task['id']}", json={"status": "In Progress"})
    assert response.status_code == 200
    
    logs = client.get("/tasks/global/activity").json()
    assert logs[0]["action"] == "STAGE TRANSITION"
    assert "Moved task 'Move Me'" in logs[0]["details"]


def test_delete_task_activity_log(client):
    """Test 3: Verify deleting a task logs a RECORD PURGED event"""
    create_resp = client.post("/tasks/", json={
        "title": "Delete Me", 
        "priority": "Low", 
        "status": "To Do"
    })
    assert create_resp.status_code == 201
    task = create_resp.json()
    
    del_response = client.delete(f"/tasks/{task['id']}")
    assert del_response.status_code == 200
    
    logs = client.get("/tasks/global/activity").json()
    assert logs[0]["action"] == "RECORD PURGED"
    assert "Delete Me" in logs[0]["details"]


def test_backend_status_normalization(client):
    """Test 4: Verify status entries like 'todo' clean up cleanly to 'To Do'"""
    response = client.post("/tasks/", json={
        "title": "Normalize Test",
        "priority": "Low",
        "status": "todo"
    })
    assert response.status_code == 201
    assert response.json()["status"] == "To Do"