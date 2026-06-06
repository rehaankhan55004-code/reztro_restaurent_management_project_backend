from fastapi import APIRouter, Depends

from app.db.database import get_db

from app.schemas.menu_schemas import (
    MenuItemCreate,
    MenuItemUpdate,
    MenuAvailabilityUpdate,
    MenuStatsUpdate
)

from app.services.menu_service import (
    create_menu_item_service,
    get_menu_items_service,
    get_menu_item_by_id_service,
    update_menu_item_service,
    delete_menu_item_service,
    update_menu_availability_service,
    update_menu_stats_service,
    get_featured_menu_items_service,
    get_top_rated_menu_items_service
)

router = APIRouter(
    prefix="/menu-items",
    tags=["Menu Items"]
)

# CREATE MENU ITEM

@router.post("")
def create_menu_item(
    payload: MenuItemCreate,
    db=Depends(get_db)
):

    create_menu_item_service(
        db,
        payload
    )

    return {
        "success": True,
        "message": "Menu item created successfully"
    }


# GET ALL MENU ITEMS

@router.get("")
def get_menu_items(
    db=Depends(get_db)
):

    items = get_menu_items_service(db)

    return {
        "success": True,
        "count": len(items),
        "data": items
    }


# GET MENU ITEM BY ID

@router.get("/{menu_id}")
def get_menu_item_by_id(
    menu_id: int,
    db=Depends(get_db)
):

    item = get_menu_item_by_id_service(
        db,
        menu_id
    )

    return {
        "success": True,
        "data": item
    }


# UPDATE MENU ITEM

@router.put("/{menu_id}")
def update_menu_item(
    menu_id: int,
    payload: MenuItemUpdate,
    db=Depends(get_db)
):

    update_menu_item_service(
        db,
        menu_id,
        payload
    )

    return {
        "success": True,
        "message": "Menu item updated successfully"
    }


# DELETE MENU ITEM

@router.delete("/{menu_id}")
def delete_menu_item(
    menu_id: int,
    db=Depends(get_db)
):

    delete_menu_item_service(
        db,
        menu_id
    )

    return {
        "success": True,
        "message": "Menu item deleted successfully"
    }


# UPDATE AVAILABILITY

@router.patch("/{menu_id}/availability")
def update_menu_availability(
    menu_id: int,
    payload: MenuAvailabilityUpdate,
    db=Depends(get_db)
):

    update_menu_availability_service(
        db,
        menu_id,
        payload
    )

    return {
        "success": True,
        "message": "Availability updated successfully"
    }


# UPDATE STATS

@router.patch("/{menu_id}/stats")
def update_menu_stats(
    menu_id: int,
    payload: MenuStatsUpdate,
    db=Depends(get_db)
):

    update_menu_stats_service(
        db,
        menu_id,
        payload
    )

    return {
        "success": True,
        "message": "Stats updated successfully"
    }


# FEATURED MENU ITEMS

@router.get("/featured")
def get_featured_menu_items(
    db=Depends(get_db)
):

    items = get_featured_menu_items_service(db)

    return {
        "success": True,
        "count": len(items),
        "data": items
    }


# TOP RATED MENU ITEMS

@router.get("/top-rated")
def get_top_rated_menu_items(
    db=Depends(get_db)
):

    items = get_top_rated_menu_items_service(db)

    return {
        "success": True,
        "count": len(items),
        "data": items
    }