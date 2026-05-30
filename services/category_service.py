from sqlalchemy.exc import IntegrityError, OperationalError,DataError
from fastapi import HTTPException, status, Depends
from data_models.pyd_models import CategoryModel
from db_models.models import Category
from db_models.db import get_db
from exceptions.DB_exception import db_exception 


class CategoryService:
    def __init__(self):
        self._session =None
        self.count = 1
    
    @db_exception   
    def getCategories(self,session):
        categories = session.query(Category).all()
        if len(categories) < self.count:
            raise HTTPException(status_code=404,detail = "The Category items list empty")
        data = [CategoryModel.model_validate(item).model_dump() for item in categories]
        return data  
    
    @db_exception
    def getCategoryById(self, **kwargs):
        session = kwargs["session"]
        id = kwargs["id"]
        category_item = session.get(Category, id)
        if category_item is None:
            raise HTTPException(status_code=404, detail= f"The category item with ID {id} not found")
        data_item = CategoryModel.model_validate(category_item).model_dump()
        return data_item
             
        
    @db_exception
    def addCategory(self, **kwargs):
        session = kwargs['session']
        new_category = kwargs['category']
        category_item = new_category.model_dump()
        db_category = Category(**category_item)
        session.add(db_category)
        session.commit()
        session.refresh(db_category)
        return category_item
        
    @db_exception
    def updateCategory(self,**kwargs):
        session = kwargs['session']
        id = kwargs['id']
        update_category = kwargs['category_model']
        category_item = session.get(Category, id)
        if category_item is None:
            raise HTTPException(status_code=404, detail=f"The category item with ID {id} not found")
        
        update_item=update_category.model_dump(exclude_unset=True)
        for key,val in update_item.items():
            setattr(category_item,key,val)
        session.add(category_item)
        session.commit()
        session.refresh(category_item)
        return update_item
        
    @db_exception
    def deleteCategory(self, **kwargs):
        session = kwargs['session']
        id = kwargs['id']
        db_category = session.get(Category, id)
        if db_category is None:
            raise HTTPException(status_code=404, detail= f"The category item with ID {id} not found")
        session.delete(db_category)
        session.commit()
        
        
    

Category_Service = CategoryService()
