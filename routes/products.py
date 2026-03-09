from  fastapi import APIRouter,Depends,HTTPException,status
from db_models.models import get_db,Product
from data_models.pyd_models import ProductModel,ProductInput
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError
from services import product_service
router= APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(get_db)]
)

@router.get("/")
def get_products(session:Session = Depends(get_db)):
    data = product_service.getProducts(session)
    return JSONResponse(content={"data":data},status_code=200)
    

@router.get('/{product_id}')
def get_product(product_id:int, session:Session = Depends(get_db)):
    data = product_service.getProduct(session,product_id)
    return JSONResponse(content= {"data":data},status_code=200)

@router.post('/')
def add_product(new_product:ProductInput, session:Session = Depends(get_db)):
    data = product_service.addProduct(session,new_product)
    return JSONResponse(content={"msg":"Item added", "data":data},status_code=200)


@router.put("/{product_id}")
def update_product(product_id:int,product_up:ProductModel, session:Session = Depends(get_db)):
    data = product_service.updateProduct(session,product_up,product_id=product_id)
    return JSONResponse(content={"message":"item updated","data":data},status_code=200)

@router.delete('/{product_id}')
def delete_product(product_id:int, session:Session = Depends(get_db)):
    
    item_id = product_service.deleteProduct(session,product_id)
    return JSONResponse(content=f"Item with ID{item_id} deleted",status_code=200)
    
