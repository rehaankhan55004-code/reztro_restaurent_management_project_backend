from pydantic import BaseModel

# CREATE CATEGORY

class MenuCategoryCreate(BaseModel):

    category_name: str


# UPDATE CATEGORY

class MenuCategoryUpdate(BaseModel):

    category_name: str