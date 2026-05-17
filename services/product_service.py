from db_models.models import Product
from data_models.pyd_models import ProductInput,ProductModel
from sqlalchemy.exc import IntegrityError, OperationalError
from fastapi import HTTPException,status

def getProducts(session):
    try:
        db_products=session.query(Product).all()
    
    except OperationalError:
        # Catches connection issues, server offline, etc.
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database service is unavailable or connection failed."
        )
    serialize_data=[ProductModel.model_validate(product).model_dump() for product in db_products]
    return serialize_data
    

def getProduct(session,product_id):
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
    
    return ProductModel.model_validate(db_product).model_dump()


def addProduct(session,new_product):
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
    
    return ProductModel.model_validate(db_product).model_dump()
    


def updateProduct(session, update_item,product_id):
    try:
        db_prod = session.get(Product,product_id)
        if db_prod is None:
            raise HTTPException(status_code=404, detail=f"The product with ID{product_id} not found")
        
        update_item = update_item.model_dump(exclude_unset=True)        
        
        for key,val in update_item.items():
            setattr(db_prod,key,val)
      
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
        
    serialize_data= ProductModel.model_validate(db_prod).model_dump()
    return serialize_data
    


def deleteProduct(session,product_id):
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
    return product_id

