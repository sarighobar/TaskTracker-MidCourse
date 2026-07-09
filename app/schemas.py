from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "To Do"
    priority: str
    tags: Optional[str] = None
    due_date: Optional[date] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    assignee: Optional[str] = "Unassigned"
    
    model_config = ConfigDict(from_attributes=True)