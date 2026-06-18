from fastapi import APIRouter, Depends

from app.db.database import get_db

from app.schemas.menu_item_meal_time_schemas import (
    MenuItemMealTimeCreate,
    MenuItemMealTimeDelete,
    GetMealTimesByMenuIdRequest,
    GetMenuItemsByMealTimeIdRequest,
    RemoveAllMealTimesFromMenuItemRequest,
    RemoveMealTimeFromAllMenuItemsRequest
)

from app.services.menu_item_meal_time_service import (
    add_menu_item_meal_time_service,
    get_menu_item_meal_times_service,
    get_meal_times_by_menu_id_service,
    get_menu_items_by_meal_time_id_service,
    remove_menu_item_meal_time_service,
    remove_all_meal_times_from_menu_item_service,
    remove_meal_time_from_all_menu_items_service
)


router = APIRouter(
    prefix="/menu-item-meal-times",
    tags=["Menu Item Meal Times"]
)


# 🔹 ADD
@router.post("")
def add_menu_item_meal_time(payload: MenuItemMealTimeCreate, db=Depends(get_db)):

    data = add_menu_item_meal_time_service(db, payload)

    return {
        "success": True,
        "message": "Meal time assigned to menu item successfully",
        "data": data
    }


# 🔹 GET ALL
@router.get("")
def get_menu_item_meal_times(db=Depends(get_db)):

    items = get_menu_item_meal_times_service(db)

    return {
        "success": True,
        "count": len(items),
        "data": items
    }


# 🔹 GET MEAL TIMES BY MENU ID
@router.post("/by-menu-id")
def get_meal_times_by_menu_id(payload: GetMealTimesByMenuIdRequest, db=Depends(get_db)):

    items = get_meal_times_by_menu_id_service(db, payload)

    return {
        "success": True,
        "count": len(items),
        "data": items
    }


# 🔹 GET MENU ITEMS BY MEAL TIME ID
@router.post("/by-meal-time-id")
def get_menu_items_by_meal_time_id(payload: GetMenuItemsByMealTimeIdRequest, db=Depends(get_db)):

    items = get_menu_items_by_meal_time_id_service(db, payload)

    return {
        "success": True,
        "count": len(items),
        "data": items
    }


# 🔹 REMOVE SINGLE
@router.delete("")
def remove_menu_item_meal_time(payload: MenuItemMealTimeDelete, db=Depends(get_db)):

    data = remove_menu_item_meal_time_service(db, payload)

    return {
        "success": True,
        "message": "Meal time removed from menu item successfully",
        "data": data
    }


# 🔹 REMOVE ALL FROM MENU
@router.delete("/all")
def remove_all_meal_times_from_menu_item(
    payload: RemoveAllMealTimesFromMenuItemRequest,
    db=Depends(get_db)
):

    data = remove_all_meal_times_from_menu_item_service(db, payload)

    return {
        "success": True,
        "message": "All meal times removed from menu item",
        "data": data
    }


# 🔹 REMOVE MEAL TIME FROM ALL MENUS
@router.delete("/remove-from-all")
def remove_meal_time_from_all_menu_items(
    payload: RemoveMealTimeFromAllMenuItemsRequest,
    db=Depends(get_db)
):

    data = remove_meal_time_from_all_menu_items_service(db, payload)

    return {
        "success": True,
        "message": "Meal time removed from all menu items",
        "data": data
    }