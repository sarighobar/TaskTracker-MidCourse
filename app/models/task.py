from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default="To Do") # To Do, In Progress, Done
    priority = Column(String, default="Medium") # Low, Medium, High
    assignee = Column(String, default="Unassigned")
    tags = Column(String, nullable=True)
    due_date = Column(String, nullable=True) # Formatted YYYY-MM-DD

    # Relationships
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    text = Column(String, nullable=False)
    timestamp = Column(String, default=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    task = relationship("Task", back_populates="comments")

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, nullable=True)
    action = Column(String, nullable=False) # CREATE, UPDATE, DELETE, STATUS_CHANGE
    details = Column(String, nullable=False)
    timestamp = Column(String, default=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))