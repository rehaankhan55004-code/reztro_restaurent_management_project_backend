from fastapi import APIRouter, Depends

from app.db.database import get_db
from app.schemas.customer_schemas import (
    CustomerCreate,
    CustomerUpdate
)
from app.services.customer_service import (
    create_customer_service,
    get_customers_service,
    get_customer_by_id_service,
    update_customer_service,
    delete_customer_service
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post("")
def create_customer(
    payload: CustomerCreate,
    db=Depends(get_db)
):

    customer = create_customer_service(
        db,
        payload
    )

    return {
        "success": True,
        "message": customer["message"],
        "data": customer
    }


@router.get("")
def get_customers(
    db=Depends(get_db)
):

    customers = get_customers_service(db)

    return {
        "success": True,
        "count": len(customers),
        "data": customers
    }


@router.get("/{customer_id}")
def get_customer_by_id(
    customer_id: int,
    db=Depends(get_db)
):

    customer = get_customer_by_id_service(
        db,
        customer_id
    )

    return {
        "success": True,
        "data": customer
    }


@router.put("/{customer_id}")
def update_customer(
    customer_id: int,
    payload: CustomerUpdate,
    db=Depends(get_db)
):

    update_customer_service(
        db,
        customer_id,
        payload
    )

    return {
        "success": True,
        "message": "Customer updated successfully"
    }


@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db=Depends(get_db)
):

    delete_customer_service(
        db,
        customer_id
    )

    return {
        "success": True,
        "message": "Customer deleted successfully"
    }