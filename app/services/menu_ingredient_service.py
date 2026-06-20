from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


#  CREATE
def create_menu_ingredient_service(db, payload):
    try:
        data = payload if isinstance(payload, dict) else payload.model_dump()

        result = db.execute(
            text("""
                EXEC Reztro.AddMenuIngredient
                    @menu_id=:menu_id,
                    @ingredient_name=:ingredient_name
            """),
            data
        )

        return result.mappings().first()

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )


#  GET ALL
def get_menu_ingredients_service(db):
    try:
        result = db.execute(
            text("""
                EXEC Reztro.GetMenuIngredients
            """)
        )

        return result.mappings().all()

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


#  GET BY ID
def get_menu_ingredient_by_id_service(db, ingredient_id: int):
    try:
        result = db.execute(
            text("""
                EXEC Reztro.GetMenuIngredientById
                    @ingredient_id=:ingredient_id
            """),
            {
                "ingredient_id": ingredient_id
            }
        )

        item = result.mappings().first()

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ingredient not found"
            )

        return item

    except HTTPException:
        raise

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )


#  GET BY MENU ID
def get_menu_ingredients_by_menu_id_service(db, payload):
    try:
        result = db.execute(
            text("""
                EXEC Reztro.GetMenuIngredientsByMenuId
                    @menu_id=:menu_id
            """),
            payload.model_dump()
        )

        return result.mappings().all()

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )


#  UPDATE
def update_menu_ingredient_service(db, ingredient_id: int, payload):
    try:
        data = payload if isinstance(payload, dict) else payload.model_dump(exclude_unset=True)

        if not data:
            return None  # nothing to update

        data["ingredient_id"] = ingredient_id

        result = db.execute(
            text("""
                EXEC Reztro.UpdateMenuIngredient
                    @ingredient_id=:ingredient_id,
                    @ingredient_name=:ingredient_name
            """),
            data
        )

        db.commit()

        return result.mappings().first()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )

#  DELETE BY ID
def delete_menu_ingredient_service(db, ingredient_id: int):
    try:
        result = db.execute(
            text("""
                EXEC Reztro.DeleteMenuIngredient
                    @ingredient_id=:ingredient_id
            """),
            {
                "ingredient_id": ingredient_id
            }
        )

        return result.mappings().first()

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )


#  DELETE BY MENU ID
def delete_menu_ingredients_by_menu_id_service(db, payload):
    try:
        result = db.execute(
            text("""
                EXEC Reztro.DeleteMenuIngredientsByMenuId
                    @menu_id=:menu_id
            """),
            payload.model_dump()
        )

        return result.mappings().first()

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )