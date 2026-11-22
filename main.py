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

class DriverCreate(BaseModel):
    name: str
    vehicle_number: str
    vehicle_type: str

class RideCreate(BaseModel):
    user_id: int
    pickup: str
    destination: str

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

@app.post("/register_driver")
def register_driver(
    driver: DriverCreate,
    db: Session = Depends(get_db)
):
    existing_driver = db.query(models.Driver).filter(models.Driver.vehicle_number == driver.vehicle_number).first()

    if existing_driver:
        raise HTTPException(
            status_code=400,
            detail="Vehicle already registered"
        )

    new_driver = models.Driver(
        name=driver.name,
        vehicle_number=driver.vehicle_number,
        vehicle_type=driver.vehicle_type
    )

    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)

    return {
        "message": "Driver registered successfully",
        "driver_id": new_driver.id,
        "name": new_driver.name,
        "vehicle_number": new_driver.vehicle_number,
        "vehicle_type": new_driver.vehicle_type
    }

@app.get("/drivers")
def get_drivers(db: Session = Depends(get_db)):
    drivers = db.query(models.Driver).all()

    return {
        "total_drivers": len(drivers),
        "drivers": [
            {
                "id": d.id,
                "name": d.name,
                "vehicle_number": d.vehicle_number,
                "vehicle_type": d.vehicle_type,
                "available": d.available
            }
            for d in drivers
        ]
    }

@app.put("/drivers/{driver_id}/availability")
def update_driver_availability(
    driver_id: int,
    available: int,
    db: Session = Depends(get_db)
):
    driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="Driver not found"
        )

    if available not in [0, 1]:
        raise HTTPException(
            status_code=400,
            detail="Availability must be 0 or 1"
        )

    driver.available = available
    db.commit()
    db.refresh(driver)

    return {
        "message": "Driver availability updated",
        "driver_id": driver.id,
        "available": driver.available
    }

@app.post("/book_ride")
def book_ride(ride: RideCreate, db: Session = Depends(get_db)):

    # Check whether user exists
    user = db.query(models.User).filter(models.User.id == ride.user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Find an available driver
    driver = db.query(models.Driver).filter(models.Driver.available == 1).first()

    if not driver:
        raise HTTPException(
            status_code=404,
            detail="No available drivers"
        )

    # Create new ride
    new_ride = models.Ride(
        user_id=ride.user_id,
        driver_id=driver.id,
        pickup=ride.pickup,
        destination=ride.destination,
        fare=0,
        status="booked"
    )

    # Mark driver unavailable
    driver.available = 0
    
    db.add(new_ride)
    db.commit()
    db.refresh(new_ride)

    return {
        "message": "Ride booked successfully",
        "ride_id": new_ride.id,
        "user_id": new_ride.user_id,
        "driver_id": new_ride.driver_id,
        "pickup": new_ride.pickup,
        "destination": new_ride.destination,
        "fare": new_ride.fare,
        "status": new_ride.status
    }

@app.get("/rides")
def get_rides(db: Session = Depends(get_db)):
    rides = db.query(models.Ride).all()

    return {
        "total_rides": len(rides),
        "rides": [
            {
                "id": ride.id,
                "user_id": ride.user_id,
                "driver_id": ride.driver_id,
                "pickup": ride.pickup,
                "destination": ride.destination,
                "fare": ride.fare,
                "status": ride.status
            }
            for ride in rides
        ]
    }

@app.put("/rides/{ride_id}/status")
def update_ride_status(
    ride_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    ride = db.query(models.Ride).filter(models.Ride.id == ride_id).first()

    if not ride:
        raise HTTPException(
            status_code=404,
            detail="Ride not found"
        )

    ride.status = status

    db.commit()
    db.refresh(ride)

    return {
        "message": "Ride status updated successfully",
        "ride_id": ride.id,
        "status": ride.status
    }