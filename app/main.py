from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator
from typing import Optional

app = FastAPI()

# Enable CORS for frontend workspace communication
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

tasks_db = []
id_counter = 1

class Task(BaseModel):
    title: str
    description: Optional[str] = ""
    priority: Optional[str] = "Medium"
    status: str = "ToDo"
    tags: Optional[str] = ""
    assignee: Optional[str] = ""

    @field_validator("title")
    def title_must_not_be_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError("Title cannot be empty")
        return v

    @field_validator("tags")
    def normalize_tags(cls, v):
        if not v: 
            return ""
        # Strip trailing whitespaces around comma-separated tags
        return ",".join([tag.strip() for tag in v.split(",") if tag.strip()])


@app.get("/")
async def read_index():
    return FileResponse("Frontend/index.html")


@app.post("/api/tasks/", status_code=status.HTTP_201_CREATED)
async def create_task(task: Task):
    global id_counter
    task_data = task.model_dump()
    task_data["id"] = id_counter
    tasks_db.append(task_data)
    id_counter += 1
    return task_data


# UPDATED: Implements ADR 001 optional status filtering parameter
@app.get("/api/tasks/")
async def get_tasks(status: Optional[str] = None):
    if status:
        return [t for t in tasks_db if t["status"] == status]
    return tasks_db


@app.get("/api/tasks/{task_id}")
async def get_single_task(task_id: int):
    for t in tasks_db:
        if t["id"] == task_id:
            return t
    raise HTTPException(status_code=404, detail="Task not found")


@app.put("/api/tasks/{task_id}")
async def update_task(task_id: int, task_update: dict):
    for t in tasks_db:
        if t["id"] == task_id:
            t.update(task_update)
            return t
    raise HTTPException(status_code=404, detail="Task not found")


@app.patch("/api/tasks/{task_id}/status")
async def update_status(task_id: int, update: dict):
    valid_statuses = ["ToDo", "InProgress", "Done"]
    new_status = update.get("status")
    
    if new_status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
        
    for t in tasks_db:
        if t["id"] == task_id:
            t["status"] = new_status
            return t
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/api/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    for i, t in enumerate(tasks_db):
        if t["id"] == task_id:
            tasks_db.pop(i)
            return None
    raise HTTPException(status_code=404, detail="Task not found")