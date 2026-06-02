from pydantic import BaseModel
from decimal import Decimal


# ============================================
# CREATE ORDER
# ============================================

class OrderCreate(BaseModel):

    customer_id: int

    order_type: str

    subtotal: Decimal

    tax_amount: Decimal = 0

    discount_amount: Decimal = 0

    total_amount: Decimal


# ============================================
# UPDATE ORDER
# ============================================

class OrderUpdate(BaseModel):

    customer_id: int

    order_type: str

    order_status: str

    subtotal: Decimal

    tax_amount: Decimal = 0

    discount_amount: Decimal = 0

    total_amount: Decimal


# ============================================
# UPDATE ORDER STATUS
# ============================================

class OrderStatusUpdate(BaseModel):

    order_status: str