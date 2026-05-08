from pydantic import BaseModel,ConfigDict
from typing import Optional


class ProductModel(BaseModel):
    id:Optional[int] = None
    category_id:int
    name:str
    quantity:int
    price:float

    class Config:
        from_attributes=True

class ProductUpdate(BaseModel):
    category_id:Optional[int] =None
    name:Optional[str] = None
    quantity:Optional[int] = None
    price:Optional[float] = None

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
    firstname:str
    lastname:str
    email:str
    password:str
    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: int
    firstname: str
    lastname: str|None = None
    email: str

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    username:str
    password:str

class RefreshToken(BaseModel):
    refresh_token:str

class ProductInput(BaseModel):
    category_id:int
    name:str
    quantity:int
    price:float

    class Config:
        from_attributes=True

class CategoryInput(BaseModel):
    
    name:str

    class Config:
        from_attributes = True

class OrderInput(BaseModel):
   
    product_id:int
    user_id:int
    firstname:str
    lastname:str
    address:str

    class Config:
        from_attributes= True

class UserInput(BaseModel):
    
    name:str
    firstname:str
    lastname:str
    email:str

    class Config:
        from_attributes= True