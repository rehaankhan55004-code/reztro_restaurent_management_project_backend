import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    # Check if admin already exists
    existing = db.execute(
        text("SELECT admin_id FROM Reztro.Admins WHERE email = :email"),
        {"email": payload.email}
    ).fetchone()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin with this email already exists."
        )

    # Hash the password securely using bcrypt
    password_hash = bcrypt.hashpw(payload.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    local_sub = f"local-sub-{payload.email}"

    # Call your Reztro stored procedure to register the admin
    try:
        db.execute(
            text("""
                EXEC Reztro.RegisterAdmin
                    @full_name=:full_name,
                    @email=:email,
                    @password_hash=:password_hash,
                    @cognito_sub=:cognito_sub,
                    @role='Admin'
            """),
            {
                "full_name": payload.name,
                "email": payload.email,
                "password_hash": password_hash,
                "cognito_sub": local_sub
            }
        )
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(getattr(e, "orig", e)))

    # Fetch the newly created admin record for the response
    admin_record = db.execute(
        text("SELECT admin_id, full_name, email FROM Reztro.Admins WHERE email = :email"),
        {"email": payload.email}
    ).mappings().first()

    return {
        "success": True,
        "message": "Admin registered successfully",
        "user": {
            "id": admin_record["admin_id"],
            "name": admin_record["full_name"],
            "email": admin_record["email"]
        }
    }

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    # Query admin from SQL Server Admins table
    admin = db.execute(
        text("SELECT admin_id, full_name, email, password_hash FROM Reztro.Admins WHERE email = :email"),
        {"email": payload.email}
    ).mappings().first()

    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    stored_hash = admin["password_hash"]
    is_valid = False

    try:
        if stored_hash and stored_hash != "COGNITO_MANAGED":
            is_valid = bcrypt.checkpw(payload.password.encode('utf-8'), stored_hash.encode('utf-8'))
    except Exception:
        is_valid = False

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    return {
        "success": True,
        "message": "Login successful",
        "user": {
            "id": admin["admin_id"],
            "name": admin["full_name"],
            "email": admin["email"]
        }
    }