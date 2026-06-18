from fastapi import APIRouter, Depends

from app.db.database import get_db

from app.schemas.menu_item_tag_schemas import (
    MenuItemTagCreate,
    MenuItemTagDelete,
    GetTagsByMenuIdRequest,
    GetMenuItemsByTagIdRequest,
    RemoveAllTagsFromMenuItemRequest
)

from app.services.menu_item_tag_service import (
    add_menu_item_tag_service,
    get_menu_item_tags_service,
    get_tags_by_menu_id_service,
    get_menu_items_by_tag_id_service,
    remove_menu_item_tag_service,
    remove_all_tags_from_menu_item_service
)


router = APIRouter(
    prefix="/menu-item-tags",
    tags=["Menu Item Tags"]
)


# 🔹 ADD TAG TO MENU ITEM

@router.post("")
def add_menu_item_tag(
    payload: MenuItemTagCreate,
    db=Depends(get_db)
):

    data = add_menu_item_tag_service(
        db,
        payload
    )

    return {
        "success": True,
        "message": "Tag assigned to menu item successfully",
        "data": data
    }


# 🔹 GET ALL MENU ITEM TAGS

@router.get("")
def get_menu_item_tags(
    db=Depends(get_db)
):

    items = get_menu_item_tags_service(db)

    return {
        "success": True,
        "count": len(items),
        "data": items
    }


# 🔹 GET TAGS BY MENU ID

@router.post("/by-menu-id")
def get_tags_by_menu_id(
    payload: GetTagsByMenuIdRequest,
    db=Depends(get_db)
):

    items = get_tags_by_menu_id_service(
        db,
        payload
    )

    return {
        "success": True,
        "count": len(items),
        "data": items
    }


# 🔹 GET MENU ITEMS BY TAG ID

@router.post("/by-tag-id")
def get_menu_items_by_tag_id(
    payload: GetMenuItemsByTagIdRequest,
    db=Depends(get_db)
):

    items = get_menu_items_by_tag_id_service(
        db,
        payload
    )

    return {
        "success": True,
        "count": len(items),
        "data": items
    }


# 🔹 REMOVE SINGLE TAG FROM MENU ITEM

@router.delete("")
def remove_menu_item_tag(
    payload: MenuItemTagDelete,
    db=Depends(get_db)
):

    data = remove_menu_item_tag_service(
        db,
        payload
    )

    return {
        "success": True,
        "message": "Tag removed from menu item successfully",
        "data": data
    }


# 🔹 REMOVE ALL TAGS FROM MENU ITEM

@router.delete("/all")
def remove_all_tags_from_menu_item(
    payload: RemoveAllTagsFromMenuItemRequest,
    db=Depends(get_db)
):

    data = remove_all_tags_from_menu_item_service(
        db,
        payload
    )

    return {
        "success": True,
        "message": "All tags removed from menu item successfully",
        "data": data
    }