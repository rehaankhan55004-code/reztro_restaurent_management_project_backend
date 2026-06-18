from pydantic import BaseModel, Field


class MenuItemMealTimeCreate(BaseModel):

    menu_id: int = Field(..., gt=0)

    meal_time_id: int = Field(..., gt=0)


class MenuItemMealTimeDelete(BaseModel):

    menu_id: int = Field(..., gt=0)

    meal_time_id: int = Field(..., gt=0)


class GetMealTimesByMenuIdRequest(BaseModel):

    menu_id: int = Field(..., gt=0)


class GetMenuItemsByMealTimeIdRequest(BaseModel):

    meal_time_id: int = Field(..., gt=0)


class RemoveAllMealTimesFromMenuItemRequest(BaseModel):

    menu_id: int = Field(..., gt=0)


class RemoveMealTimeFromAllMenuItemsRequest(BaseModel):

    meal_time_id: int = Field(..., gt=0)