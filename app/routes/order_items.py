from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import get_db

from app.schemas.order_item_schemas import (
    OrderItemCreate,
    OrderItemUpdate
)

router = APIRouter()

# ADD ORDER ITEM

@router.post("/order-items")
def add_order_item(
    payload: OrderItemCreate,
    db=Depends(get_db)
):

    try:

        query = text("""
            EXEC Reztro.AddOrderItem
                @order_id = :order_id,
                @menu_id = :menu_id,
                @quantity = :quantity,
                @notes = :notes
        """)

        db.execute(
            query,
            {
                "order_id": payload.order_id,
                "menu_id": payload.menu_id,
                "quantity": payload.quantity,
                "notes": payload.notes
            }
        )

        db.commit()

        return {
            "success": True,
            "message": "Order item added successfully"
        }

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================
# GET ALL ORDER ITEMS
# ============================================

@router.get("/order-items")
def get_order_items(
    db=Depends(get_db)
):

    try:

        query = text("""
            EXEC Reztro.GetOrderItems
        """)

        result = db.execute(query)

        items = result.mappings().all()

        return {
            "success": True,
            "count": len(items),
            "data": items
        }

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================
# GET ORDER ITEMS BY ORDER ID
# ============================================

@router.get("/orders/{order_id}/items")
def get_order_items_by_order_id(
    order_id: int,
    db=Depends(get_db)
):

    try:

        query = text("""
            EXEC Reztro.GetOrderItemsByOrderId
                @order_id = :order_id
        """)

        result = db.execute(
            query,
            {
                "order_id": order_id
            }
        )

        items = result.mappings().all()

        return {
            "success": True,
            "count": len(items),
            "data": items
        }

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================
# GET ORDER ITEM BY ID
# ============================================

@router.get("/order-items/{order_item_id}")
def get_order_item_by_id(
    order_item_id: int,
    db=Depends(get_db)
):

    try:

        query = text("""
            EXEC Reztro.GetOrderItemById
                @order_item_id = :order_item_id
        """)

        result = db.execute(
            query,
            {
                "order_item_id": order_item_id
            }
        )

        item = result.mappings().first()

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order item not found"
            )

        return {
            "success": True,
            "data": item
        }

    except HTTPException as e:
        raise e

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================
# UPDATE ORDER ITEM
# ============================================

@router.put("/order-items/{order_item_id}")
def update_order_item(
    order_item_id: int,
    payload: OrderItemUpdate,
    db=Depends(get_db)
):

    try:

        query = text("""
            EXEC Reztro.UpdateOrderItem
                @order_item_id = :order_item_id,
                @menu_id = :menu_id,
                @quantity = :quantity,
                @notes = :notes
        """)

        db.execute(
            query,
            {
                "order_item_id": order_item_id,
                "menu_id": payload.menu_id,
                "quantity": payload.quantity,
                "notes": payload.notes
            }
        )

        db.commit()

        return {
            "success": True,
            "message": "Order item updated successfully"
        }

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================
# DELETE ORDER ITEM
# ============================================

@router.delete("/order-items/{order_item_id}")
def delete_order_item(
    order_item_id: int,
    db=Depends(get_db)
):

    try:

        query = text("""
            EXEC Reztro.DeleteOrderItem
                @order_item_id = :order_item_id
        """)

        db.execute(
            query,
            {
                "order_item_id": order_item_id
            }
        )

        db.commit()

        return {
            "success": True,
            "message": "Order item deleted successfully"
        }

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )