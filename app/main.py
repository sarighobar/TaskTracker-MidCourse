from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .database import engine, Base
from . import models
from .routers import router

# Initialize the actual database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# Connect the endpoints defined in routers.py
app.include_router(router)

@app.get("/")
async def read_index():
    return FileResponse("frontend/index.html")

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok"}