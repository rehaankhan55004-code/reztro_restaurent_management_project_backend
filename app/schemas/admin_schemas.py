from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RegisterAdminSchema(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)

    email: str = Field(..., min_length=5, max_length=150)

    password_hash: str = Field(..., min_length=50, max_length=255)

    role: str = Field(default="Admin")


class UpdateAdminSchema(BaseModel):
    full_name: Optional[str] = Field(default=None, min_length=2, max_length=100)

    email: Optional[str] = Field(default=None, min_length=5, max_length=150)

    role: Optional[str] = Field(default="Admin")

    is_active: Optional[bool] = None


class AdminResponseSchema(BaseModel):
    admin_id: int

    full_name: str

    email: str

    role: str

    is_active: bool

    created_at: datetime

    updated_at: Optional[datetime]