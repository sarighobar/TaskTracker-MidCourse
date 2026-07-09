import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import your database elements and models cleanly
from app.database import Base, get_db
from app.models.task import Task
from app.main import app

# FIXED: Use a local file instead of volatile :memory: so data survives between API requests
TEST_DATABASE_URL = "sqlite:///./test_tracker.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply the path database overrides
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    # Build the tables fresh in our stable test file
    Base.metadata.create_all(bind=test_engine)
    yield
    # Clean up and drop tables after the test finishes
    Base.metadata.drop_all(bind=test_engine)

# Test 1: Creating a task with tags
def test_create_task_with_tags():
    response = client.post("/tasks/", json={
        "title": "Fix Login Page",
        "description": "Auth token bug",
        "tags": "Bug,Frontend"
    })
    assert response.status_code == 201
    assert response.json()["tags"] == "Bug,Frontend"

# Test 2: Stripping whitespace validation
def test_tags_validation_whitespace():
    response = client.post("/tasks/", json={
        "title": "Clean Database",
        "tags": " Backend , Database "
    })
    assert response.status_code == 201
    assert response.json()["tags"] == "Backend,Database"

# Test 3: Querying text search by Title parameter
def test_search_filter_by_title():
    client.post("/tasks/", json={"title": "Apple Ecosystem Task"})
    client.post("/tasks/", json={"title": "Banana Harvest Task"})
    
    response = client.get("/tasks/?search=Apple")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["title"] == "Apple Ecosystem Task"

# Test 4: Querying text search by Tag attribute
def test_search_filter_by_tag():
    client.post("/tasks/", json={"title": "Task A", "tags": "Urgent"})
    client.post("/tasks/", json={"title": "Task B", "tags": "Normal"})
    
    response = client.get("/tasks/?search=Urgent")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["tags"] == "Urgent"