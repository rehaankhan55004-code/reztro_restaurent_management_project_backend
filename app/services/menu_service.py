from fastapi import HTTPException, status

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.services.menu_nutrition_service import (
    add_menu_nutrition_service,
    update_menu_nutrition_by_menu_id_service,
    delete_menu_nutrition_by_menu_id_service
)

from app.services.menu_ingredient_service import (
    create_menu_ingredient_service,
    delete_menu_ingredients_by_menu_id_service
)

from app.services.menu_item_tag_service import (
    add_menu_item_tag_service,
    remove_all_tags_from_menu_item_service
)

from app.services.menu_item_promotion_service import (
    add_menu_item_promotion_service,
    remove_all_promotions_from_menu_item_service
)

from app.services.menu_item_meal_time_service import (
    add_menu_item_meal_time_service,
    remove_all_meal_times_from_menu_item_service
)



def create_menu_item_service(db, payload):
    try:
        result = db.execute(
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
            payload.model_dump(exclude={
                "nutrition",
                "ingredients",
                "tag_ids",
                "meal_time_ids",
                "promotion_ids"
            })
        )

        menu = result.mappings().first()

        if not menu:
            raise HTTPException(
                status_code=500,
                detail="Menu item created but menu_id not returned"
            )

        menu_id = menu["menu_id"]

        if payload.nutrition:
            add_menu_nutrition_service(db, {
                "menu_id": menu_id,
                "calories": payload.nutrition.calories,
                "proteins": payload.nutrition.proteins,
                "fats": payload.nutrition.fats,
                "carbs": payload.nutrition.carbs
            })

        if payload.ingredients:
            for ingredient in payload.ingredients:
                create_menu_ingredient_service(db, {
                    "menu_id": menu_id,
                    "ingredient_name": ingredient
                })

        if payload.tag_ids:
            for tag_id in payload.tag_ids:
                add_menu_item_tag_service(db, {
                    "menu_id": menu_id,
                    "tag_id": tag_id
                })

        if payload.meal_time_ids:
            for meal_time_id in payload.meal_time_ids:
                add_menu_item_meal_time_service(db, {
                    "menu_id": menu_id,
                    "meal_time_id": meal_time_id
                })

        if payload.promotion_ids:
            for promotion_id in payload.promotion_ids:
                add_menu_item_promotion_service(db, {
                    "menu_id": menu_id,
                    "promotion_id": promotion_id
                })

        db.commit()

        return menu

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

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


def update_menu_item_service(db, menu_id: int, payload):
    try:
        params = payload.model_dump(exclude={
            "nutrition",
            "ingredients",
            "tag_ids",
            "meal_time_ids",
            "promotion_ids"
        })
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

        if payload.nutrition:
            update_menu_nutrition_by_menu_id_service(
                db,
                menu_id,
                {
                    "calories": payload.nutrition.calories,
                    "proteins": payload.nutrition.proteins,
                    "fats": payload.nutrition.fats,
                    "carbs": payload.nutrition.carbs
                }
            )

        if payload.ingredients is not None:
            delete_menu_ingredients_by_menu_id_service(db, {"menu_id": menu_id})

            for ingredient in payload.ingredients:
                create_menu_ingredient_service(db, {
                    "menu_id": menu_id,
                    "ingredient_name": ingredient
                })
                
        if payload.tag_ids is not None:
            remove_all_tags_from_menu_item_service(db, {"menu_id": menu_id})

            for tag_id in payload.tag_ids:
                add_menu_item_tag_service(db, {
                    "menu_id": menu_id,
                    "tag_id": tag_id
                })

        if payload.meal_time_ids is not None:
            remove_all_meal_times_from_menu_item_service(db, {"menu_id": menu_id})

            for meal_time_id in payload.meal_time_ids:
                add_menu_item_meal_time_service(db, {
                    "menu_id": menu_id,
                    "meal_time_id": meal_time_id
                })

        if payload.promotion_ids is not None:
            remove_all_promotions_from_menu_item_service(db, menu_id)

            for promotion_id in payload.promotion_ids:
                add_menu_item_promotion_service(db, {
                    "menu_id": menu_id,
                    "promotion_id": promotion_id
                })

        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def delete_menu_item_service(db, menu_id: int):
    try:

        delete_menu_ingredients_by_menu_id_service(
            db,
            {"menu_id": menu_id}
        )

        delete_menu_nutrition_by_menu_id_service(
            db,
            {"menu_id": menu_id}
        )

        remove_all_tags_from_menu_item_service(
            db,
            {"menu_id": menu_id}
        )

        remove_all_promotions_from_menu_item_service(
            db,
            menu_id
        )

        remove_all_meal_times_from_menu_item_service(
            db,
            {"menu_id": menu_id}
        )

        db.execute(
            text("""
                EXEC Reztro.DeleteMenuItem
                    @menu_id=:menu_id
            """),
            {"menu_id": menu_id}
        )

        db.commit()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

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