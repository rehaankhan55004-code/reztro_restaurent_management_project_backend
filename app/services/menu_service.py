from fastapi import HTTPException, status

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


def create_menu_item_service(
    db,
    payload
):

    try:

        db.execute(
            text("""
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
            """),
            payload.model_dump()
        )

        db.commit()

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


def get_menu_items_service(
    db
):

    try:

        result = db.execute(
            text("""
                EXEC Reztro.GetMenuItems
            """)
        )

        return result.mappings().all()

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


def get_menu_item_by_id_service(
    db,
    menu_id: int
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

        return item

    except HTTPException:
        raise

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


def update_menu_item_service(
    db,
    menu_id: int,
    payload
):

    try:

        params = payload.model_dump()

        params["menu_id"] = menu_id

        db.execute(
            text("""
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
            """),
            params
        )

        db.commit()

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


def delete_menu_item_service(
    db,
    menu_id: int
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

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


def update_menu_availability_service(
    db,
    menu_id: int,
    payload
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

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


def update_menu_stats_service(
    db,
    menu_id: int,
    payload
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

    except SQLAlchemyError as e:

        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


def get_featured_menu_items_service(
    db
):

    try:

        result = db.execute(
            text("""
                EXEC Reztro.GetFeaturedMenuItems
            """)
        )

        return result.mappings().all()

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


def get_top_rated_menu_items_service(
    db
):

    try:

        result = db.execute(
            text("""
                EXEC Reztro.GetTopRatedMenuItems
            """)
        )

        return result.mappings().all()

    except SQLAlchemyError as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )