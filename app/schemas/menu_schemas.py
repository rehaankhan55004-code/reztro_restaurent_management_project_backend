from pydantic import BaseModel
from decimal import Decimal


class MenuItemCreate(BaseModel):

    category_id: int
    name: str
    image_url: str | None = None
    price: Decimal
    rating: Decimal = 0
    description: str | None = None
    values_text: str | None = None

    is_featured: bool = False
    is_top_rated: bool = False
    is_recommended: bool = False
    is_new: bool = False


class MenuItemUpdate(BaseModel):

    category_id: int
    name: str
    image_url: str | None = None
    price: Decimal
    rating: Decimal = 0
    description: str | None = None
    values_text: str | None = None

    is_featured: bool = False
    is_top_rated: bool = False
    is_recommended: bool = False
    is_new: bool = False


class MenuAvailabilityUpdate(BaseModel):

    is_available: bool


class MenuStatsUpdate(BaseModel):

    rating: Decimal
    total_reviews: int
    total_orders: int
    favorites_count: int