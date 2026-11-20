from fastapi import Depends, FastAPI, HTTPException
from database import engine, Base
import models

app = FastAPI(
    title="RideSphere",
    description="Smart Cab Booking Platform",
    version="1.0.0"
)

# Create Database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {
        "message": "Welcome to RideSphere!",
        "status": "Backend is running successfully"
    }

@app.get("/database-status")
def database_status():
    return {
        "database": "SQLite",
        "status": "Connected",
        "tables": ["users", "drivers", "rides"]
    }