from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="ToDo")      # ToDo, InProgress, Done
    priority = Column(String, default="Medium")  # Low, Medium, High
    assignee = Column(String, nullable=True)
    tags = Column(String, nullable=True, default="")  # Comma-separated tags (e.g. "bug,ui")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)