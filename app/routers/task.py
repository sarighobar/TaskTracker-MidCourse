from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, database

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    # Clean tags: split by comma, strip whitespace, join back
    if task.tags:
        tags_list = [t.strip() for t in task.tags.split(",")]
        task.tags = ",".join(tags_list)
        
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/", response_model=List[schemas.Task])
def get_all_tasks(
    status: Optional[str] = None, 
    search: Optional[str] = None,
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Task)
    
    if status:
        query = query.filter(models.Task.status == status)
    
    # New search logic: search in title OR tags (case-insensitive)
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (models.Task.title.ilike(search_filter)) | 
            (models.Task.tags.ilike(search_filter))
        )
        
    return query.all()

@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}