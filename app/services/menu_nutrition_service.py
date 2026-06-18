def add_menu_nutrition_service(db, payload):
    cursor = db.cursor()
    cursor.execute(
        "EXEC Reztro.AddMenuNutrition ?, ?, ?, ?, ?",
        (
            payload.menu_id,
            payload.calories,
            payload.proteins,
            payload.fats,
            payload.carbs
        )
    )
    result = cursor.fetchone()
    db.commit()
    return result


def get_menu_nutrition_service(db):
    cursor = db.cursor()
    cursor.execute("EXEC Reztro.GetMenuNutrition")
    return cursor.fetchall()


def get_menu_nutrition_by_id_service(db, nutrition_id):
    cursor = db.cursor()
    cursor.execute(
        "EXEC Reztro.GetMenuNutritionById ?",
        (nutrition_id,)
    )
    return cursor.fetchone()


def get_menu_nutrition_by_menu_id_service(db, menu_id):
    cursor = db.cursor()
    cursor.execute(
        "EXEC Reztro.GetMenuNutritionByMenuId ?",
        (menu_id,)
    )
    return cursor.fetchone()


def update_menu_nutrition_service(db, nutrition_id, payload):
    cursor = db.cursor()
    cursor.execute(
        "EXEC Reztro.UpdateMenuNutrition ?, ?, ?, ?, ?",
        (
            nutrition_id,
            payload.calories,
            payload.proteins,
            payload.fats,
            payload.carbs
        )
    )
    result = cursor.fetchone()
    db.commit()
    return result


def update_menu_nutrition_by_menu_id_service(db, menu_id, payload):
    cursor = db.cursor()
    cursor.execute(
        "EXEC Reztro.UpdateMenuNutritionByMenuId ?, ?, ?, ?, ?",
        (
            menu_id,
            payload.calories,
            payload.proteins,
            payload.fats,
            payload.carbs
        )
    )
    result = cursor.fetchone()
    db.commit()
    return result


def delete_menu_nutrition_service(db, nutrition_id):
    cursor = db.cursor()
    cursor.execute(
        "EXEC Reztro.DeleteMenuNutrition ?",
        (nutrition_id,)
    )
    result = cursor.fetchone()
    db.commit()
    return result


def delete_menu_nutrition_by_menu_id_service(db, menu_id):
    cursor = db.cursor()
    cursor.execute(
        "EXEC Reztro.DeleteMenuNutritionByMenuId ?",
        (menu_id,)
    )
    result = cursor.fetchone()
    db.commit()
    return result