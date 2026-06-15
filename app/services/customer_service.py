from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.utils.cloudinary import upload_to_cloudinary


def create_customer_service(db, payload, file=None):

    try:

        profile_image_url = None

        if file:
            upload_result = upload_to_cloudinary(file)
            profile_image_url = upload_result["url"]

        result = db.execute(
            text("""
                EXEC Reztro.AddCustomer
                    @full_name = :full_name,
                    @email = :email,
                    @phone = :phone,
                    @address = :address,
                    @profile_image_url = :profile_image_url
            """),
            {
                **payload.model_dump(),
                "profile_image_url": profile_image_url
            }
        )

        customer = result.mappings().first()

        db.commit()

        return customer

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )

def get_customers_service(db):

    try:

        result = db.execute(
            text("""
                EXEC Reztro.GetCustomers
            """)
        )

        return result.mappings().all()

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )


def get_customer_by_id_service(db, customer_id: int):

    try:

        result = db.execute(
            text("""
                EXEC Reztro.GetCustomerById
                    @customer_id = :customer_id
            """),
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

        return customer

    except HTTPException:
        raise

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )


def update_customer_service(
    db,
    customer_id: int,
    payload
):

    try:

        db.execute(
            text("""
                EXEC Reztro.UpdateCustomer
                    @customer_id = :customer_id,
                    @full_name = :full_name,
                    @email = :email,
                    @phone = :phone,
                    @address = :address,
                    @profile_image_url = :profile_image_url
            """),
            {
                "customer_id": customer_id,
                **payload.model_dump()
            }
        )

        db.commit()

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )


def delete_customer_service(
    db,
    customer_id: int
):

    try:

        db.execute(
            text("""
                EXEC Reztro.DeleteCustomer
                    @customer_id = :customer_id
            """),
            {
                "customer_id": customer_id
            }
        )

        db.commit()

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )