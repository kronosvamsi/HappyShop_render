from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, OperationalError
from db_models.models import User,get_db
from data_models.pyd_models import UserModel

router = APIRouter(
    prefix = "/users",
    tags=["users"],
    dependencies = [Depends(get_db)]
)

@router.get("/")
async def get_users(session:Session = Depends(get_db)):
    try:
        db_users = session.query(User).all()
        if len(db_users) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The users list in db is empty")
        
       
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
    except Exception as e:
        session.rollback()
        print(f"Log- unhandled exception {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= f"Unexpected error came in process "

        )
    data_items = [UserModel.model_validate(userobj).model_dump() for userobj in db_users]
    return JSONResponse(content={"message":"Usermodel items fetched from DB","items":data_items},status_code=200)


@router.get("/user/{user_id}")
def get_user_by_id(user_id:int, session:Session = Depends(get_db)):
    try:
        db_user = session.get(User, user_id)
        if db_user is None:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"The user id - {user_id} not found")
    
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
    data_item = UserModel.model_validate(db_user).model_dump()
    return JSONResponse(content= {"message":"The userobj by id fetched ","item":data_item},status_code=200)

@router.post('/addUser')
def addUser(new_user:UserModel, session:Session = Depends(get_db)):
    try:
        user_obj=new_user.model_dump()
        if len(user_obj.keys()) == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "The user obj is empty")
        
        db_user_obj=User(**user_obj)
        session.add(db_user_obj)
        session.commit()
        session.refresh(db_user_obj)
    
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
    
    return JSONResponse(content= "User with ID added",status_code=200)


@router.put("updateUser/{user_id}")
def update_user(user_id:int, update_user:UserModel, session:Session = Depends(get_db)):
    try:
        db_user=session.get(User,user_id)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details= f"The user id - {user_id} not found")
        
        update_user_obj=update_user.model_dump()
        for key,val in update_user_obj.items():
            setattr(db_user,key,val)
        
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    
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
    
    return JSONResponse(content=f"The user ID-{user_id} is updated",status_code=200)

@router.delete('/deleteUser/{user_id}')
def delete_user(user_id:int, session:Session = Depends(get_db)):
    try:
        db_user = session.get(User, user_id)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The User with ID - {user_id} not found")
        
        session.delete(db_user)
        session.commit()

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
    

    return JSONResponse(content= f"The user ID {user_id} deleted ",status_code=200)

