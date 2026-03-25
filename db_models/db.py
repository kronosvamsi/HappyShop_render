from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from db_models.models import Base

PYMYSQL_CONNECT_ARGS = {
    'ssl': {}  
}

# print(settings.DATABASE_URL)
engine = create_engine(
         settings.DATABASE_URL,
         connect_args=PYMYSQL_CONNECT_ARGS,
         pool_recycle=3600,
         echo=True)

# Base.metadata.create_all(engine)

Session = sessionmaker(autoflush=False,autocommit=False, bind=engine)

def get_db():
    session=Session()
    try:
        yield session
    finally:
        session.close()
