from  fastapi import APIRouter,Depends,HTTPException,status
from db_models.models import Product
from db_models.db import get_db
from data_models.pyd_models import ProductModel,ProductInput,ProductUpdate
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError
from services import product_service
from core.security import get_current_user
from db_models.models import User

router= APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(get_db)]
)

@router.get("/")
def get_products(session:Session = Depends(get_db)):
    data = product_service.getProducts(session)
    return JSONResponse(content=data,status_code=200)
    

@router.get('/{product_id}')
def get_product(product_id:int, session:Session = Depends(get_db)):
    data = product_service.getProduct(session,product_id)
    return JSONResponse(content= {"data":data},status_code=200)

@router.post('/')
def add_product(new_product:ProductInput, session:Session = Depends(get_db),user:User =  Depends(get_current_user)):
    if user is not None:
        data = product_service.addProduct(session,new_product)
        return JSONResponse(content={"msg":"Item added", "data":data},status_code=200)


@router.put("/{product_id}")
def update_product(product_id:int,product_up:ProductUpdate, session:Session = Depends(get_db), user:User =  Depends(get_current_user)):
    if user is not None:
        data = product_service.updateProduct(session,product_up,product_id=product_id)
        return JSONResponse(content={"message":"item updated","data":data},status_code=200)

@router.delete('/{product_id}')
def delete_product(product_id:int, session:Session = Depends(get_db), user:User =  Depends(get_current_user)):
    if user is not None:
        item_id = product_service.deleteProduct(session,product_id)
        return JSONResponse(content=f"Item with ID{item_id} deleted",status_code=200)
    

@router.delete("/clear-all", status_code=status.HTTP_200_OK)
def clear_all_products(db: Session = Depends(get_db)):
    """
    Deletes all products from the database to reset the catalog.
    """
    try:
        # Counts items before dropping them for a clean confirmation message
        num_deleted = db.query(Product).delete(synchronize_session=False)
        db.commit()
        
        return {
            "status": "success", 
            "message": f"Successfully cleared catalog. Deleted {num_deleted} products."
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error during deletion: {str(e)}"
        )
