from datetime import datetime

from pydantic import (
    BaseModel,
    Field
)


class TakeawayOrderCreate(BaseModel):

    order_id: int = Field(..., gt=0)

    pickup_time: datetime | None = None

    pickup_code: str | None = Field(
        None,
        max_length=50
    )


class TakeawayOrderUpdate(BaseModel):

    pickup_time: datetime | None = None

    pickup_code: str | None = Field(
        None,
        max_length=50
    )