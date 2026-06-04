from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import get_db

from app.schemas.menu_schemas import (
    MenuItemCreate,
    MenuItemUpdate,
    MenuAvailabilityUpdate,
    MenuStatsUpdate
)

router = APIRouter()


# CREATE MENU ITEM

@router.post("/menu-items")
def create_menu_item(
    payload: MenuItemCreate,
    db=Depends(get_db)
):

    try:

        query = text("""
            EXEC Reztro.AddMenuItem
                @category_id=:category_id,
                @name=:name,
                @image_url=:image_url,
                @price=:price,
                @rating=:rating,
                @description=:description,
                @values_text=:values_text,
                @is_featured=:is_featured,
                @is_top_rated=:is_top_rated,
                @is_recommended=:is_recommended,
                @is_new=:is_new
        """)

        db.execute(query, payload.model_dump())

        db.commit()

        return {
            "success": True,
            "message": "Menu item created successfully"
        }

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# GET ALL MENU ITEMS

@router.get("/menu-items")
def get_menu_items(
    db=Depends(get_db)
):

    try:

        result = db.execute(
            text("EXEC Reztro.GetMenuItems")
        )

        items = result.mappings().all()

        return {
            "success": True,
            "count": len(items),
            "data": items
        }

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# GET MENU ITEM BY ID

@router.get("/menu-items/{menu_id}")
def get_menu_item_by_id(
    menu_id: int,
    db=Depends(get_db)
):

    try:

        result = db.execute(
            text("""
                EXEC Reztro.GetMenuItemById
                    @menu_id=:menu_id
            """),
            {
                "menu_id": menu_id
            }
        )

        item = result.mappings().first()

        if not item:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu item not found"
            )

        return {
            "success": True,
            "data": item
        }

    except HTTPException as e:
        raise e

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# UPDATE MENU ITEM

@router.put("/menu-items/{menu_id}")
def update_menu_item(
    menu_id: int,
    payload: MenuItemUpdate,
    db=Depends(get_db)
):

    try:

        params = payload.model_dump()

        params["menu_id"] = menu_id

        query = text("""
            EXEC Reztro.UpdateMenuItem
                @menu_id=:menu_id,
                @category_id=:category_id,
                @name=:name,
                @image_url=:image_url,
                @price=:price,
                @rating=:rating,
                @description=:description,
                @values_text=:values_text,
                @is_featured=:is_featured,
                @is_top_rated=:is_top_rated,
                @is_recommended=:is_recommended,
                @is_new=:is_new
        """)

        db.execute(query, params)

        db.commit()

        return {
            "success": True,
            "message": "Menu item updated successfully"
        }

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# DELETE MENU ITEM

@router.delete("/menu-items/{menu_id}")
def delete_menu_item(
    menu_id: int,
    db=Depends(get_db)
):

    try:

        db.execute(
            text("""
                EXEC Reztro.DeleteMenuItem
                    @menu_id=:menu_id
            """),
            {
                "menu_id": menu_id
            }
        )

        db.commit()

        return {
            "success": True,
            "message": "Menu item deleted successfully"
        }

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# UPDATE AVAILABILITY

@router.patch("/menu-items/{menu_id}/availability")
def update_menu_availability(
    menu_id: int,
    payload: MenuAvailabilityUpdate,
    db=Depends(get_db)
):

    try:

        db.execute(
            text("""
                EXEC Reztro.UpdateMenuAvailability
                    @menu_id=:menu_id,
                    @is_available=:is_available
            """),
            {
                "menu_id": menu_id,
                "is_available": payload.is_available
            }
        )

        db.commit()

        return {
            "success": True,
            "message": "Availability updated successfully"
        }

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# UPDATE STATS

@router.patch("/menu-items/{menu_id}/stats")
def update_menu_stats(
    menu_id: int,
    payload: MenuStatsUpdate,
    db=Depends(get_db)
):

    try:

        params = payload.model_dump()

        params["menu_id"] = menu_id

        db.execute(
            text("""
                EXEC Reztro.UpdateMenuStats
                    @menu_id=:menu_id,
                    @rating=:rating,
                    @total_reviews=:total_reviews,
                    @total_orders=:total_orders,
                    @favorites_count=:favorites_count
            """),
            params
        )

        db.commit()

        return {
            "success": True,
            "message": "Stats updated successfully"
        }

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# FEATURED MENU ITEMS

@router.get("/menu-items/featured")
def get_featured_menu_items(
    db=Depends(get_db)
):

    try:

        result = db.execute(
            text("EXEC Reztro.GetFeaturedMenuItems")
        )

        items = result.mappings().all()

        return {
            "success": True,
            "count": len(items),
            "data": items
        }

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# TOP RATED MENU ITEMS

@router.get("/menu-items/top-rated")
def get_top_rated_menu_items(
    db=Depends(get_db)
):

    try:

        result = db.execute(
            text("EXEC Reztro.GetTopRatedMenuItems")
        )

        items = result.mappings().all()

        return {
            "success": True,
            "count": len(items),
            "data": items
        }

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

