from pydantic import BaseModel, Field


class DineInOrderCreate(BaseModel):

    order_id: int = Field(..., gt=0)

    table_no: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    guest_count: int | None = Field(
        None,
        gt=0
    )


class DineInOrderUpdate(BaseModel):

    table_no: str = Field(
        ...,
        min_length=1,
        max_length=50
    )

    guest_count: int | None = Field(
        None,
        gt=0
    )