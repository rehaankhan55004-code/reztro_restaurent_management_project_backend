from pydantic import (
    BaseModel,
    Field,
)


class MenuItemTagCreate(BaseModel):

    menu_id: int = Field(
        ...,
        gt=0
    )

    tag_id: int = Field(
        ...,
        gt=0
    )


class MenuItemTagDelete(BaseModel):

    menu_id: int = Field(
        ...,
        gt=0
    )

    tag_id: int = Field(
        ...,
        gt=0
    )


class GetTagsByMenuIdRequest(BaseModel):

    menu_id: int = Field(
        ...,
        gt=0
    )


class GetMenuItemsByTagIdRequest(BaseModel):

    tag_id: int = Field(
        ...,
        gt=0
    )


class RemoveAllTagsFromMenuItemRequest(BaseModel):

    menu_id: int = Field(
        ...,
        gt=0
    )