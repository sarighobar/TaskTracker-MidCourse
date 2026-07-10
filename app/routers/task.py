from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, database

router = APIRouter(prefix="/tasks", tags=["tasks"])

activity_log: List[dict] = []


def _append_activity(action: str, details: str):
    activity_log.append({
        "action": action,
        "details": details,
        "timestamp": datetime.utcnow().isoformat(timespec="seconds")
    })


@router.post("", response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    # Clean tags: split by comma, strip whitespace, join back
    if task.tags:
        tags_list = [t.strip() for t in task.tags.split(",")]
        task.tags = ",".join(tags_list)
        
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    _append_activity("Task Created", f"Created task '{db_task.title}'")
    return db_task

@router.get("", response_model=List[schemas.Task])
def get_all_tasks(
    status: Optional[str] = None,
    search: Optional[str] = None,
    priority_filter: Optional[str] = None,
    overdue_only: Optional[bool] = None,
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Task)

    if status:
        query = query.filter(models.Task.status == status)

    if priority_filter:
        query = query.filter(models.Task.priority == priority_filter)

    if overdue_only:
        query = query.filter(models.Task.due_date.is_not(None)).filter(models.Task.due_date < date.today())

    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (models.Task.title.ilike(search_filter)) |
            (models.Task.tags.ilike(search_filter))
        )

    return query.all()


@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    _append_activity("Task Updated", f"Updated task '{task.title}' to {task.status}")
    return task

@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    _append_activity("Task Deleted", f"Deleted task '{task.title}'")
    return {"message": "Task deleted"}


@router.get("/global/activity")
def get_activity_logs():
    return list(reversed(activity_log[-10:]))