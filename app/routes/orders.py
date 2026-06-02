from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import get_db

from app.schemas.order_schemas import (
    OrderCreate,
    OrderUpdate,
    OrderStatusUpdate
)

router = APIRouter()


# CREATE ORDER

@router.post("/orders")
def create_order(
    payload: OrderCreate,
    db=Depends(get_db)
):

    try:

        # VALIDATION

        if payload.subtotal <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subtotal must be greater than 0"
            )

        if payload.total_amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Total amount must be greater than 0"
            )

        query = text("""
            EXEC Reztro.CreateOrder
                @customer_id = :customer_id,
                @order_type = :order_type,
                @subtotal = :subtotal,
                @tax_amount = :tax_amount,
                @discount_amount = :discount_amount,
                @total_amount = :total_amount
        """)

        db.execute(query, {
            "customer_id": payload.customer_id,
            "order_type": payload.order_type,
            "subtotal": payload.subtotal,
            "tax_amount": payload.tax_amount,
            "discount_amount": payload.discount_amount,
            "total_amount": payload.total_amount
        })

        db.commit()

        return {
            "success": True,
            "message": "Order created successfully"
        }

    except HTTPException as e:
        raise e

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# GET ALL ORDERS

@router.get("/orders")
def get_orders(
    db=Depends(get_db)
):

    try:

        query = text("""
            EXEC Reztro.GetOrders
        """)

        result = db.execute(query)

        orders = result.mappings().all()

        return {
            "success": True,
            "count": len(orders),
            "data": orders
        }

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# GET ORDER BY ID

@router.get("/orders/{order_id}")
def get_order_by_id(
    order_id: int,
    db=Depends(get_db)
):

    try:

        query = text("""
            EXEC Reztro.GetOrderById
                @order_id = :order_id
        """)

        result = db.execute(query, {
            "order_id": order_id
        })

        order = result.mappings().first()

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        return {
            "success": True,
            "data": order
        }

    except HTTPException as e:
        raise e

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# UPDATE ORDER

@router.put("/orders/{order_id}")
def update_order(
    order_id: int,
    payload: OrderUpdate,
    db=Depends(get_db)
):

    try:

        if payload.subtotal <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subtotal must be greater than 0"
            )

        if payload.total_amount <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Total amount must be greater than 0"
            )

        query = text("""
            EXEC Reztro.UpdateOrder
                @order_id = :order_id,
                @customer_id = :customer_id,
                @order_type = :order_type,
                @order_status = :order_status,
                @subtotal = :subtotal,
                @tax_amount = :tax_amount,
                @discount_amount = :discount_amount,
                @total_amount = :total_amount
        """)

        db.execute(query, {
            "order_id": order_id,
            "customer_id": payload.customer_id,
            "order_type": payload.order_type,
            "order_status": payload.order_status,
            "subtotal": payload.subtotal,
            "tax_amount": payload.tax_amount,
            "discount_amount": payload.discount_amount,
            "total_amount": payload.total_amount
        })

        db.commit()

        return {
            "success": True,
            "message": "Order updated successfully"
        }

    except HTTPException as e:
        raise e

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# UPDATE ORDER STATUS

@router.patch("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db=Depends(get_db)
):

    try:    
        valid_status = [
            "On Process",
            "Completed",
            "Cancelled"
        ]

        if payload.order_status not in valid_status:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid order status"
            )

        query = text("""
            EXEC Reztro.UpdateOrderStatus
                @order_id = :order_id,
                @order_status = :order_status
        """)

        db.execute(query, {
            "order_id": order_id,
            "order_status": payload.order_status
        })

        db.commit()

        return {
            "success": True,
            "message": "Order status updated successfully"
        }

    except HTTPException as e:
        raise e

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# DELETE / CANCEL ORDER

@router.delete("/orders/{order_id}")
def delete_order(
    order_id: int,
    db=Depends(get_db)
):

    try:

        query = text("""
            EXEC Reztro.DeleteOrder
                @order_id = :order_id
        """)

        db.execute(query, {
            "order_id": order_id
        })

        db.commit()

        return {
            "success": True,
            "message": "Order cancelled successfully"
        }

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )