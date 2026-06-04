from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class CustomerCreate(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    profile_image_url: Optional[str] = Field(None, max_length=500)


class CustomerUpdate(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    profile_image_url: Optional[str] = Field(None, max_length=500)