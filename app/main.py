from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pathlib import Path
from app.database import engine, Base, get_db
from app import models, schemas
from app.business_rules import validate_status_transition

# Create SQLite DB tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Tracker Enterprise API")

# Setup CORS so the frontend can easily communicate with backend endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve path to index.html inside the sibling "frontend" folder
FRONTEND_PATH = Path(__file__).resolve().parent.parent / "frontend" / "index.html"

@app.get("/", response_class=HTMLResponse)
def read_root():
    """Serves the frontend Kanban board directly at the root URL."""
    if not FRONTEND_PATH.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="index.html not found in frontend/ directory"
        )
    return FRONTEND_PATH.read_text(encoding="utf-8")

@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

@app.get("/tasks", response_model=List[schemas.TaskResponse])
def get_tasks(
    search: Optional[str] = Query(None, description="Search by title or description"),
    tag: Optional[str] = Query(None, description="Filter tasks by tag"),
    db: Session = Depends(get_db)
):
    """Fetches tasks from the database with optional search and tag filters."""
    query = db.query(models.Task)
    
    # 1. Text search across both Title & Description
    if search:
        query = query.filter(
            (models.Task.title.ilike(f"%{search}%")) | 
            (models.Task.description.ilike(f"%{search}%"))
        )
    
    # 2. Tag Filter (Matches if tag is present inside comma-separated string)
    if tag:
        query = query.filter(models.Task.tags.ilike(f"%{tag}%"))
        
    return query.all()

@app.post("/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Creates a new task with validated schemas and tags."""
    new_task = models.Task(**payload.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.patch("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """Updates selected attributes of a task and checks state transition rules."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    
    update_data = payload.model_dump(exclude_unset=True)
    
    # Validate transition rule if status is being updated
    if "status" in update_data:
        validate_status_transition(task.status, update_data["status"])
        
    for key, val in update_data.items():
        setattr(task, key, val)
        
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Deletes a task from the board database."""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted"}