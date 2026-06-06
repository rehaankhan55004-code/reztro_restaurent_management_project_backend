from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import get_db
from app.schemas.customer_schemas import (
    CustomerCreate,
    CustomerUpdate
)

router = APIRouter()


# ADD CUSTOMER

@router.post("/customers")
def add_customer(
    payload: CustomerCreate,
    db=Depends(get_db)
):

    try:

        if len(payload.full_name.strip()) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Full name must be at least 3 characters"
            )

        query = text("""
            EXEC Reztro.AddCustomer
                @full_name = :full_name,
                @email = :email,
                @phone = :phone,
                @profile_image_url = :profile_image_url
        """)

        result = db.execute(
            query,
            {
                "full_name": payload.full_name,
                "email": payload.email,
                "phone": payload.phone,
                "profile_image_url": payload.profile_image_url
            }
        )

        customer = result.mappings().first()

        db.commit()

        return {
            "success": True,
            "message": customer["message"],
            "data": customer
        }

    except HTTPException as e:
        raise e

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )

# GET ALL CUSTOMERS

@router.get("/customers")
def get_customers(
    db=Depends(get_db)
):

    try:

        query = text("""
            EXEC Reztro.GetCustomers
        """)

        result = db.execute(query)

        customers = result.mappings().all()

        return {
            "success": True,
            "count": len(customers),
            "data": customers
        }

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )

# GET CUSTOMER BY ID

@router.get("/customers/{customer_id}")
def get_customer_by_id(
    customer_id: int,
    db=Depends(get_db)
):

    try:

        query = text("""
            EXEC Reztro.GetCustomerById
                @customer_id = :customer_id
        """)

        result = db.execute(
            query,
            {
                "customer_id": customer_id
            }
        )

        customer = result.mappings().first()

        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        return {
            "success": True,
            "data": customer
        }

    except HTTPException as e:
        raise e

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )

# UPDATE CUSTOMER

@router.put("/customers/{customer_id}")
def update_customer(
    customer_id: int,
    payload: CustomerUpdate,
    db=Depends(get_db)
):

    try:

        if len(payload.full_name.strip()) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Full name must be at least 3 characters"
            )

        query = text("""
            EXEC Reztro.UpdateCustomer
                @customer_id = :customer_id,
                @full_name = :full_name,
                @email = :email,
                @phone = :phone,
                @profile_image_url = :profile_image_url
        """)

        db.execute(
            query,
            {
                "customer_id": customer_id,
                "full_name": payload.full_name,
                "email": payload.email,
                "phone": payload.phone,
                "profile_image_url": payload.profile_image_url
            }
        )

        db.commit()

        return {
            "success": True,
            "message": "Customer updated successfully"
        }

    except HTTPException as e:
        raise e

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )

# DELETE CUSTOMER

@router.delete("/customers/{customer_id}")
def delete_customer(
    customer_id: int,
    db=Depends(get_db)
):

    try:

        query = text("""
            EXEC Reztro.DeleteCustomer
                @customer_id = :customer_id
        """)

        db.execute(
            query,
            {
                "customer_id": customer_id
            }
        )

        db.commit()

        return {
            "success": True,
            "message": "Customer deleted successfully"
        }

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )