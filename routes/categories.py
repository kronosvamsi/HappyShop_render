from  fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError,DataError
from data_models.pyd_models import CategoryModel
from db_models.models import Category
from db_models.db import get_db
import logging
from services.category_service import Category_Service


router = APIRouter(
    prefix = "/categories",
    tags = ['categories'],
    dependencies = [Depends(get_db)]
)

@router.get("/")
def get_categories(session:Session = Depends(get_db)):
    data_items = Category_Service.getCategories(session)
    return JSONResponse(content={"message":"Items fetched from database","items":data_items},status_code=200)
    
@router.get("/{category_id}")
def get_category(category_id:int, session:Session = Depends(get_db)):
    data_item = Category_Service.getCategoryById(session= session,id=category_id)
    return JSONResponse(content={"message":"Item found","item":data_item},status_code=200)

# logger = logging.getLogger(__name__)
@router.post("/")
def add_category(new_category:CategoryModel, session:Session =  Depends(get_db)):
    category_item = Category_Service.addCategory(category = new_category, session = session)
    return JSONResponse(content=f"Item added:{category_item}",status_code=200)


@router.put("/{category_id}")
def update_category(category_id:int, update_category:CategoryModel, session:Session = Depends(get_db)):
    category_item = Category_Service.updateCategory(session = session, id = category_id, category_model = update_category)
    return JSONResponse(content=f"Category item updated:{category_item}",status_code=200)

@router.delete("/{category_id}")
def delete_category(category_id:int, session:Session = Depends(get_db)):
    Category_Service.deleteCategory(session = session, id = category_id)
    return JSONResponse(content=f"Item with ID {category_id} deleted",status_code=200)
    
