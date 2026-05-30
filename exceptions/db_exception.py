from functools import wraps
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, OperationalError

def db_exception(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        session = kwargs.get("session")
        try:
            return func(self, *args, **kwargs)
        
        except IntegrityError:
                session.rollback()
                raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Data conflict (duplicate key or foreign key issue)."
            )
        except OperationalError:
            session.rollback()
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection/service unavailable."
            )
        
        
    return wrapper