from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ==================== CREATE SCHEMA ====================
class AdminCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, description="Plain text password from frontend")
    role: str = Field(default="Admin", pattern="^Admin$")

# ==================== UPDATE SCHEMA ====================
class AdminUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[str] = Field(None, pattern="^Admin$")
    is_active: Optional[bool] = None

# ==================== RESPONSE SCHEMA ====================
class AdminResponse(BaseModel):
    admin_id: int
    cognito_sub: Optional[str] = None
    full_name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

class AdminListResponse(BaseModel):
    admins: list[AdminResponse]