from fastapi import FastAPI, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator
from typing import Optional, List

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
        # Strip whitespaces around comma-separated tags, eliminate empty strings
        cleaned = [tag.strip() for tag in v.split(",") if tag.strip()]
        return ",".join(cleaned)


@app.get("/")
async def read_index():
    return FileResponse("Frontend/index.html")


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok"}


@app.post("/api/tasks/", status_code=status.HTTP_201_CREATED)
async def create_task(task: Task):
    global id_counter
    task_data = task.model_dump()
    task_data["id"] = id_counter
    tasks_db.append(task_data)
    id_counter += 1
    return task_data


@app.get("/api/tasks/")
async def get_tasks(
    status: Optional[str] = None, 
    priority: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None
):
    results = tasks_db
    
    # 1. Filter by Status if requested
    if status:
        results = [t for t in results if t.get("status") == status]
        
    # 2. Filter by Priority if requested
    if priority:
        results = [t for t in results if t.get("priority") == priority]

    # 3. Filter by Tag if requested
    if tag:
        tag_lower = tag.lower()
        results = [
            t for t in results 
            if tag_lower in [tg.strip().lower() for tg in t.get("tags", "").split(",") if tg.strip()]
        ]
        
    # 4. Multi-column Search across Title & Description
    if search:
        search_lower = search.lower()
        results = [
            t for t in results 
            if search_lower in t.get("title", "").lower() or 
               search_lower in t.get("description", "").lower()
        ]
        
    return results


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
            # If tags are updated, normalize them
            if "tags" in task_update and task_update["tags"]:
                tags_clean = [tg.strip() for tg in task_update["tags"].split(",") if tg.strip()]
                task_update["tags"] = ",".join(tags_clean)
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