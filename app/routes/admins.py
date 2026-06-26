from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.admin_schemas import (
    RegisterAdminSchema,
    UpdateAdminSchema,
)

from app.services.admin_service import (
    register_admin_service,
    get_all_admins_service,
    get_admin_by_id_service,
    get_admin_by_email_service,
    update_admin_service,
)

router = APIRouter(
    prefix="/admins",
    tags=["Admins"]
)

# REGISTER

@router.post("")
def register_admin(
    payload: RegisterAdminSchema,
    db: Session = Depends(get_db)
):
    result = register_admin_service(db, payload)

    return {
        "success": True,
        "message": "Admin registered successfully",
        "data": result
    }


# GET ALL


@router.get("")
def get_all_admins(
    db: Session = Depends(get_db)
):
    return {
        "success": True,
        "data": get_all_admins_service(db)
    }


# GET BY EMAIL


@router.get("/email/{email}")
def get_admin_by_email(
    email: str,
    db: Session = Depends(get_db)
):
    return {
        "success": True,
        "data": get_admin_by_email_service(db, email)
    }


# GET BY ID


@router.get("/{admin_id}")
def get_admin_by_id(
    admin_id: int,
    db: Session = Depends(get_db)
):
    return {
        "success": True,
        "data": get_admin_by_id_service(db, admin_id)
    }


# UPDATE


@router.put("/{admin_id}")
def update_admin(
    admin_id: int,
    payload: UpdateAdminSchema,
    db: Session = Depends(get_db)
):
    result = update_admin_service(db, admin_id, payload)

    return {
        "success": True,
        "message": "Admin updated successfully",
        "data": result
    }