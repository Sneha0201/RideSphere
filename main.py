from fastapi import FastAPI

app = FastAPI(
    title="RideSphere",
    description="Smart Cab Booking Platform",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to RideSphere!",
        "status": "Backend is running successfully"
    }

@app.get("/about")
def about():
    return {
        "project": "RideSphere",
        "technology": "Python FastAPI",
        "features": [
            "User Registration",
            "Cab Booking",
            "Driver Management",
            "Fare Estimation"
        ]
    }