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