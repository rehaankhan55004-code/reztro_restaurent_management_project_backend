from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


def safe_fetch_one(result):
    try:
        return result.mappings().first()
    except Exception:
        return None


# REGISTER


def register_admin_service(db, payload):
    try:

        result = db.execute(
            text("""
                EXEC Reztro.RegisterAdmin
                    @full_name=:full_name,
                    @email=:email,
                    @password_hash=:password_hash,
                    @role=:role
            """),
            payload.model_dump(),
        )

        response = safe_fetch_one(result)

        db.commit()

        return response

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(getattr(e, "orig", e))
        )


# GET ALL


def get_all_admins_service(db):
    try:

        result = db.execute(
            text("""
                EXEC Reztro.GetAllAdmins
            """)
        )

        return result.mappings().all()

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=500,
            detail=str(getattr(e, "orig", e))
        )


# GET BY ID


def get_admin_by_id_service(db, admin_id: int):
    try:

        result = db.execute(
            text("""
                EXEC Reztro.GetAdminById
                    @admin_id=:admin_id
            """),
            {
                "admin_id": admin_id
            },
        )

        data = safe_fetch_one(result)

        if not data:
            raise HTTPException(
                status_code=404,
                detail="Admin not found"
            )

        return data

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=400,
            detail=str(getattr(e, "orig", e))
        )


# GET BY EMAIL


def get_admin_by_email_service(db, email: str):
    try:

        result = db.execute(
            text("""
                EXEC Reztro.GetAdminByEmail
                    @email=:email
            """),
            {
                "email": email
            },
        )

        data = safe_fetch_one(result)

        if not data:
            raise HTTPException(
                status_code=404,
                detail="Admin not found"
            )

        return data

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=400,
            detail=str(getattr(e, "orig", e))
        )


# UPDATE


def update_admin_service(db, admin_id: int, payload):
    try:

        params = payload.model_dump()

        params["admin_id"] = admin_id

        result = db.execute(
            text("""
                EXEC Reztro.UpdateAdmin
                    @admin_id=:admin_id,
                    @full_name=:full_name,
                    @email=:email,
                    @role=:role,
                    @is_active=:is_active
            """),
            params,
        )

        response = safe_fetch_one(result)

        db.commit()

        return response

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(getattr(e, "orig", e))
        )