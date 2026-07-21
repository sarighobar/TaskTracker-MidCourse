import pytest

# ==========================================
# BASELINE CORE CRUD TESTS
# ==========================================

def test_create_task_basic(client):
    response = client.post("/api/tasks/", json={
        "title": "Basic Task",
        "description": "Simple description"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Basic Task"
    assert "id" in data


def test_reject_empty_title(client):
    response = client.post("/api/tasks/", json={
        "title": "   ",
        "description": "No title task"
    })
    assert response.status_code == 422


def test_get_single_task_and_not_found(client):
    create_res = client.post("/api/tasks/", json={"title": "Find Me"})
    task_id = create_res.json()["id"]

    res = client.get(f"/api/tasks/{task_id}")
    assert res.status_code == 200
    assert res.json()["title"] == "Find Me"

    nf_res = client.get("/api/tasks/9999")
    assert nf_res.status_code == 404


def test_delete_task(client):
    create_res = client.post("/api/tasks/", json={"title": "To Be Deleted"})
    task_id = create_res.json()["id"]

    del_res = client.delete(f"/api/tasks/{task_id}")
    assert del_res.status_code == 204

    get_res = client.get(f"/api/tasks/{task_id}")
    assert get_res.status_code == 404


# ==========================================
# TAGS / LABELS TESTS
# ==========================================

def test_create_task_with_tags(client):
    response = client.post("/api/tasks/", json={
        "title": "Build Auth Feature",
        "description": "OAuth implementation",
        "tags": "backend, security, v1"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["tags"] == "backend,security,v1"


def test_reject_empty_tag(client):
    response = client.post("/api/tasks/", json={
        "title": "Clean Database",
        "tags": "   ,  , backend , , "
    })
    assert response.status_code == 201
    assert response.json()["tags"] == "backend"


def test_update_task_tags(client):
    create_res = client.post("/api/tasks/", json={"title": "Setup CI/CD", "tags": "devops"})
    task_id = create_res.json()["id"]

    update_res = client.put(f"/api/tasks/{task_id}", json={
        "title": "Setup CI/CD",
        "tags": "devops, github-actions"
    })
    assert update_res.status_code == 200
    assert update_res.json()["tags"] == "devops,github-actions"


def test_filter_by_tag(client):
    client.post("/api/tasks/", json={"title": "UI Task", "tags": "frontend"})
    client.post("/api/tasks/", json={"title": "API Task", "tags": "backend"})
    client.post("/api/tasks/", json={"title": "Fullstack Task", "tags": "frontend,backend"})

    res = client.get("/api/tasks/?tag=frontend")
    assert res.status_code == 200
    tasks = res.json()
    assert len(tasks) == 2
    titles = [t["title"] for t in tasks]
    assert "UI Task" in titles
    assert "Fullstack Task" in titles


def test_preserve_tags_after_unrelated_update(client):
    create_res = client.post("/api/tasks/", json={
        "title": "Fix Bug", 
        "status": "ToDo", 
        "tags": "urgent,bug"
    })
    task_id = create_res.json()["id"]

    patch_res = client.patch(f"/api/tasks/{task_id}/status", json={"status": "InProgress"})
    assert patch_res.status_code == 200
    assert patch_res.json()["tags"] == "urgent,bug"


# ==========================================
# SEARCH & COMBINED FILTERS TESTS
# ==========================================

def test_search_title_and_description(client):
    client.post("/api/tasks/", json={"title": "Fix Auth Bug", "description": "Minor fix"})
    client.post("/api/tasks/", json={"title": "Update Docs", "description": "Include OAuth authentication"})
    client.post("/api/tasks/", json={"title": "Refactor Code", "description": "Clean up functions"})

    res = client.get("/api/tasks/?search=auth")
    assert res.status_code == 200
    tasks = res.json()
    assert len(tasks) == 2
    titles = [t["title"] for t in tasks]
    assert "Fix Auth Bug" in titles
    assert "Update Docs" in titles


def test_combine_status_and_priority(client):
    client.post("/api/tasks/", json={"title": "Task 1", "status": "ToDo", "priority": "High"})
    client.post("/api/tasks/", json={"title": "Task 2", "status": "ToDo", "priority": "Low"})
    client.post("/api/tasks/", json={"title": "Task 3", "status": "Done", "priority": "High"})

    res = client.get("/api/tasks/?status=ToDo&priority=High")
    assert res.status_code == 200
    tasks = res.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Task 1"


def test_search_no_matches_returns_empty_list(client):
    client.post("/api/tasks/", json={"title": "Setup Docker", "description": "Containerize app"})

    res = client.get("/api/tasks/?search=nonexistentterm")
    assert res.status_code == 200
    assert res.json() == []


def test_invalid_filter_value_status(client):
    create_res = client.post("/api/tasks/", json={"title": "Test Task"})
    task_id = create_res.json()["id"]

    res = client.patch(f"/api/tasks/{task_id}/status", json={"status": "InvalidStatus"})
    assert res.status_code == 400
    assert res.json()["detail"] == "Invalid status"


def test_health_check_endpoint(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}

    import pytest
from fastapi import HTTPException
from app.business_rules import validate_status_transition

def test_same_status_is_valid():
    """Verify that keeping the same status doesn't raise an error."""
    validate_status_transition("ToDo", "ToDo")
    validate_status_transition("InProgress", "InProgress")
    validate_status_transition("Done", "Done")

def test_allowed_status_transitions():
    """Verify valid transitions move through the state machine correctly."""
    validate_status_transition("ToDo", "InProgress")
    validate_status_transition("InProgress", "Done")
    validate_status_transition("InProgress", "ToDo")
    validate_status_transition("Done", "InProgress")

def test_invalid_current_status_raises_400():
    """Verify an unknown starting status raises a 400 HTTPException."""
    with pytest.raises(HTTPException) as exc_info:
        validate_status_transition("UnknownStatus", "Done")
    
    assert exc_info.value.status_code == 400
    assert "Invalid current status" in exc_info.value.detail

def test_disallowed_transition_raises_400():
    """Verify skipping states (e.g. ToDo -> Done directly) raises a 400 HTTPException."""
    with pytest.raises(HTTPException) as exc_info:
        validate_status_transition("ToDo", "Done")
    
    assert exc_info.value.status_code == 400
    assert "Invalid status transition" in exc_info.value.detail