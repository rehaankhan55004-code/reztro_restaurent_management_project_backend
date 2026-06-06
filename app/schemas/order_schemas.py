from typing import Literal

from pydantic import (
    BaseModel,
    Field
)


class OrderCreate(BaseModel):

    customer_id: int = Field(..., gt=0)

    order_type: Literal[
        "Dine-In",
        "Takeaway",
        "Online"
    ]


class OrderUpdate(BaseModel):

    customer_id: int = Field(..., gt=0)

    order_type: Literal[
        "Dine-In",
        "Takeaway",
        "Online"
    ]

    order_status: Literal[
        "On Process",
        "Completed",
        "Cancelled"
    ]


class OrderStatusUpdate(BaseModel):

    order_status: Literal[
        "On Process",
        "Completed",
        "Cancelled"
    ]