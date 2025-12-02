from fastapi import FastAPI, Depends,HTTPException,status
from db_models.models import Session,Product,Category
from data_models.pyd_models import ProductModel,CategoryModel
# from  db_models.models import Product
from sqlalchemy.exc import IntegrityError, OperationalError
from pydantic import ValidationError
from routes import products,categories,users

app=FastAPI()

app.include_router(products.router)
app.include_router(categories.router)
app.include_router(users.router)

def get_db():
    session=Session()
    try:
        yield session
    finally:
        session.close()

@app.get("/")
def get_root():
    return {"message":"Welcome to Happy shop"}

@app.post("/addCategory")   
def add_category(new_category:CategoryModel, session:Session = Depends(get_db)):
    try:
        category_add=new_category.model_dump()
        del category_add['id']
        db_category=Category(**category_add)
        session.add(db_category)
        session.commit()
        session.refresh(db_category)
    
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
    except AttributeError:
        # This usually signals a bug in your code
        session.rollback()
        print("LOG: Critical AttributeError detected in post creation logic.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="A critical application error occurred.")
    
    except Exception as e:
        session.rollback()
        print(f"LOG: Unhandled exception: {e}") # Log the specific error for debugging
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                            detail="An unexpected internal error occurred.")
    
    return {"message":"Item added", "item":db_category}


