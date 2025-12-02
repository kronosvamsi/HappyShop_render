from  fastapi import APIRouter,Depends,HTTPException,status
from db_models.models import get_db,Product
from data_models.pyd_models import ProductModel
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError
    
router= APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(get_db)]
)

@router.get("/")
def get_products(session:Session = Depends(get_db)):
    try:
        db_products=session.query(Product).all()
    
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
    serialize_data=[ProductModel.model_validate(product).model_dump() for product in db_products]
    return JSONResponse(content={"message":"Items fetched from DB","data":serialize_data},status_code=200)
    

@router.get('/{product_id}')
def get_product_by_id(product_id:int, session:Session = Depends(get_db)):
    try:
        db_product=session.query(Product).filter(Product.id == product_id).first()
        if db_product is None:
            raise HTTPException(status_code=404, detail=f"Product by id {product_id} is not found ")
    
    except OperationalError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
    
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                detail="Data conflict (e.g., duplicate unique key or missing foreign key).")
    
    return JSONResponse(content= f"Product with ID {product_id} found",status_code=200)

@router.post('/addProduct')
def add_product(new_product:ProductModel, session:Session = Depends(get_db)):
    try:
        product_item=new_product.model_dump()
        db_product=Product(**product_item)
        session.add(db_product)
        session.commit()
        session.refresh(db_product)
    
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                detail="Data conflict (e.g., duplicate unique key or missing foreign key).")
    
    except OperationalError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
    
    except Exception as e:
        session.rollback()
        print(f"LOG: Unhandled exception: {e}") # Log the specific error for debugging
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="An unexpected internal error occurred.")
    
    return JSONResponse(content="Item added",status_code=200)


@router.put("/updateProduct/{product_id}")
def update_product_by_id(product_id:int,product_up:ProductModel, session:Session = Depends(get_db)):
    try:
        db_prod = session.get(Product,product_id)
        if db_prod is None:
            raise HTTPException(status_code=404, detail=f"The product with ID{product_id} not found")
        
        update_item = product_up.model_dump(exclude_unset=True)
        for key,val in update_item.items():
            setattr(db_prod,key,val)
        
        session.add(db_prod)
        session.commit()
        session.refresh(db_prod)
    
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                detail="Data conflict (e.g., duplicate unique key or missing foreign key).")
    
    except OperationalError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
    
    except Exception as e:
        session.rollback()
        print(f"LOG: Unhandled exception: {e}") # Log the specific error for debugging
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="An unexpected internal error occurred.")
    
    serialize_data= ProductModel.model_validate(db_prod).model_dump()
    return JSONResponse(content={"message":"item updated","item":serialize_data},status_code=200)

@router.delete('/deleteProduct/{product_id}')
def delete_product_by_id(product_id:int, session:Session = Depends(get_db)):
    try:
        db_product = session.get(Product,product_id)
        if db_product is None:
            raise HTTPException(status_code=404, detail= f"The product with ID {product_id} not found")
        
        session.delete(db_product)
        session.commit()
    
    except OperationalError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
    except Exception as e:
        session.rollback()
        print(f"LOG: Unhandled exception: {e}") # Log the specific error for debugging
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="An unexpected internal error occurred.")
    
    return JSONResponse(content="Item deleted",status_code=200)
    
