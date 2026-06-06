from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import get_db

from app.schemas.menu_category_schemas import (
    MenuCategoryCreate,
    MenuCategoryUpdate
)

router = APIRouter()


# CREATE CATEGORY

@router.post("/menu-categories")
def create_menu_category(
    payload: MenuCategoryCreate,
    db=Depends(get_db)
):

    try:

        query = text("""
            EXEC Reztro.AddMenuCategory
                @category_name=:category_name
        """)

        db.execute(
            query,
            payload.model_dump()
        )

        db.commit()

        return {
            "success": True,
            "message": "Menu category created successfully"
        }

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# GET ALL CATEGORIES

@router.get("/menu-categories")
def get_menu_categories(
    db=Depends(get_db)
):

    try:

        result = db.execute(
            text("EXEC Reztro.GetMenuCategories")
        )

        categories = result.mappings().all()

        return {
            "success": True,
            "count": len(categories),
            "data": categories
        }

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# GET CATEGORY BY ID

@router.get("/menu-categories/{category_id}")
def get_menu_category_by_id(
    category_id: int,
    db=Depends(get_db)
):

    try:

        result = db.execute(
            text("""
                EXEC Reztro.GetMenuCategoryById
                    @category_id=:category_id
            """),
            {
                "category_id": category_id
            }
        )

        category = result.mappings().first()

        if not category:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Menu category not found"
            )

        return {
            "success": True,
            "data": category
        }

    except HTTPException as e:
        raise e

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# UPDATE CATEGORY

@router.put("/menu-categories/{category_id}")
def update_menu_category(
    category_id: int,
    payload: MenuCategoryUpdate,
    db=Depends(get_db)
):

    try:

        query = text("""
            EXEC Reztro.UpdateMenuCategory
                @category_id=:category_id,
                @category_name=:category_name
        """)

        db.execute(
            query,
            {
                "category_id": category_id,
                "category_name": payload.category_name
            }
        )

        db.commit()

        return {
            "success": True,
            "message": "Menu category updated successfully"
        }

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# DELETE CATEGORY

@router.delete("/menu-categories/{category_id}")
def delete_menu_category(
    category_id: int,
    db=Depends(get_db)
):

    try:

        db.execute(
            text("""
                EXEC Reztro.DeleteMenuCategory
                    @category_id=:category_id
            """),
            {
                "category_id": category_id
            }
        )

        db.commit()

        return {
            "success": True,
            "message": "Menu category deleted successfully"
        }

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# RESTORE CATEGORY

@router.patch("/menu-categories/{category_id}/restore")
def restore_menu_category(
    category_id: int,
    db=Depends(get_db)
):

    try:

        db.execute(
            text("""
                EXEC Reztro.RestoreMenuCategory
                    @category_id=:category_id
            """),
            {
                "category_id": category_id
            }
        )

        db.commit()

        return {
            "success": True,
            "message": "Menu category restored successfully"
        }

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )