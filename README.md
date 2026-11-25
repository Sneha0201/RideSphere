# RideSphere – Smart Cab Booking Platform

## About the Project
RideSphere is a backend-based smart cab booking platform developed using Python and FastAPI. It allows users to register, log in, book rides, view ride details, and manage ride status. Drivers can register and update their availability.

## Technologies Used
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Passlib (Password Hashing)
- Swagger UI

## Main Features
1. User Registration and Login
2. Driver Registration
3. View Available Drivers
4. Update Driver Availability
5. Book a Cab
6. Automatic Fare Calculation
7. View All Rides
8. Update Ride Status
9. Cancel Rides
10. View User-Specific Ride History

## Fare Calculation
The fare is calculated using:

Fare = Base Fare + (Distance × Per KM Rate)

- Base Fare = ₹50
- Per KM Rate = ₹12

## Database Tables
- Users: Stores user details.
- Drivers: Stores driver and vehicle information.
- Rides: Stores booking details, fare and ride status.

## Project Structure
- main.py – API endpoints and application logic
- database.py – Database connection and session management
- models.py – Database models

## How to Run
1. Install the required dependencies.
2. Open the project folder in VS Code.
3. Run the backend using:

`uvicorn main:app --reload`

4. Open Swagger UI:

`http://127.0.0.1:8000/docs`

5. Test the available API endpoints.

## Testing
The backend APIs were tested using Swagger UI. Successful responses (HTTP 200) were received for database connectivity, ride listing, user ride history, driver availability and ride booking.

## Conclusion
RideSphere demonstrates backend development, REST API creation, database management, user authentication, driver management and cab booking operations using Python and FastAPI.