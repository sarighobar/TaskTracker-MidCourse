from pydantic import BaseModel, field_validator
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "ToDo"
    priority: Optional[str] = "Medium"
    assignee: Optional[str] = None
    tags: Optional[str] = ""

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Title cannot be blank or empty.")
        return v.strip()

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, v: Optional[str]) -> str:
        if not v:
            return ""
        # Split tags by commas, clean spaces, and remove empty strings
        cleaned = [t.strip() for t in v.split(",") if t.strip()]
        return ",".join(cleaned)

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assignee: Optional[str] = None
    tags: Optional[str] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not v or not v.strip()):
            raise ValueError("Title cannot be blank or empty.")
        return v.strip() if v else v

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        cleaned = [t.strip() for t in v.split(",") if t.strip()]
        return ",".join(cleaned)

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    assignee: Optional[str] = None
    tags: str

    class Config:
        from_attributes = True