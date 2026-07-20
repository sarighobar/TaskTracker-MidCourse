from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from . import models, database

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_task(task_data: dict, db: Session = Depends(database.get_db)):
    title = task_data.get("title")
    if not title or not str(title).strip():
        raise HTTPException(status_code=422, detail="Title required")
    
    raw_tags = task_data.get("tags") or ""
    tags_list = [t.strip() for t in raw_tags.split(",") if t.strip()]
    normalized_tags = ",".join(tags_list)

    db_task = models.Task(
        title=title.strip(),
        description=task_data.get("description", ""),
        priority=task_data.get("priority", "Medium"),
        status=task_data.get("status", "ToDo"),
        tags=normalized_tags,
        assignee=task_data.get("assignee", "")
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/")
def get_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Task)

    if status:
        query = query.filter(models.Task.status == status)
    if priority:
        query = query.filter(models.Task.priority == priority)
    if tag:
        tag_lower = f"%{tag.lower()}%"
        query = query.filter(models.Task.tags.ilike(tag_lower))
    if search:
        search_pattern = f"%{search.lower()}%"
        query = query.filter(
            (models.Task.title.ilike(search_pattern)) | 
            (models.Task.description.ilike(search_pattern))
        )

    return query.all()

@router.get("/{t_id}")
def get_task(t_id: int, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == t_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{t_id}")
def update_task(t_id: int, task_data: dict, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == t_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if "tags" in task_data:
        raw_tags = task_data.get("tags") or ""
        tags_clean = [tg.strip() for tg in raw_tags.split(",") if tg.strip()]
        task_data["tags"] = ",".join(tags_clean)

    allowed_fields = {"title", "description", "priority", "status", "tags", "assignee"}
    for key, value in task_data.items():
        if key in allowed_fields:
            setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task

@router.patch("/{t_id}/status")
def patch_status(t_id: int, status_data: dict, db: Session = Depends(database.get_db)):
    valid_statuses = ["ToDo", "InProgress", "Done"]
    new_status = status_data.get("status")

    if new_status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")

    task = db.query(models.Task).filter(models.Task.id == t_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = new_status
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{t_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(t_id: int, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.id == t_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return None