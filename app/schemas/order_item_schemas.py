from pydantic import BaseModel

# CREATE ORDER ITEM

class OrderItemCreate(BaseModel):

    order_id: int
    menu_id: int
    quantity: int
    notes: str | None = None


# UPDATE ORDER ITEM

class OrderItemUpdate(BaseModel):

    menu_id: int
    quantity: int
    notes: str | None = None