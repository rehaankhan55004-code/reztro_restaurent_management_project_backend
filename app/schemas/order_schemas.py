from pydantic import BaseModel
from typing import Literal


# ============================================
# CREATE ORDER
# ============================================

class OrderCreate(BaseModel):

    customer_id: int

    order_type: Literal[
        "Dine-In",
        "Takeaway",
        "Online"
    ]


# ============================================
# UPDATE ORDER
# ============================================

class OrderUpdate(BaseModel):

    customer_id: int

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


# ============================================
# UPDATE ORDER STATUS
# ============================================

class OrderStatusUpdate(BaseModel):

    order_status: Literal[
        "On Process",
        "Completed",
        "Cancelled"
    ]