from pydantic import BaseModel, Field, field_validator
from typing import Optional


# ✅ CREATE REVIEW
class ReviewCreateSchema(BaseModel):
    customer_id: int = Field(..., gt=0)
    menu_id: int = Field(..., gt=0)

    rating: float = Field(..., ge=0, le=5)

    comment: Optional[str] = Field(None, max_length=1000)

    food_quality: Optional[float] = Field(None, ge=0, le=5)
    service: Optional[float] = Field(None, ge=0, le=5)
    ambiance: Optional[float] = Field(None, ge=0, le=5)
    value_for_money: Optional[float] = Field(None, ge=0, le=5)
    cleanliness: Optional[float] = Field(None, ge=0, le=5)

    review_type: Optional[str] = "Positive"

    @field_validator("review_type")
    @classmethod
    def validate_review_type(cls, v):
        if v not in ["Positive", "Negative", "Neutral"]:
            raise ValueError("review_type must be Positive, Negative, or Neutral")
        return v


class ReviewUpdateSchema(BaseModel):
    rating: float = Field(..., ge=0, le=5)

    comment: Optional[str] = Field(None, max_length=1000)

    food_quality: Optional[float] = Field(None, ge=0, le=5)
    service: Optional[float] = Field(None, ge=0, le=5)
    ambiance: Optional[float] = Field(None, ge=0, le=5)
    value_for_money: Optional[float] = Field(None, ge=0, le=5)
    cleanliness: Optional[float] = Field(None, ge=0, le=5)

    review_type: Optional[str] = "Positive"

    @field_validator("review_type")
    @classmethod
    def validate_review_type(cls, v):
        if v not in ["Positive", "Negative", "Neutral"]:
            raise ValueError("review_type must be Positive, Negative, or Neutral")
        return v