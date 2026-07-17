import pytest

def test_create_task(client):
    response = client.post("/api/tasks/", json={"title": "Test Task", "status": "ToDo"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"

def test_get_tasks(client):
    response = client.get("/api/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_task(client):
    create = client.post("/api/tasks/", json={"title": "Single", "status": "ToDo"})
    t_id = create.json()["id"]
    response = client.get(f"/api/tasks/{t_id}")
    assert response.status_code == 200
    assert response.json()["id"] == t_id

def test_update_task_details(client):
    create = client.post("/api/tasks/", json={"title": "Old", "status": "ToDo"})
    t_id = create.json()["id"]
    response = client.put(f"/api/tasks/{t_id}", json={"title": "New"})
    assert response.status_code == 200

def test_delete_task(client):
    create = client.post("/api/tasks/", json={"title": "DeleteMe", "status": "ToDo"})
    t_id = create.json()["id"]
    response = client.delete(f"/api/tasks/{t_id}")
    assert response.status_code == 204

def test_get_non_existent_task(client):
    response = client.get("/api/tasks/999")
    assert response.status_code == 404

def test_update_non_existent_task(client):
    response = client.put("/api/tasks/999", json={"title": "Fail"})
    assert response.status_code == 404

def test_delete_non_existent_task(client):
    response = client.delete("/api/tasks/999")
    assert response.status_code == 404

def test_create_task_empty_title(client):
    response = client.post("/api/tasks/", json={"title": "", "status": "ToDo"})
    assert response.status_code in [400, 422]

def test_valid_status_transition(client):
    create = client.post("/api/tasks/", json={"title": "Status", "status": "ToDo"})
    t_id = create.json()["id"]
    response = client.patch(f"/api/tasks/{t_id}/status", json={"status": "Done"})
    assert response.status_code == 200

def test_invalid_status_transition(client):
    create = client.post("/api/tasks/", json={"title": "Bad", "status": "ToDo"})
    t_id = create.json()["id"]
    response = client.patch(f"/api/tasks/{t_id}/status", json={"status": "Invalid"})
    assert response.status_code == 400

def test_tag_normalization(client):
    response = client.post("/api/tasks/", json={"title": "Tags", "tags": " a, b , c "})
    assert response.status_code == 201
    assert "a,b,c" in response.json()["tags"]