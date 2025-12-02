from pydantic import BaseModel
from typing import Optional


class ProductModel(BaseModel):
    id:Optional[int] = None
    category_id:int
    name:str
    quantity:int
    price:float

    class Config:
        from_attributes=True

class CategoryModel(BaseModel):
    id:Optional[int] =None
    name:str

    class Config:
        from_attributes = True

class OrderModel(BaseModel):
    id:Optional[int] = None
    product_id:int
    user_id:int
    firstname:str
    lastname:str
    address:str

    class Config:
        from_attributes= True

class UserModel(BaseModel):
    id:Optional[int] = None
    name:str
    firstname:str
    lastname:str
    email:str

    class Config:
        from_attributes= True

