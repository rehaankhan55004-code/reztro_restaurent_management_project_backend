from decimal import Decimal

from pydantic import (
    BaseModel,
    Field,
)


class MenuItemCreate(BaseModel):

    category_id: int = Field(..., gt=0)

    name: str = Field(
        ...,
        min_length=2,
        max_length=150
    )

    image_url: str | None = Field(
        None,
        max_length=500
    )

    price: Decimal = Field(..., gt=0)

    rating: Decimal = Field(
        default=0,
        ge=0,
        le=5
    )

    description: str | None = Field(
        None,
        max_length=1000
    )

    values_text: str | None = Field(
        None,
        max_length=500
    )

    is_featured: bool = False
    is_top_rated: bool = False
    is_recommended: bool = False
    is_new: bool = False


class MenuItemUpdate(MenuItemCreate):
    pass


class MenuAvailabilityUpdate(BaseModel):

    is_available: bool


class MenuStatsUpdate(BaseModel):

    rating: Decimal = Field(
        ...,
        ge=0,
        le=5
    )

    total_reviews: int = Field(
        ...,
        ge=0
    )

    total_orders: int = Field(
        ...,
        ge=0
    )

    favorites_count: int = Field(
        ...,
        ge=0
    )