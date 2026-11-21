from fastapi import Depends, FastAPI, HTTPException
from database import engine, Base
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from database import get_db
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

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@app.post("/register")
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(user.password)
    
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        phone=user.phone
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id,
        "name": new_user.name,
        "email": new_user.email
    }

@app.post("/login")
def login_user(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    # Find user by email
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()

    # Check if user exists
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password")

    # Verify password
    if not pwd_context.verify(
        user.password,
        existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful",
        "user_id": existing_user.id,
        "name": existing_user.name,
        "email": existing_user.email
    }