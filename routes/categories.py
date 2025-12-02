from  fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError
from data_models.pyd_models import CategoryModel
from db_models.models import Category,get_db



router = APIRouter(
    prefix = "/categories",
    tags = ['categories'],
    dependencies = [Depends(get_db)]
)

@router.get("/")
def get_categories(session:Session = Depends(get_db)) :
    try:
        db_categories = session.query(Category).all()
        if len(db_categories) == 0:
            raise HTTPException(status_code= 404, detail= "Empty categories list")
    
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                detail="Data conflict (e.g., duplicate unique key or missing foreign key).")
    except OperationalError:
        # Catches connection issues, server offline, etc.
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
    
    data_items = [CategoryModel.model_validate(item).model_dump() for item in db_categories]
    return JSONResponse(content={"message":"Items fetched from database","items":data_items},status_code=200)
    
@router.get("/category/{category_id}")
def get_category_by_id(category_id:int, session:Session = Depends(get_db)):
    try:
        category_item = session.get(Category, category_id)
        if category_item is None:
            raise HTTPException(status_code=404, detail= f"The category item with ID {category_id} not found")
    
    except IntegrityError:
        session.rollback()
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Data conflict (e.g., duplicate unique key or missing foreign key).")
    except OperationalError:
        # Catches connection issues, server offline, etc.
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
    
    data_item = CategoryModel.model_validate(category_item).model_dump()
    return JSONResponse(content={"message":"Item found","item":data_item},status_code=200)

@router.post("/addCategory")
def add_category(new_category:CategoryModel, session:Session =  Depends(get_db)):
    try:
        category_item = new_category.model_dump()
        db_category = Category(**category_item)
        session.add(db_category)
        session.commit()
        session.refresh(db_category)
    
    except IntegrityError:
        session.rollback()
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Data conflict (e.g., duplicate unique key or missing foreign key).")
    except OperationalError:
        # Catches connection issues, server offline, etc.
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )

    return JSONResponse(content="Item added",status_code=200)


@router.put("/updateCategory/{category_id}")
def update_category(category_id:int, update_category:CategoryModel, session:Session = Depends(get_db)):
    try:
        category_item = session.get(Category, category_id)
        if category_item is None:
            raise HTTPException(status_code=404, content=f"The category item with ID {category_id} not found")
        update_item=update_category.model_dump(exclude_unset=True)
        for key,val in update_item.items():
            setattr(category_item,key,val)
        
        session.add(category_item)
        session.commit()
        session.refresh(category_item)
        
    except IntegrityError:
        session.rollback()
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Data conflict (e.g., duplicate unique key or missing foreign key).")
    except OperationalError:
        # Catches connection issues, server offline, etc.
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
    return JSONResponse(content=f"Category item with ID {category_id} updated",status_code=200)

@router.delete("/deleteCategory/{category_id}")
def delete_category(category_id:int, session:Session = Depends(get_db)):
    try:
        db_category = session.get(Category, category_id)
        if db_category is None:
            raise HTTPException(status_code=404, detail= f"The category item with ID {category_id} not found")
        
        session.delete(db_category)
        session.commit()
    
    except IntegrityError:
        session.rollback()
        raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Data conflict (e.g., duplicate unique key or missing foreign key).")
    except OperationalError:
        # Catches connection issues, server offline, etc.
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
    
    return JSONResponse(content=f"Item with ID {category_id} deleted",status_code=200)
    
