from fastapi import (
    HTTPException,
    status
)

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


# ORDERS

def create_order_service(
    db,
    payload
):

    try:

        result = db.execute(
            text("""
                EXEC Reztro.CreateOrder
                    @customer_id=:customer_id,
                    @order_type=:order_type
            """),
            payload.model_dump()
        )

        order = result.mappings().first()

        db.commit()

        return order

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


def get_orders_service(
    db
):

    try:

        result = db.execute(
            text("EXEC Reztro.GetOrders")
        )

        return result.mappings().all()

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


def get_order_by_id_service(
    db,
    order_id: int
):

    try:

        result = db.execute(
            text("""
                EXEC Reztro.GetOrderById
                    @order_id=:order_id
            """),
            {
                "order_id": order_id
            }
        )

        order = result.mappings().first()

        if not order:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )

        return order

    except HTTPException:
        raise

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


def update_order_service(
    db,
    order_id,
    payload
):

    try:

        db.execute(
            text("""
                EXEC Reztro.UpdateOrder
                    @order_id=:order_id,
                    @customer_id=:customer_id,
                    @order_type=:order_type,
                    @order_status=:order_status
            """),
            {
                "order_id": order_id,
                "customer_id": payload.customer_id,
                "order_type": payload.order_type,
                "order_status": payload.order_status
            }
        )

        db.commit()

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


def update_order_status_service(
    db,
    order_id,
    payload
):

    try:

        db.execute(
            text("""
                EXEC Reztro.UpdateOrderStatus
                    @order_id=:order_id,
                    @order_status=:order_status
            """),
            {
                "order_id": order_id,
                "order_status": payload.order_status
            }
        )

        db.commit()

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


def delete_order_service(
    db,
    order_id
):

    try:

        db.execute(
            text("""
                EXEC Reztro.DeleteOrder
                    @order_id=:order_id
            """),
            {
                "order_id": order_id
            }
        )

        db.commit()

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


# ============================================
# ORDER ITEMS
# ============================================

def add_order_item_service(
    db,
    payload
):

    try:

        db.execute(
            text("""
                EXEC Reztro.AddOrderItem
                    @order_id=:order_id,
                    @menu_id=:menu_id,
                    @quantity=:quantity,
                    @notes=:notes
            """),
            payload.model_dump()
        )

        db.commit()

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


def get_order_items_service(
    db
):

    try:

        result = db.execute(
            text("""
                EXEC Reztro.GetOrderItems
            """)
        )

        return result.mappings().all()

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


def get_order_items_by_order_id_service(
    db,
    order_id
):

    try:

        result = db.execute(
            text("""
                EXEC Reztro.GetOrderItemsByOrderId
                    @order_id=:order_id
            """),
            {
                "order_id": order_id
            }
        )

        return result.mappings().all()

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


def get_order_item_by_id_service(
    db,
    order_item_id
):

    try:

        result = db.execute(
            text("""
                EXEC Reztro.GetOrderItemById
                    @order_item_id=:order_item_id
            """),
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

        return item

    except HTTPException:
        raise

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


def update_order_item_service(
    db,
    order_item_id,
    payload
):

    try:

        db.execute(
            text("""
                EXEC Reztro.UpdateOrderItem
                    @order_item_id=:order_item_id,
                    @menu_id=:menu_id,
                    @quantity=:quantity,
                    @notes=:notes
            """),
            {
                "order_item_id": order_item_id,
                "menu_id": payload.menu_id,
                "quantity": payload.quantity,
                "notes": payload.notes
            }
        )

        db.commit()

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


def delete_order_item_service(
    db,
    order_item_id
):

    try:

        db.execute(
            text("""
                EXEC Reztro.DeleteOrderItem
                    @order_item_id=:order_item_id
            """),
            {
                "order_item_id": order_item_id
            }
        )

        db.commit()

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )