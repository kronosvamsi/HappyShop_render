from db_models.models import Product
from data_models.pyd_models import ProductInput,ProductModel
from sqlalchemy.exc import IntegrityError, OperationalError
from fastapi import HTTPException,status
from  exceptions.db_exception import db_exception

@db_exception
def getProducts(session):
    db_products=session.query(Product).all()
    serialize_data=[ProductModel.model_validate(product).model_dump() for product in db_products]
    return serialize_data
    
@db_exception
def getProduct(session,product_id):
    db_product=session.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail=f"Product by id {product_id} is not found ")

    return ProductModel.model_validate(db_product).model_dump()

@db_exception
def addProduct(session,new_product):
    product_item=new_product.model_dump()
    db_product=Product(**product_item)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return ProductModel.model_validate(db_product).model_dump()
    

@db_exception
def updateProduct(session, update_item,product_id): 
    db_prod = session.get(Product,product_id)
    if db_prod is None:
        raise HTTPException(status_code=404, detail=f"The product with ID{product_id} not found")
    
    update_item = update_item.model_dump(exclude_unset=True)        
    for key,val in update_item.items():
        setattr(db_prod,key,val)
    
    session.commit()
    session.refresh(db_prod)   
    serialize_data= ProductModel.model_validate(db_prod).model_dump()
    return serialize_data
    

@db_exception
def deleteProduct(session,product_id):
    db_product = session.get(Product,product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail= f"The product with ID {product_id} not found")
    
    session.delete(db_product)
    session.commit()
    return product_id

