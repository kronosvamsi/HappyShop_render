from  fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from db_models.db import get_db
from services import product_service


router= APIRouter(
    prefix="/random",
    tags=["random"],
    dependencies=[Depends(get_db)]
)

@router.get("/products")
def get_random(session:Session = Depends(get_db)):
    data = product_service.getProducts(session)
    return data
