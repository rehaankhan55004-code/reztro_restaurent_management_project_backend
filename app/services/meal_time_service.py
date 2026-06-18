from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


# 🔹 CREATE
def create_meal_time_service(db, payload):
    try:
        result = db.execute(
            text("""
                EXEC Reztro.AddMealTime
                    @meal_time_name=:meal_time_name
            """),
            payload.model_dump()
        )

        db.commit()

        return result.mappings().first()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )


# 🔹 GET ALL
def get_meal_times_service(db):
    try:
        result = db.execute(
            text("""
                EXEC Reztro.GetMealTimes
            """)
        )

        return result.mappings().all()

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e.orig)
        )


# 🔹 GET BY ID
def get_meal_time_by_id_service(db, meal_time_id: int):
    try:
        result = db.execute(
            text("""
                EXEC Reztro.GetMealTimeById
                    @meal_time_id=:meal_time_id
            """),
            {
                "meal_time_id": meal_time_id
            }
        )

        item = result.mappings().first()

        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meal time not found"
            )

        return item

    except HTTPException:
        raise

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )


# 🔹 UPDATE
def update_meal_time_service(db, meal_time_id: int, payload):
    try:
        params = payload.model_dump()
        params["meal_time_id"] = meal_time_id

        result = db.execute(
            text("""
                EXEC Reztro.UpdateMealTime
                    @meal_time_id=:meal_time_id,
                    @meal_time_name=:meal_time_name
            """),
            params
        )

        db.commit()

        return result.mappings().first()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )


# 🔹 DELETE (soft delete)
def delete_meal_time_service(db, meal_time_id: int):
    try:
        result = db.execute(
            text("""
                EXEC Reztro.DeleteMealTime
                    @meal_time_id=:meal_time_id
            """),
            {
                "meal_time_id": meal_time_id
            }
        )

        db.commit()

        return result.mappings().first()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )


# 🔹 RESTORE
def restore_meal_time_service(db, meal_time_id: int):
    try:
        result = db.execute(
            text("""
                EXEC Reztro.RestoreMealTime
                    @meal_time_id=:meal_time_id
            """),
            {
                "meal_time_id": meal_time_id
            }
        )

        db.commit()

        return result.mappings().first()

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e.orig)
        )