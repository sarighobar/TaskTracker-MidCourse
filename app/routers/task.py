import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task import Task  
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Global memory state array to keep tracking log data light and instant
SYSTEM_ACTIVITY_RECORDS = [
    {
        "action": "SYS INIT",
        "details": "Core tracking engine pipelines synchronized successfully.",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
]

def record_system_event(action: str, details: str):
    """Helper method to inject fresh records to the top of our log pipeline"""
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    SYSTEM_ACTIVITY_RECORDS.insert(0, {
        "action": action,
        "details": details,
        "timestamp": now_str
    })
    # Keep the log stream length clean and optimized
    if len(SYSTEM_ACTIVITY_RECORDS) > 25:
        SYSTEM_ACTIVITY_RECORDS.pop()

@router.get("/global/activity")
def get_global_activity():
    # Returns the dynamically updated system log list
    return SYSTEM_ACTIVITY_RECORDS

@router.get("/", response_model=List[TaskResponse])
def get_all_tasks(
    search: Optional[str] = None, 
    priority_filter: Optional[str] = None, 
    overdue_only: str = "false",
    db: Session = Depends(get_db)
):
    query = db.query(Task)
    today_str = datetime.date.today().isoformat()

    if search:
        query = query.filter(
            (Task.title.ilike(f"%{search}%")) | 
            (Task.description.ilike(f"%{search}%"))
        )
    if priority_filter:
        query = query.filter(Task.priority.ilike(priority_filter))
    if overdue_only == "true":
        query = query.filter(Task.due_date < today_str, Task.status != "Done")

    return query.all()

@router.post("/", response_model=TaskResponse)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    resolved_title = task_in.summary if task_in.summary else task_in.title
    if not resolved_title:
        raise HTTPException(status_code=400, detail="Task title or summary is required.")

    clean_status = task_in.status
    if clean_status.replace(" ", "").lower() in ["todo", "todocolumn"]:
        clean_status = "To Do"

    new_task = Task(
        title=resolved_title,
        description=task_in.description,
        status=clean_status,
        priority=task_in.priority,
        tags=task_in.tags,
        due_date=task_in.due_date
    )
    
    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        
        # 🔔 LIVE LOG CAPTURE: Record creation event
        record_system_event(
            action="TASK CREATED", 
            details=f"New task '{new_task.title}' initialized under column '{new_task.status}'."
        )
        
        return new_task
    except Exception as db_err:
        db.rollback()
        print(f"CRITICAL DATABASE ERROR: {db_err}")
        raise HTTPException(status_code=500, detail=f"Database execution crash: {str(db_err)}")

@router.put("/{task_id}", response_model=TaskResponse)
def update_task_status(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")

    old_status = task.status
    incoming_status = payload.status.replace(" ", "").lower()
    
    if incoming_status in ["todo", "todocolumn"]:
        task.status = "To Do"
    elif incoming_status in ["inprogress", "progress"]:
        task.status = "In Progress"
    else:
        task.status = "Done"

    db.commit()
    db.refresh(task)

    # 🔔 LIVE LOG CAPTURE: Record lifecycle state movement
    record_system_event(
        action="STAGE TRANSITION", 
        details=f"Moved task '{task.title}' out of '{old_status}' into '{task.status}'."
    )

    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    
    task_title = task.title
    db.delete(task)
    db.commit()

    # 🔔 LIVE LOG CAPTURE: Record records deletion tracking event
    record_system_event(
        action="RECORD PURGED", 
        details=f"Task file item '{task_title}' completely deleted from core data registers."
    )

    return {"message": "Success", "id": task_id}