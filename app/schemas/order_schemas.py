from typing import Literal

from pydantic import (
    BaseModel,
    Field
)


class OrderItemPayload(BaseModel):

    menu_id: int = Field(..., gt=0)

    quantity: int = Field(
        ...,
        gt=0
    )

    notes: str | None = Field(
        None,
        max_length=500
    )


class OrderCreate(BaseModel):

    customer_id: int = Field(..., gt=0)

    order_type: Literal[
        "Dine-In",
        "Takeaway",
        "Online"
    ]

    items: list[OrderItemPayload] = []


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