from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_task_with_trimmed_tags():
    # Test 1: Verifies tags are automatically trimmed of extra spaces
    response = client.post("/tasks", json={
        "title": "Fix dashboard layout",
        "tags": " ui , bug, frontend "
    })
    assert response.status_code == 201
    assert response.json()["tags"] == "ui,bug,frontend"

def test_search_tasks_filter():
    # Test 2: Verifies search matches titles and description
    client.post("/tasks", json={"title": "Write Odoo report"})
    client.post("/tasks", json={"title": "Walk the dog"})
    
    response = client.get("/tasks?search=Odoo")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Write Odoo report"

def test_filter_by_tag():
    # Test 3: Verifies filtering by tag returns matching items only
    client.post("/tasks", json={"title": "API Auth", "tags": "security"})
    client.post("/tasks", json={"title": "CSS color tweak", "tags": "style"})
    
    response = client.get("/tasks?tag=security")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "API Auth"

def test_invalid_status_transition_returns_422():
    # Test 4: Verifies we cannot jump directly from ToDo to Done
    create_res = client.post("/tasks", json={"title": "Validation test"})
    task_id = create_res.json()["id"]
    
    update_res = client.patch(f"/tasks/{task_id}", json={"status": "Done"})
    assert update_res.status_code == 422