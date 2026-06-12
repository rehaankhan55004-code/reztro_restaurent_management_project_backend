from fastapi import (
    APIRouter,
    Depends
)

from app.db.database import get_db

from app.schemas.online_order_schemas import (
    OnlineOrderUpdate
)

from app.services.online_order_service import (
    get_online_orders_service,
    get_online_order_by_id_service,
    get_online_order_by_order_id_service,
    update_online_order_service,
    delete_online_order_service
)

router = APIRouter(
    prefix="/online-orders",
    tags=["Online Orders"]
)


@router.get("")
def get_online_orders(
    db=Depends(get_db)
):

    orders = get_online_orders_service(db)

    return {
        "success": True,
        "count": len(orders),
        "data": orders
    }


@router.get("/{online_order_id}")
def get_online_order_by_id(
    online_order_id: int,
    db=Depends(get_db)
):

    order = get_online_order_by_id_service(
        db,
        online_order_id
    )

    return {
        "success": True,
        "data": order
    }


@router.get("/order/{order_id}")
def get_online_order_by_order_id(
    order_id: int,
    db=Depends(get_db)
):

    order = get_online_order_by_order_id_service(
        db,
        order_id
    )

    return {
        "success": True,
        "data": order
    }


@router.put("/{online_order_id}")
def update_online_order(
    online_order_id: int,
    payload: OnlineOrderUpdate,
    db=Depends(get_db)
):

    update_online_order_service(
        db,
        online_order_id,
        payload
    )

    return {
        "success": True,
        "message": "Online order details updated successfully"
    }


@router.delete("/{online_order_id}")
def delete_online_order(
    online_order_id: int,
    db=Depends(get_db)
):

    delete_online_order_service(
        db,
        online_order_id
    )

    return {
        "success": True,
        "message": "Online order details deleted successfully"
    }