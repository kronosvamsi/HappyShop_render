from fastapi import FastAPI
# from db_models.models import Product,Category
# from data_models.pyd_models import ProductModel,CategoryModel
# from  db_models.models import Product

from pydantic import ValidationError
from fastapi.responses import HTMLResponse,JSONResponse
from routes import products,categories,users,auth
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

origins = [
    "http://localhost:5173",    ## react app url
    
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # MUST be a list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(products.router)
app.include_router(categories.router)
app.include_router(users.router)
app.include_router(auth.router)

# def get_db():
#     session=Session()
#     try:
#         yield session
#     finally:
#         session.close()

@app.get("/",response_class=HTMLResponse)
def get_root():
    return f"""
    <html>
    <head> 
    <title> Happyshop APi Info </title>
    </head>
    <body style="background-color:#010b13;color:white;">
    <h1> Welcome to Happyshop Docs !!</h1>
    <p>This is a happyshop api documentation </p>
    <p> There are 3 custom api endpoints:</p>
    
    <ul style = "padding:1px;">
    <li style="font-size:18px;">  Categories  </li>
    <li style="font-size:18px;">  Products  </li>
    <li style="font-size:18px;">   Users </li>
    </ul>
    
    <h2>Categories End points </h2>
    <ul style = "padding:1px;">
     <li style = "font-size:16px; margin:3px 0px "> <code style = "color:#F2F2F2"> /categories </code>        :  It fecthes the category Items from DB  </li>
     <li style = "font-size:16px; margin:3px 0px;"> <code style = "color:#F2F2F2; "> /categories/category/category_id:Int </code>     : To fetch the single category item by id  </li>
     <li style = "font-size:16px; margin:3px 0px;"> <code style = "color:#F2F2F2; "> /categories/addCategory </code>    :  To add the new category item  </li>
     <li style = "font-size:16px; margin:3px 0px;"> <code style = "color:#F2F2F2; "> /categories/updateCategory/category_id:Int </code>     :   To update the category item by id  </li>
     <li style = "font-size:16px; margin:3px 0px;"> <code style = "color:#F2F2F2;">  /categories/deleteCategory/category_id:Int </code>    :   To delete the category item from DB by id  </li>
     </ul>
     
     <p> Go to url <a style="color:#488cfa;" href="https://happyshop-render.onrender.com/docs"> happyshop_api_docs </a> to get more info </p>
     </body>
    
    </html>

     """

@app.get("/api/status")
def app_health_check():
    return JSONResponse(content={"status":"healthy"}, status_code=200)


