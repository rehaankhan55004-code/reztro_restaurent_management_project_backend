from pydantic import BaseModel
from typing import Optional


class CustomerCreate(BaseModel):
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    profile_image_url: Optional[str] = None


class CustomerUpdate(BaseModel):
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    profile_image_url: Optional[str] = None