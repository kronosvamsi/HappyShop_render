from sqlalchemy import create_engine,Column,Integer,String,Float,ForeignKey
from sqlalchemy.orm import relationship, declarative_base,sessionmaker
# from google.cloud.sql.connector import Connector
import os
from config import settings
# class Base(declarative_base()):

#     pass

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"

    id=Column(Integer, primary_key=True)
    name=Column(String(50), nullable=False)
    products=relationship("Product",back_populates="category_rel")
    

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    category_id = Column(Integer,ForeignKey("categories.id"))
    quantity = Column(Integer,default=0)
    price = Column(Float,default=0.0)
    
    category_rel = relationship("Category", back_populates="products")
    orders=relationship("Order",back_populates="product")

class Order(Base):

    __tablename__ = "orders"

    id=Column(Integer, primary_key=True)
    product_id= Column(Integer,ForeignKey("products.id"))
    user_id=Column(Integer, ForeignKey("users.id"))
    firstname=Column(String(50))
    lastname=Column(String(50))
    address=Column(String(100))

    product=relationship("Product",back_populates="orders")

    user=relationship("User",back_populates="orders")

class User(Base):
    __tablename__ = "users"

    id= Column(Integer, primary_key=True)
    name=Column(String(50))
    firstname=Column(String(50))
    lastname=Column(String(50))
    email=Column(String(50))
    orders=relationship("Order",back_populates="user")



# Get these from environment variables for security in Cloud Run/App Engine
# DB_USER = os.environ.get("DB_USER")          # e.g., 'app_user'
# DB_PASS = os.environ.get("DB_PASS")          # e.g., 'your_app_password'
# DB_NAME = os.environ.get("DB_NAME")          # e.g., 'my_app_db'
# # e.g., 'project-id:region:instance-id'
# INSTANCE_CONN_NAME = os.environ.get("INSTANCE_CONNECTION_NAME")


# It's recommended to initialize the Connector outside the request context (global scope)
# connector = Connector(refresh_strategy="lazy" )

# def getconn():
    # Inside this method, we call the connector's connect method, 
    # passing the standard database driver arguments (user, password, etc.).
    # conn = connector.connect(
    #     INSTANCE_CONN_NAME,
    #     # The Python database driver you are using
    #     "pymysql", 
    #     # --- HERE is where you select the user, password, and database ---
    #     user=DB_USER,
    #     password=DB_PASS,
    #     database=DB_NAME,
    #     # Optional: Set refresh strategy to "lazy" for serverless environments
        
    # )
    # return conn

# --- 4. Create the SQLAlchemy Engine ---
# SQLAlchemy uses the 'creator' argument to manage connections securely.
# engine = create_engine(
#     "mysql+pymysql://",  # Use an empty URL or just the dialect
#     creator=getconn,     # Pass your creator function here
#     pool_size=5,         # Recommended pool settings for serverless
#     max_overflow=2,
#     pool_timeout=30,
#     pool_recycle=1800
# )

# DB_URL= "mysql+mysqlconnector://root:mysql1234@127.0.0.1:3306/my_db"

# Aiven requires encrypted connections, so we enforce it with ssl_mode='REQUIRED'
# CONNECT_ARGS = {
#     # The key MUST be 'ssl_mode' (with an underscore) for mysql-connector-python
#     "ssl":{
#          "ssl_mode": "REQUIRED" 
#     }
   
# }

engine = create_engine(
         settings.DATABASE_URL,
         pool_recycle=3600,
         echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(autoflush=False,autocommit=False, bind=engine)

def get_db():
    session=Session()
    try:
        yield session
    finally:
        session.close()
