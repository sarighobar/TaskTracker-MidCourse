from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.routers import task
from app.database import engine
from app import models as task_model

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_PATH = BASE_DIR / "index.html"

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

@app.get("/", response_class=HTMLResponse)
def system_root_check():
    return INDEX_PATH.read_text(encoding="utf-8")