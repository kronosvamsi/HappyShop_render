from sqlalchemy.exc import IntegrityError, OperationalError,DataError
from fastapi import HTTPException, status, Depends
from data_models.pyd_models import CategoryModel
from db_models.models import Category
from db_models.db import get_db


class CategoryService:
    def __init__(self):
        self._session =None
        self.count = 1
        
    def getCategories(self,session):
        try:
            # print("From category service")
            self._session = session
            categories = self._session.query(Category).all()
            if len(categories) < self.count:
                raise HTTPException(status_code=404,detail = "The Category items list empty")
            data = [CategoryModel.model_validate(item).model_dump() for item in categories]
            return data
        
        except IntegrityError:
            self._session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Data conflict (e.g., duplicate unique key or missing foreign key).")
        
        except OperationalError:
        # Catches connection issues, server offline, etc.
         self._session.rollback()
         raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
        finally:
            self._session = None  
    
    def getCategoryById(self, **kwargs):
        session = kwargs["session"]
        id = kwargs["id"]
        self._session = session
        try:
             category_item = self._session.get(Category, id)
             if category_item is None:
                 raise HTTPException(status_code=404, detail= f"The category item with ID {id} not found")
             
             data_item = CategoryModel.model_validate(category_item).model_dump()
             return data_item
             
        except IntegrityError:
            self._session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Data conflict (e.g., duplicate unique key or missing foreign key).")
        
        except  OperationalError:
            self._session.rollback()
            raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
        finally:
            self._session = None
    
    def addCategory(self, **kwargs):
        session = kwargs['session']
        new_category = kwargs['category']
        self._session = session
        try :
            category_item = new_category.model_dump()
            db_category = Category(**category_item)
            self._session.add(db_category)
            self._session.commit()
            self._session.refresh(db_category)
            return category_item
        
        except IntegrityError:
              self._session.rollback()
              raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Data conflict (e.g., duplicate unique key or missing foreign key).")
            
        except OperationalError:
            self._session.rollback()
            raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
            
        finally:
            self._session = None
        
    
    def updateCategory(self,**kwargs):
        session = kwargs['session']
        id = kwargs['id']
        update_category = kwargs['category_model']
        self._session = session
        try:
            category_item = self._session.get(Category, id)
            if category_item is None:
                raise HTTPException(status_code=404, content=f"The category item with ID {id} not found")
            
            update_item=update_category.model_dump(exclude_unset=True)
            for key,val in update_item.items():
                setattr(category_item,key,val)
            
            self._session.add(category_item)
            self._session.commit()
            self._session.refresh(category_item)
            return update_item
        
        except IntegrityError:
            self._session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Data conflict (e.g., duplicate unique key or missing foreign key).")

            
        except OperationalError:
            self._session.rollback()
            raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
            
        finally:
            self._session = None
 
    
    def deleteCategory(self, **kwargs):
        session = kwargs['session']
        id = kwargs['id']
        self._session = session
        try:
            db_category = self._session.get(Category, id)
            if db_category is None:
                raise HTTPException(status_code=404, detail= f"The category item with ID {id} not found")
            
            self._session.delete(db_category)
            self._session.commit()
        
        except IntegrityError:
            self._session.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Data conflict (e.g., duplicate unique key or missing foreign key).")

            
        except OperationalError:
            self._session.rollback()
            raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
        finally:
            self._session = None
    

Category_Service = CategoryService()
