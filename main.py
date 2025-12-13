from fastapi import FastAPI, Depends,HTTPException,status
from db_models.models import Session,Product,Category
from data_models.pyd_models import ProductModel,CategoryModel
# from  db_models.models import Product
from sqlalchemy.exc import IntegrityError, OperationalError
from pydantic import ValidationError
from fastapi.responses import HTMLResponse
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

@app.get("/",response_class=HTMLResponse)
def get_root():
    return f"""
    <html>
    <head> 
    <title> Happyshop APi Info </title>
    </head>
    <body style="background-color:#010b13;color:white;text-align:center;">
    <h1> Welcome to Happyshop Docs !!</h1>
    <p>This is a happyshop api documentation </p>
    <p> There are 3 custom api endpoints:
    <ul>
    <li> Categories </li>
    <li> Products </li>
    <li> Categories </li>
    </ul>
    <h2>Categories End points </h2>
    <ul>
     <li> <code style = "color:#242424"> /categories </code>     =>  It fecthes the category Items from DB  </li>
     <li> <code style = "color:#242424"> /categories/category/category_id:int </code>     => To fetch the single category item by id  </li>
     <li> <code style = "color:#242424"> /categories/addCategory </code>    =>  To add the new category item  </li>
     <li> <code style = "color:#242424"> /categories/updateCategory/category_id:int </code>     =>   To update the category item by id  </li>
     <li> <code style = "color:#242424">  /categories/deleteCategory/category_id:int </code>    =>   To delete the category item from DB by id  </li>
     </ul>
     
     <p> Go to url <a href="https://happyshop-render.onrender.com/docs"> happyshop_api_docs </a> to get more info </p>
     </body>
    
    </html>

     """


