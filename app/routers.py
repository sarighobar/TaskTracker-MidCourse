from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, database

router = APIRouter(prefix="/api/tasks")

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_task(task: dict, db: Session = Depends(database.get_db)):
    # Validate title presence
    if not task.get("title") or not task["title"].strip():
        raise HTTPException(status_code=422, detail="Title required")
    
    # Normalize tags if they exist
    if task.get("tags"):
        tags_list = [t.strip() for t in task["tags"].split(",") if t.strip()]
        task["tags"] = ",".join(tags_list)
        
    db_task = models.Task(**task)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/")
def get_tasks(db: Session = Depends(database.get_db)):
    return db.query(models.Task).all()

@router.get("/{t_id}")
def get_task(t_id: int, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == t_id).first()
    if not task: raise HTTPException(status_code=404)
    return task

@router.put("/{t_id}")
def update_task(t_id: int, task_data: dict, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == t_id).first()
    if not task: raise HTTPException(status_code=404)
    return task

@router.delete("/{t_id}", status_code=204)
def delete_task(t_id: int, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == t_id).first()
    if not task: raise HTTPException(status_code=404)
    db.delete(task)
    db.commit()
    return None

@router.patch("/{t_id}/status")
def patch_status(t_id: int, status_data: dict, db: Session = Depends(database.get_db)):
    if status_data.get("status") not in ["ToDo", "Done"]:
        raise HTTPException(status_code=400)
    return {"status": "ok"}