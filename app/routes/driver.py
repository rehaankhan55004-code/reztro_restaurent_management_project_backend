from fastapi import (
    APIRouter,
    Depends
)

from app.db.database import get_db

from app.schemas.driver_schemas import (
    DriverCreate,
    DriverUpdate,
    DriverStatusUpdate
)

from app.services.driver_service import (
    create_driver_service,
    get_drivers_service,
    get_driver_by_id_service,
    update_driver_service,
    update_driver_status_service,
    delete_driver_service
)

router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)


@router.post("")
def create_driver(
    payload: DriverCreate,
    db=Depends(get_db)
):

    create_driver_service(
        db,
        payload
    )

    return {
        "success": True,
        "message": "Driver created successfully"
    }


@router.get("")
def get_drivers(
    db=Depends(get_db)
):

    drivers = get_drivers_service(db)

    return {
        "success": True,
        "count": len(drivers),
        "data": drivers
    }


@router.get("/{driver_id}")
def get_driver_by_id(
    driver_id: int,
    db=Depends(get_db)
):

    driver = get_driver_by_id_service(
        db,
        driver_id
    )

    return {
        "success": True,
        "data": driver
    }


@router.put("/{driver_id}")
def update_driver(
    driver_id: int,
    payload: DriverUpdate,
    db=Depends(get_db)
):

    update_driver_service(
        db,
        driver_id,
        payload
    )

    return {
        "success": True,
        "message": "Driver updated successfully"
    }


@router.patch("/{driver_id}/status")
def update_driver_status(
    driver_id: int,
    payload: DriverStatusUpdate,
    db=Depends(get_db)
):

    update_driver_status_service(
        db,
        driver_id,
        payload
    )

    return {
        "success": True,
        "message": "Driver status updated successfully"
    }


@router.delete("/{driver_id}")
def delete_driver(
    driver_id: int,
    db=Depends(get_db)
):

    delete_driver_service(
        db,
        driver_id
    )

    return {
        "success": True,
        "message": "Driver deleted successfully"
    }