from pydantic import BaseModel, Field
from typing import Optional

class TaskBase(BaseModel):
    # Set both fields as optional here so Pydantic never fails validation
    title: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = ""
    status: str = "To Do"
    priority: str = "Medium"
    tags: Optional[str] = ""
    due_date: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    status: str

class TaskResponse(BaseModel):
    id: int
    title: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = ""
    status: str
    priority: str
    tags: Optional[str] = ""
    due_date: Optional[str] = None

    class Config:
        from_attributes = True
        populate_by_name = True