from fastapi import APIRouter, Depends, UploadFile, File, Form

from app.db.database import get_db
from app.utils.cloudinary import upload_to_cloudinary

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
async def create_menu_item(
    category_id: int = Form(...),
    name: str = Form(...),
    price: float = Form(...),
    rating: float = Form(0),
    description: str = Form(None),
    values_text: str = Form(None),
    is_featured: bool = Form(False),
    is_top_rated: bool = Form(False),
    is_recommended: bool = Form(False),
    is_new: bool = Form(False),
    file: UploadFile = File(None),
    db=Depends(get_db)
):
    image_url = None

    if file:
        upload_result = upload_to_cloudinary(file)
        image_url = upload_result["url"]

    payload = MenuItemCreate(
        category_id=category_id,
        name=name,
        image_url=image_url,
        price=price,
        rating=rating,
        description=description,
        values_text=values_text,
        is_featured=is_featured,
        is_top_rated=is_top_rated,
        is_recommended=is_recommended,
        is_new=is_new
    )

    create_menu_item_service(db, payload)

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

from fastapi import UploadFile, File, Form, Depends

from app.utils.cloudinary import upload_to_cloudinary
from app.services.menu_service import (
    update_menu_item_service,
    get_menu_item_by_id_service
)
from app.schemas.menu_schemas import MenuItemUpdate
from app.db.database import get_db


@router.put("/{menu_id}")
async def update_menu_item(
    menu_id: int,
    category_id: int = Form(...),
    name: str = Form(...),
    price: float = Form(...),
    rating: float = Form(0),
    description: str = Form(None),
    values_text: str = Form(None),
    is_featured: bool = Form(False),
    is_top_rated: bool = Form(False),
    is_recommended: bool = Form(False),
    is_new: bool = Form(False),
    file: UploadFile = File(None),
    db=Depends(get_db)
):
    existing = get_menu_item_by_id_service(db, menu_id)

    if file:
        upload_result = upload_to_cloudinary(file)
        image_url = upload_result["url"]
    else:
        image_url = existing["image_url"]  # keep old image

    payload = MenuItemUpdate(
        category_id=category_id,
        name=name,
        image_url=image_url,
        price=price,
        rating=rating,
        description=description,
        values_text=values_text,
        is_featured=is_featured,
        is_top_rated=is_top_rated,
        is_recommended=is_recommended,
        is_new=is_new
    )

    update_menu_item_service(db, menu_id, payload)

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