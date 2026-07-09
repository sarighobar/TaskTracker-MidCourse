from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import task  # Changed from tasks to task
from app.database import engine
from app.models import task as task_model  

task_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Tracker Enterprise API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connects your route pathway to the app core
app.include_router(task.router)

@app.get("/")
def system_root_check():
    return {"status": "Online", "engine": "FastAPI Structured Core"}